#!/usr/bin/env python3
"""
Decision Trace Extractor

Extracts business-level decision traces from Claude Code session transcripts.

Foundation Capital's key insight:
> "Decision traces operate at a higher level of abstraction than execution traces—
> not 'the agent called this tool with these parameters' but 'this decision was
> made under this policy, with this exception, approved by this person, based on
> this precedent.'"

This prototype attempts to bridge the gap between:
- Execution traces (tool calls, parameters)
- Decision traces (business-level choices and reasoning)
"""

import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any
from pathlib import Path
from datetime import datetime

@dataclass
class DecisionTrace:
    """A structured representation of a decision made during a session."""
    timestamp: str
    decision_type: str      # planning, recovery, diagnosis, sequencing, clarification
    summary: str            # 1-line summary of the decision
    context: str            # What situation triggered this decision
    reasoning: str          # Why this choice was made
    action_taken: str       # What was done
    tools_used: List[str]   # Which tools were invoked
    outcome: Optional[str]  # What happened (if known)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DecisionPatternMatcher:
    """Identifies decision patterns in thinking traces."""

    PATTERNS = {
        'planning': [
            r"let me (break down|plan|start|set up|create)",
            r"(first|before|to begin),? (i should|let me|i need to)",
            r"this (requires|needs|involves) (multiple|several)",
        ],
        'recovery': [
            r"(failed|error|didn't work|issue)",
            r"let me try (a different|another|instead)",
            r"workaround",
        ],
        'diagnosis': [
            r"looking at the (error|issue|problem)",
            r"the (reason|cause|issue) (is|was|seems)",
            r"this (happens|failed|broke) because",
        ],
        'sequencing': [
            r"(first|then|next|after that|before)",
            r"i need to .+ (before|first)",
            r"(already|now|done).+ (move on|proceed|continue)",
        ],
        'clarification': [
            r"the user (wants|is asking|means)",
            r"(should i|do they want)",
            r"(unclear|ambiguous|not sure)",
        ],
        'context_awareness': [
            r"(we're|i'm) (already|currently|now)",
            r"(the current|existing) (state|branch|file)",
            r"(remember|note) that",
        ],
    }

    def classify(self, thinking_text: str) -> List[str]:
        """Classify a thinking block into decision types."""
        text_lower = thinking_text.lower()
        matches = []
        for decision_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    matches.append(decision_type)
                    break
        return matches if matches else ['general']


class TranscriptParser:
    """Parses Claude Code JSONL transcripts."""

    def __init__(self, transcript_path: str):
        self.path = Path(transcript_path)
        self.messages = []
        self.thinking_blocks = []
        self.tool_uses = []

    def parse(self) -> None:
        """Load and parse the transcript."""
        with open(self.path, 'r') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    self.messages.append(obj)
                    self._extract_content(obj)
                except json.JSONDecodeError:
                    continue

    def _extract_content(self, obj: Dict) -> None:
        """Extract thinking blocks and tool uses from a message."""
        if obj.get('type') != 'assistant':
            return

        message = obj.get('message', {})
        content = message.get('content', [])
        timestamp = obj.get('timestamp', '')

        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'thinking':
                self.thinking_blocks.append({
                    'timestamp': timestamp,
                    'thinking': block.get('thinking', ''),
                    'parent_uuid': obj.get('parentUuid'),
                })
            elif block.get('type') == 'tool_use':
                self.tool_uses.append({
                    'timestamp': timestamp,
                    'name': block.get('name'),
                    'input': block.get('input', {}),
                })


