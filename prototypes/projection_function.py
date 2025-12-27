#!/usr/bin/env python3
"""
Projection Function Prototype

Implements Venkatraman's concept:
    projection_function(datagraph, moment_context) → context_graph

Given accumulated decision traces (datagraph) and current situation,
returns the relevant subset of knowledge for THIS moment.

This is where the three layers meet:
- Knowledge graph: semantic grounding (what things mean)
- Datagraph: learned patterns (what's worked before)
- Context graph: moment-specific projection (what matters now)
"""

import json
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict
from pathlib import Path

from decision_trace_extractor import DecisionTrace, DecisionTraceExtractor


@dataclass
class ContextGraph:
    """
    The projected context for a specific moment.

    This is what gets assembled for the AI system to consider
    when making decisions RIGHT NOW.
    """
    # Relevant precedents from history
    precedents: List[DecisionTrace]

    # Extracted patterns applicable to this situation
    applicable_patterns: List[str]

    # Warnings based on past failures
    warnings: List[str]

    # Suggested tools based on history
    suggested_tools: List[str]

    # Confidence score (0-1)
    relevance_score: float

    def to_prompt_context(self) -> str:
        """Format as context that could be injected into a prompt."""
        lines = ["## Relevant Context from History", ""]

        if self.precedents:
            lines.append("### Similar Past Decisions")
            for i, p in enumerate(self.precedents[:3], 1):
                lines.append(f"{i}. [{p.decision_type}] {p.summary}")
                if p.reasoning:
                    lines.append(f"   Reasoning: {p.reasoning[:100]}...")
            lines.append("")

        if self.applicable_patterns:
            lines.append("### Patterns That Apply")
            for pattern in self.applicable_patterns[:5]:
                lines.append(f"- {pattern}")
            lines.append("")

        if self.warnings:
            lines.append("### ⚠️ Warnings from History")
            for warning in self.warnings[:3]:
                lines.append(f"- {warning}")
            lines.append("")

        if self.suggested_tools:
            lines.append(f"### Suggested Tools: {', '.join(self.suggested_tools[:5])}")

        return "\n".join(lines)


@dataclass
class DecisionDatagraph:
    """
    The accumulated learning from all decision traces.

    This is the "datagraph" in Venkatraman's framework -
    the strategic asset that compounds over time.
    """
    traces: List[DecisionTrace] = field(default_factory=list)

    # Indexed patterns for fast lookup
    by_type: Dict[str, List[DecisionTrace]] = field(default_factory=lambda: defaultdict(list))
    by_tool: Dict[str, List[DecisionTrace]] = field(default_factory=lambda: defaultdict(list))
    by_keyword: Dict[str, List[DecisionTrace]] = field(default_factory=lambda: defaultdict(list))

    # Learned heuristics
    recovery_patterns: List[Tuple[str, str]] = field(default_factory=list)  # (trigger, response)
    tool_sequences: Dict[str, List[str]] = field(default_factory=dict)  # tool -> likely next tools

    def add_trace(self, trace: DecisionTrace):
        """Add a trace and update indices."""
        self.traces.append(trace)

        # Index by type
        self.by_type[trace.decision_type].append(trace)

        # Index by tools used
        for tool in trace.tools_used:
            self.by_tool[tool].append(trace)

        # Index by keywords in summary
        keywords = self._extract_keywords(trace.summary + " " + trace.context)
        for kw in keywords:
            self.by_keyword[kw].append(trace)

        # Extract recovery patterns
        if trace.decision_type == 'recovery':
            self.recovery_patterns.append((
                trace.context[:100],
                trace.action_taken[:100] if trace.action_taken else trace.summary[:100]
            ))

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract meaningful keywords from text."""
        # Simple keyword extraction - could be enhanced with NLP
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        # Filter common words
        stopwords = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'will',
                     'would', 'could', 'should', 'there', 'their', 'about', 'which'}
        return [w for w in words if w not in stopwords][:10]

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the datagraph."""
        return {
            'total_traces': len(self.traces),
            'decision_types': {k: len(v) for k, v in self.by_type.items()},
            'tools_indexed': len(self.by_tool),
            'keywords_indexed': len(self.by_keyword),
            'recovery_patterns': len(self.recovery_patterns),
        }


