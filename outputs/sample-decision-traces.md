# Sample Decision Traces

**Generated**: 2025-12-27 12:34

---

## What Are Decision Traces?


Decision traces capture the **reasoning** behind actions, not just the actions themselves.

Foundation Capital's definition:
> "Decision traces operate at a higher level of abstraction than execution traces—
> not 'the agent called this tool with these parameters' but 'this decision was
> made under this policy, with this exception, approved by this person, based on
> this precedent.'"

In Claude Code, the **thinking blocks** in session transcripts contain this reasoning.

## Source Session

- **File**: `4bf0ea08-9c21-4cd5-b924-1c3b61036bb2.jsonl`
- **Project**: helloworld
- **Traces found**: 61

---

## Sample Traces

### Trace #1: PLANNING

**Timestamp**: `2025-12-27T17:54:57.142Z`

**Summary**:
> The user wants to start an experiment to explore "context graphs" based on the strategic essay th...

**Context** (what triggered this):
> The user wants to start an experiment to explore "context graphs" based on the strategic essay they've shared. This is a rich topic that combines AI systems architecture with business strategy.

**Action** (what was decided):
> let me start by understanding what they want to explore and set up the experiment properly.

**Associated Tools**: `WebSearch, WebFetch`

---

### Trace #2: RECOVERY

**Timestamp**: `2025-12-27T17:55:20.772Z`

**Summary**:
> The WebFetch tool failed due to a deployment issue. Let me try a web search instead to get inform...

**Context** (what triggered this):
> The WebFetch tool failed due to a deployment issue. Let me try a web search instead to get information about the Foundation Capital essay.

**Action** (what was decided):
> let me try a web search instead to get information about the foundation capital essay.

**Associated Tools**: `Bash, WebSearch, WebFetch`

---

### Trace #3: SEQUENCING

**Timestamp**: `2025-12-27T17:56:08.997Z`

**Summary**:
> Ah right, we're already on that branch. I need to switch back to main first, then create the work...

**Context** (what triggered this):
> Ah right, we're already on that branch. I need to switch back to main first, then create the worktree.

**Action** (what was decided):
> i need to switch back to main first, then create the worktree.

**Associated Tools**: `Bash, Read, TodoWrite, Write, WebSearch`

---

### Trace #4: GENERAL

**Timestamp**: `2025-12-27T17:56:14.591Z`

**Summary**:
> The hook is warning about uncommitted changes, but these are just untracked files (.DS_Store and ...

**Context** (what triggered this):
> The hook is warning about uncommitted changes, but these are just untracked files (.DS_Store and .vscode/) - not actually uncommitted changes to tracked files. These are safe to leave. Let me use `git...

**Reasoning** (why this choice):
> since these are untracked files that won't be lost.

**Action** (what was decided):
> let me use `git switch` instead which is safer, or just force the checkout since these are untracked files that won't be lost.

**Associated Tools**: `Bash, Read, TodoWrite, Write, WebSearch`

---

### Trace #5: CLARIFICATION

**Timestamp**: `2025-12-27T18:22:07.221Z`

**Summary**:
> The user wants to see the outputs from our prototypes. Let me show them how to run each script an...

**Context** (what triggered this):
> The user wants to see the outputs from our prototypes. Let me show them how to run each script and view the results.

**Action** (what was decided):
> let me show them how to run each script and view the results.

**Associated Tools**: `Bash`

---

### Trace #6: GENERAL

**Timestamp**: `2025-12-27T18:22:18.360Z`

**Summary**:
> Let me also show the projection function output more clearly.

**Action** (what was decided):
> let me also show the projection function output more clearly.

**Associated Tools**: `Bash`

---

### Trace #7: GENERAL

**Timestamp**: `2025-12-27T18:22:23.946Z`

**Summary**:
> Good, the user can now see the outputs. Let me provide a summary of the different ways to view ou...

**Context** (what triggered this):
> Good, the user can now see the outputs. Let me provide a summary of the different ways to view outputs.

**Action** (what was decided):
> let me provide a summary of the different ways to view outputs.

**Associated Tools**: `Bash`

---

### Trace #8: CLARIFICATION

**Timestamp**: `2025-12-27T18:33:07.615Z`

**Summary**:
> Great point! The user wants me to store the outputs as markdown documents so they can view them d...

**Context** (what triggered this):
> Great point! The user wants me to store the outputs as markdown documents so they can view them directly in the repo rather than running commands. Let me generate the outputs and save them as markdown...

**Action** (what was decided):
> let me generate the outputs and save them as markdown files in the context-graphs experiment.

**Associated Tools**: `Bash`

---

### Trace #9: GENERAL

**Timestamp**: `2025-12-27T18:33:12.371Z`

**Summary**:
> Now let me generate each output and save as markdown files.

**Action** (what was decided):
> let me generate each output and save as markdown files.

**Associated Tools**: `Bash`

---

### Trace #10: PLANNING

**Timestamp**: `2025-12-27T18:33:34.972Z`

**Summary**:
> Good, now let me create the projection function output as a markdown file too.

**Action** (what was decided):
> let me create the projection function output as a markdown file too.

**Associated Tools**: `Bash`

---

## Decision Type Taxonomy


| Type | Description | Example Pattern |
|------|-------------|-----------------|
| `planning` | Task decomposition, setup | "Let me break down...", "First I'll..." |
| `sequencing` | Ordering operations | "Before X, I need to Y" |
| `recovery` | Error handling | "Failed, let me try...", "The error was..." |
| `clarification` | Understanding intent | "The user wants...", "This means..." |
| `context_awareness` | State recognition | "We're already on...", "Currently..." |
| `general` | Other decisions | (Catch-all for unclassified) |

## How These Are Extracted


1. **Parse JSONL**: Each line is a message in the session
2. **Find thinking blocks**: Look for `{"type": "thinking", "thinking": "..."}`
3. **Classify**: Match patterns in the text to decision types
4. **Associate tools**: Find tool calls within ~60 seconds of the thinking
5. **Extract structure**: Pull out context, reasoning, and action

