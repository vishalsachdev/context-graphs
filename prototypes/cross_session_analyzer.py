#!/usr/bin/env python3
"""
Cross-Session Decision Pattern Analyzer

Analyzes decision patterns across multiple Claude Code sessions to identify:
1. Recurring decision types (what kinds of decisions are made most?)
2. Recovery patterns (how are errors handled?)
3. Tool sequences (what tool combinations work?)
4. Decision heuristics (implicit rules being followed)

This builds toward Venkatraman's concept of a "datagraph" -
capturing product-in-use behavior that compounds learning.
"""

import json
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Import our decision trace extractor
from decision_trace_extractor import (
    DecisionTraceExtractor,
    DecisionTrace,
    DecisionPatternMatcher
)


@dataclass
class SessionSummary:
    """Summary of decision patterns from a single session."""
    session_id: str
    project: str
    file_path: str
    created: str
    trace_count: int
    decision_types: Dict[str, int]
    tools_used: Dict[str, int]
    recovery_count: int
    sample_traces: List[DecisionTrace] = field(default_factory=list)


@dataclass
class AggregatePatterns:
    """Aggregated patterns across all analyzed sessions."""
    total_sessions: int = 0
    total_traces: int = 0
    decision_type_counts: Dict[str, int] = field(default_factory=Counter)
    tool_counts: Dict[str, int] = field(default_factory=Counter)
    recovery_patterns: List[str] = field(default_factory=list)
    tool_sequences: Dict[str, int] = field(default_factory=Counter)
    projects_analyzed: set = field(default_factory=set)

    def add_session(self, summary: SessionSummary):
        """Add a session's patterns to the aggregate."""
        self.total_sessions += 1
        self.total_traces += summary.trace_count
        self.projects_analyzed.add(summary.project)

        for dtype, count in summary.decision_types.items():
            self.decision_type_counts[dtype] += count

        for tool, count in summary.tools_used.items():
            self.tool_counts[tool] += count

        self.recovery_patterns.extend([
            t.summary for t in summary.sample_traces
            if t.decision_type == 'recovery'
        ])


def get_sessions_via_aichat(
    query: str = "",
    limit: int = 20,
    by_time: bool = True
) -> List[Dict]:
    """
    Get sessions using aichat search command.

    Returns list of session metadata dicts.
    """
    cmd = ["aichat", "search", "--json"]
    if by_time:
        cmd.append("--by-time")
    if query:
        cmd.append(query)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        sessions = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    sessions.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return sessions[:limit]

    except subprocess.TimeoutExpired:
        print("Warning: aichat search timed out")
        return []
    except FileNotFoundError:
        print("Warning: aichat not found, using fallback")
        return []