class ProjectionFunction:
    """
    The projection function that selects relevant context.

    This is the key strategic component - it defines what
    the AI system can even consider in a given moment.
    """

    def __init__(self, datagraph: DecisionDatagraph):
        self.datagraph = datagraph

    def project(
        self,
        current_task: str,
        current_tools: Optional[List[str]] = None,
        current_error: Optional[str] = None
    ) -> ContextGraph:
        """
        Project relevant context for the current moment.

        Args:
            current_task: Description of what user is trying to do
            current_tools: Tools being considered
            current_error: If handling an error, what went wrong

        Returns:
            ContextGraph with relevant precedents, patterns, warnings
        """
        precedents = []
        patterns = []
        warnings = []
        suggested_tools = []

        # 1. If handling an error, find recovery precedents
        if current_error:
            recovery_traces = self.datagraph.by_type.get('recovery', [])
            for trace in recovery_traces:
                if self._text_similarity(current_error, trace.context) > 0.3:
                    precedents.append(trace)
                    if trace.action_taken:
                        patterns.append(f"Past recovery: {trace.action_taken[:80]}")

        # 2. Find traces with similar keywords to current task
        task_keywords = self._extract_keywords(current_task)
        keyword_matches = defaultdict(int)

        for kw in task_keywords:
            for trace in self.datagraph.by_keyword.get(kw, []):
                keyword_matches[id(trace)] += 1

        # Sort by number of keyword matches
        matched_traces = sorted(
            [(trace, keyword_matches[id(trace)])
             for trace in self.datagraph.traces
             if id(trace) in keyword_matches],
            key=lambda x: -x[1]
        )

        for trace, score in matched_traces[:5]:
            if trace not in precedents:
                precedents.append(trace)

        # 3. If specific tools mentioned, find traces using those tools
        if current_tools:
            for tool in current_tools:
                tool_traces = self.datagraph.by_tool.get(tool, [])
                for trace in tool_traces[:3]:
                    if trace not in precedents:
                        precedents.append(trace)

                # Suggest commonly co-occurring tools
                co_tools = defaultdict(int)
                for trace in tool_traces:
                    for other_tool in trace.tools_used:
                        if other_tool != tool:
                            co_tools[other_tool] += 1

                for co_tool, count in sorted(co_tools.items(), key=lambda x: -x[1])[:3]:
                    if co_tool not in suggested_tools:
                        suggested_tools.append(co_tool)

        # 4. Extract warnings from past failures
        for trace in self.datagraph.by_type.get('recovery', []):
            # If current task is similar to something that failed before
            if self._text_similarity(current_task, trace.context) > 0.2:
                warnings.append(f"Similar task failed before: {trace.summary[:60]}")

        # 5. Extract applicable patterns from precedents
        for trace in precedents[:5]:
            if trace.decision_type == 'sequencing':
                patterns.append(f"Sequencing: {trace.summary[:60]}")
            elif trace.decision_type == 'planning':
                patterns.append(f"Planning approach: {trace.summary[:60]}")

        # Calculate relevance score
        relevance = min(1.0, len(precedents) / 5.0)

        return ContextGraph(
            precedents=precedents[:10],
            applicable_patterns=patterns[:5],
            warnings=warnings[:3],
            suggested_tools=suggested_tools[:5],
            relevance_score=relevance
        )

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        stopwords = {'this', 'that', 'with', 'from', 'have', 'been', 'were', 'will'}
        return [w for w in words if w not in stopwords][:15]

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Simple keyword-based similarity score."""
        words1 = set(self._extract_keywords(text1))
        words2 = set(self._extract_keywords(text2))

        if not words1 or not words2:
            return 0.0

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0


def build_datagraph_from_sessions(session_files: List[str]) -> DecisionDatagraph:
    """Build a datagraph from multiple session transcript files."""
    datagraph = DecisionDatagraph()
    extractor = DecisionTraceExtractor()

    for fpath in session_files:
        try:
            traces = extractor.extract(fpath)
            for trace in traces:
                datagraph.add_trace(trace)
        except Exception as e:
            print(f"Warning: Could not process {fpath}: {e}")

    return datagraph


def demo():
    """Demonstrate the projection function."""
    from pathlib import Path

    # Find some session files
    projects_dir = Path.home() / ".claude" / "projects"
    session_files = []

    for project_dir in projects_dir.iterdir():
        if project_dir.is_dir():
            jsonl_files = [f for f in project_dir.glob("*.jsonl")
                          if not f.name.startswith("agent-")]
            session_files.extend(str(f) for f in jsonl_files[:2])

    session_files = session_files[:10]  # Limit for demo

    print(f"Building datagraph from {len(session_files)} sessions...")
    datagraph = build_datagraph_from_sessions(session_files)

    print(f"\nDatagraph stats:")
    stats = datagraph.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # Create projection function
    project = ProjectionFunction(datagraph)

    # Demo: Project context for different scenarios
    print("\n" + "="*70)
    print("PROJECTION FUNCTION DEMO")
    print("="*70)

    scenarios = [
        {
            "task": "I need to create a new git branch and set up a worktree",
            "tools": ["Bash"],
            "error": None
        },
        {
            "task": "The build is failing with a TypeScript error",
            "tools": ["Bash", "Read"],
            "error": "TypeScript compilation failed"
        },
        {
            "task": "I want to commit my changes",
            "tools": ["Bash"],
            "error": None
        }
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['task'][:50]}... ---\n")

        context = project.project(
            current_task=scenario['task'],
            current_tools=scenario.get('tools'),
            current_error=scenario.get('error')
        )

        print(context.to_prompt_context())
        print(f"\n[Relevance score: {context.relevance_score:.2f}]")


if __name__ == "__main__":
    demo()
