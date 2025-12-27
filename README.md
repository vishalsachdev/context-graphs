# Context Graphs Research

Research exploring **context graphs as competitive infrastructure** in the age of AI.

## Core Thesis

Context graphs are the "action layer" of a three-tier intelligence infrastructure:

```
┌─────────────────────────────────────────────────────────────┐
│  KNOWLEDGE GRAPHS  │  Semantic layer - what things mean     │
├────────────────────┼────────────────────────────────────────┤
│     DATAGRAPHS     │  Learning layer - behavioral data      │
│                    │  with network effects (strategic)      │
├────────────────────┼────────────────────────────────────────┤
│   CONTEXT GRAPHS   │  Action layer - moment-specific        │
│                    │  projections for human-machine coord   │
└────────────────────┴────────────────────────────────────────┘
```

**Key insight**: Context graphs are **projections** of datagraphs, not standalone assets. Competitive advantage comes from the underlying datagraph and the projection function that selects "what matters now."

## Key Sources

| Source | Key Thesis |
|--------|------------|
| [Foundation Capital (Dec 2025)](https://foundationcapital.com/context-graphs-ais-trillion-dollar-opportunity/) | Next trillion-dollar platforms = "systems of record for decisions" |
| [Venkatraman (Dec 2025)](https://www.linkedin.com/pulse/why-context-graphs-make-datagraphs-strategically-venkat-venkatraman-xfdqf/) | Context graphs make datagraphs strategically decisive |

## What's Here

### `/research`
Framework synthesis comparing Foundation Capital and Venkatraman perspectives.

### `/prototypes`
Working Python implementations:

| Script | What It Does |
|--------|--------------|
| `decision_trace_extractor.py` | Extracts decision traces from Claude Code thinking blocks |
| `cross_session_analyzer.py` | Analyzes patterns across multiple sessions |
| `projection_function.py` | Implements the projection function (datagraph → context) |

### `/outputs`
Pre-generated analysis results (viewable without running code):

- `cross-session-analysis.md` - Decision patterns across 12 sessions
- `projection-function-demo.md` - 5 scenarios with projected context
- `sample-decision-traces.md` - Detailed trace examples

## Key Findings

1. **Claude Code thinking blocks ARE decision traces** - They contain explicit reasoning (task decomposition, error recovery, sequencing logic)

2. **Cross-session patterns reveal your "datagraph"**:
   - 15.8% recovery rate (1 in 6 decisions handle errors)
   - Core tool vocabulary: Bash → Edit → Read
   - 44 recovery patterns captured

3. **The projection function works**:
   - Indexes 153 traces, 464 keywords
   - Given a task, finds relevant precedents
   - Returns warnings based on past failures

4. **Strategic insight**: Who controls the projection function controls what the AI can consider.

## Running the Code

```bash
cd prototypes

# Extract traces from a single session
python3 decision_trace_extractor.py ~/.claude/projects/*/session.jsonl

# Analyze patterns across sessions
python3 cross_session_analyzer.py --sample 15

# Demo the projection function
python3 projection_function.py
```

## Origin

This research started as an experiment in [helloworld](https://github.com/vishalsachdev/helloworld) and was graduated to a standalone repo.