def get_sample_sessions(
    sample_size: int = 10,
    diverse: bool = True
) -> List[Dict]:
    """
    Get a diverse sample of sessions for analysis.

    If diverse=True, tries to sample across different:
    - Projects
    - Time periods
    - Query types (git, error, build, etc.)
    """
    all_sessions = []

    if diverse:
        # Get sessions with different characteristics
        queries = [
            "",              # Recent sessions (any topic)
            "error",         # Error handling sessions
            "git",           # Git-related work
            "build",         # Build/compile work
            "test",          # Testing work
        ]

        per_query = max(2, sample_size // len(queries))

        for query in queries:
            sessions = get_sessions_via_aichat(query, limit=per_query)
            all_sessions.extend(sessions)
    else:
        all_sessions = get_sessions_via_aichat("", limit=sample_size)

    # Deduplicate by session_id
    seen = set()
    unique = []
    for s in all_sessions:
        sid = s.get('session_id', s.get('file_path'))
        if sid not in seen:
            seen.add(sid)
            unique.append(s)

    return unique[:sample_size]


def analyze_session(session_meta: Dict, extractor: DecisionTraceExtractor) -> Optional[SessionSummary]:
    """Analyze a single session and return its summary."""
    file_path = session_meta.get('file_path', '')

    if not file_path or not Path(file_path).exists():
        return None

    try:
        traces = extractor.extract(file_path)

        if not traces:
            return None

        # Count decision types
        type_counts = Counter(t.decision_type for t in traces)

        # Count tools used
        tool_counts = Counter()
        for t in traces:
            for tool in t.tools_used:
                tool_counts[tool] += 1

        # Count recoveries
        recovery_count = type_counts.get('recovery', 0)

        # Sample some traces for qualitative analysis
        sample_traces = traces[:5]

        return SessionSummary(
            session_id=session_meta.get('session_id', 'unknown'),
            project=session_meta.get('project', 'unknown'),
            file_path=file_path,
            created=session_meta.get('created', ''),
            trace_count=len(traces),
            decision_types=dict(type_counts),
            tools_used=dict(tool_counts),
            recovery_count=recovery_count,
            sample_traces=sample_traces
        )

    except Exception as e:
        print(f"  Error analyzing {file_path}: {e}")
        return None


def analyze_tool_sequences(sessions: List[SessionSummary]) -> Dict[str, int]:
    """
    Analyze common tool sequences across sessions.

    Returns counts of tool pair sequences.
    """
    sequences = Counter()

    for session in sessions:
        tools = list(session.tools_used.keys())
        # Create pairs
        for i in range(len(tools) - 1):
            pair = f"{tools[i]} → {tools[i+1]}"
            sequences[pair] += 1

    return dict(sequences.most_common(20))


def generate_report(patterns: AggregatePatterns) -> str:
    """Generate a human-readable report of patterns."""
    lines = [
        "=" * 70,
        "CROSS-SESSION DECISION PATTERN ANALYSIS",
        "=" * 70,
        "",
        f"Sessions analyzed: {patterns.total_sessions}",
        f"Total decision traces: {patterns.total_traces}",
        f"Projects covered: {len(patterns.projects_analyzed)}",
        f"  ({', '.join(sorted(patterns.projects_analyzed))})",
        "",
        "-" * 70,
        "DECISION TYPE DISTRIBUTION",
        "-" * 70,
    ]

    total = sum(patterns.decision_type_counts.values())
    for dtype, count in patterns.decision_type_counts.most_common():
        pct = (count / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 2)
        lines.append(f"  {dtype:20} {count:4} ({pct:5.1f}%) {bar}")

    lines.extend([
        "",
        "-" * 70,
        "TOOL USAGE",
        "-" * 70,
    ])

    for tool, count in patterns.tool_counts.most_common(15):
        lines.append(f"  {tool:20} {count:4}")

    if patterns.recovery_patterns:
        lines.extend([
            "",
            "-" * 70,
            "SAMPLE RECOVERY PATTERNS (Error Handling)",
            "-" * 70,
        ])

        for i, pattern in enumerate(patterns.recovery_patterns[:10], 1):
            # Truncate long patterns
            if len(pattern) > 70:
                pattern = pattern[:67] + "..."
            lines.append(f"  {i}. {pattern}")

    lines.extend([
        "",
        "=" * 70,
        "STRATEGIC INSIGHTS (Venkatraman Lens)",
        "=" * 70,
        "",
    ])

    # Generate insights based on patterns
    top_decision = patterns.decision_type_counts.most_common(1)
    if top_decision:
        dtype, count = top_decision[0]
        lines.append(f"• Most common decision type: {dtype} ({count} instances)")
        lines.append(f"  → This is your primary 'decision mode' when using Claude Code")

    recovery_pct = (
        patterns.decision_type_counts.get('recovery', 0) /
        max(1, sum(patterns.decision_type_counts.values())) * 100
    )
    lines.append(f"")
    lines.append(f"• Recovery rate: {recovery_pct:.1f}% of decisions are error recovery")
    if recovery_pct > 20:
        lines.append(f"  → High recovery rate suggests opportunity for proactive error prevention")
    else:
        lines.append(f"  → Low recovery rate indicates smooth workflows")

    top_tools = patterns.tool_counts.most_common(3)
    if top_tools:
        lines.append(f"")
        lines.append(f"• Top tool trio: {', '.join(t[0] for t in top_tools)}")
        lines.append(f"  → These form your core 'action vocabulary'")

    lines.append("")

    return "\n".join(lines)


def get_sessions_from_directory(transcripts_dir: Path, limit: int = 10) -> List[Dict]:
    """
    Get sessions from a local directory of JSONL files.

    Args:
        transcripts_dir: Directory containing .jsonl transcript files
        limit: Max number of sessions to return
    """
    sessions = []

    # Handle both flat directory and nested project directories
    jsonl_files = list(transcripts_dir.glob("*.jsonl"))
    if not jsonl_files:
        # Try nested structure like ~/.claude/projects/*/
        jsonl_files = list(transcripts_dir.glob("*/*.jsonl"))

    # Filter out agent files and sort by modification time
    jsonl_files = [f for f in jsonl_files if not f.name.startswith("agent-")]
    jsonl_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    for fpath in jsonl_files[:limit]:
        project = fpath.parent.name.split('-')[-1] if '-' in fpath.parent.name else fpath.stem
        sessions.append({
            'file_path': str(fpath),
            'project': project,
            'session_id': fpath.stem,
        })

    return sessions


def main():
    """Run cross-session analysis."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze decision patterns across Claude Code sessions"
    )
    parser.add_argument(
        "--sample", "-n",
        type=int,
        default=10,
        help="Number of sessions to sample (default: 10)"
    )
    parser.add_argument(
        "--query", "-q",
        type=str,
        default="",
        help="Search query to filter sessions"
    )
    parser.add_argument(
        "--transcripts", "-t",
        type=str,
        default=None,
        help="Path to transcripts directory (default: ~/.claude/projects)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of report"
    )

    args = parser.parse_args()

    print(f"Getting sample of {args.sample} sessions...")

    # Determine transcript source
    if args.transcripts:
        transcripts_path = Path(args.transcripts).expanduser()
        print(f"Using transcripts from: {transcripts_path}")
        sessions = get_sessions_from_directory(transcripts_path, limit=args.sample)
    elif args.query:
        sessions = get_sessions_via_aichat(args.query, limit=args.sample)
    else:
        sessions = get_sample_sessions(sample_size=args.sample, diverse=True)

    print(f"Found {len(sessions)} sessions to analyze\n")

    extractor = DecisionTraceExtractor()
    patterns = AggregatePatterns()
    summaries = []

    for i, session_meta in enumerate(sessions, 1):
        project = session_meta.get('project', 'unknown')
        print(f"[{i}/{len(sessions)}] Analyzing {project}...", end=" ")

        summary = analyze_session(session_meta, extractor)

        if summary:
            patterns.add_session(summary)
            summaries.append(summary)
            print(f"✓ ({summary.trace_count} traces)")
        else:
            print("✗ (no traces)")

    print()

    if args.json:
        output = {
            "sessions_analyzed": patterns.total_sessions,
            "total_traces": patterns.total_traces,
            "projects": list(patterns.projects_analyzed),
            "decision_types": dict(patterns.decision_type_counts),
            "tool_counts": dict(patterns.tool_counts),
            "recovery_samples": patterns.recovery_patterns[:10],
        }
        print(json.dumps(output, indent=2))
    else:
        report = generate_report(patterns)
        print(report)


if __name__ == "__main__":
    main()