class DecisionTraceExtractor:
    """Main extractor that converts transcripts to decision traces."""

    def __init__(self):
        self.pattern_matcher = DecisionPatternMatcher()

    def extract(self, transcript_path: str) -> List[DecisionTrace]:
        """Extract decision traces from a transcript."""
        parser = TranscriptParser(transcript_path)
        parser.parse()

        traces = []
        for i, block in enumerate(parser.thinking_blocks):
            thinking = block['thinking']
            if not thinking or len(thinking) < 50:  # Skip trivial blocks
                continue

            # Classify the decision type
            decision_types = self.pattern_matcher.classify(thinking)

            # Find associated tool uses (within ~1 minute window)
            associated_tools = self._find_associated_tools(
                block['timestamp'],
                parser.tool_uses
            )

            # Create a decision trace
            trace = DecisionTrace(
                timestamp=block['timestamp'],
                decision_type=decision_types[0] if decision_types else 'general',
                summary=self._summarize(thinking),
                context=self._extract_context(thinking),
                reasoning=self._extract_reasoning(thinking),
                action_taken=self._extract_action(thinking),
                tools_used=[t['name'] for t in associated_tools],
                outcome=None,  # Would need to look at subsequent messages
            )
            traces.append(trace)

        return traces

    def _summarize(self, thinking: str, max_len: int = 100) -> str:
        """Create a 1-line summary of the thinking."""
        # Take first sentence or first N chars
        first_line = thinking.split('\n')[0]
        if len(first_line) <= max_len:
            return first_line
        return first_line[:max_len-3] + '...'

    def _extract_context(self, thinking: str) -> str:
        """Extract what situation triggered this decision."""
        # Look for context-setting phrases
        lines = thinking.split('\n')
        for line in lines[:3]:  # First few lines usually set context
            if any(phrase in line.lower() for phrase in
                   ['the user', 'we have', 'currently', 'the error', 'looking at']):
                return line.strip()
        return lines[0].strip() if lines else ''

    def _extract_reasoning(self, thinking: str) -> str:
        """Extract the reasoning/justification."""
        # Look for reasoning phrases
        reasoning_patterns = [
            r"because\s+(.+?)(?:\.|$)",
            r"since\s+(.+?)(?:\.|$)",
            r"this (means|indicates|suggests)\s+(.+?)(?:\.|$)",
        ]
        for pattern in reasoning_patterns:
            match = re.search(pattern, thinking.lower())
            if match:
                return match.group(0)[:200]
        return ''

    def _extract_action(self, thinking: str) -> str:
        """Extract what action was decided on."""
        action_patterns = [
            r"let me\s+(.+?)(?:\.|$)",
            r"i (should|will|need to)\s+(.+?)(?:\.|$)",
        ]
        for pattern in action_patterns:
            match = re.search(pattern, thinking.lower())
            if match:
                return match.group(0)[:200]
        return ''

    def _find_associated_tools(
        self,
        timestamp: str,
        tool_uses: List[Dict],
        window_seconds: int = 60
    ) -> List[Dict]:
        """Find tool uses within a time window of a thinking block."""
        try:
            think_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except:
            return []

        associated = []
        for tool in tool_uses:
            try:
                tool_time = datetime.fromisoformat(
                    tool['timestamp'].replace('Z', '+00:00')
                )
                diff = abs((tool_time - think_time).total_seconds())
                if diff <= window_seconds:
                    associated.append(tool)
            except:
                continue
        return associated


def main():
    """Run the extractor on a transcript."""
    if len(sys.argv) < 2:
        print("Usage: python decision_trace_extractor.py <transcript.jsonl>")
        print("\nExample:")
        print("  python decision_trace_extractor.py ~/.claude/projects/*/session.jsonl")
        sys.exit(1)

    extractor = DecisionTraceExtractor()
    transcript_path = sys.argv[1]

    print(f"Extracting decision traces from: {transcript_path}\n")

    traces = extractor.extract(transcript_path)

    print(f"Found {len(traces)} decision traces:\n")
    print("=" * 80)

    for i, trace in enumerate(traces[:10], 1):  # Show first 10
        print(f"\n[{i}] {trace.decision_type.upper()}")
        print(f"    Time: {trace.timestamp}")
        print(f"    Summary: {trace.summary}")
        if trace.context:
            print(f"    Context: {trace.context[:100]}...")
        if trace.tools_used:
            print(f"    Tools: {', '.join(trace.tools_used)}")
        print("-" * 80)

    # Output as JSON for further processing
    if '--json' in sys.argv:
        output = [t.to_dict() for t in traces]
        print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
