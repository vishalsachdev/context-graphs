# Projection Function Demo

**Generated**: 2025-12-27 12:33

---

## Concept

The projection function implements Venkatraman's key insight:

```
projection_function(datagraph, moment_context) → context_graph
```

Given accumulated decision traces (the datagraph) and a current situation,
it returns the **relevant subset** of knowledge for THIS moment.

## Building the Datagraph

| Metric | Value |
|--------|-------|
| Sessions indexed | 12 |
| Total traces | 270 |
| Keywords indexed | 624 |
| Recovery patterns | 60 |
| Tools indexed | 13 |

### Decision Types in Datagraph

| Type | Count |
|------|-------|
| clarification | 17 |
| recovery | 60 |
| sequencing | 37 |
| general | 124 |
| planning | 28 |
| context_awareness | 4 |

---

## Demo Scenarios

The following scenarios show what context the projection function returns for different tasks.

### Scenario 1: Creating a Git Branch

**Task**: I need to create a new git branch and set up a worktree
**Tools considered**: Bash

#### Projected Context

**Similar Past Decisions:**

1. `[general]` Now I need to create the TRASH-FILES.md to document what was moved....
2. `[general]` The CLOUDFLARE_API_TOKEN is not set in the environment. I could create a script ...
3. `[planning]` Now let me create the structure. I'll organize them in a `notebooks/` directory ...

**Applicable Patterns:**

- Planning approach: Now let me create the structure. I'll organize them...
- Planning approach: Now let me create the individual notebooks. I'll st...
- Planning approach: Now let me create the individual notebooks. I'll cr...

**Suggested Tools**: Read, Edit, TodoWrite

**Relevance Score**: 1.00

---

### Scenario 2: Handling a Build Error

**Task**: The build is failing with a TypeScript error
**Error**: `TypeScript compilation failed`
**Tools considered**: Bash, Read

#### Projected Context

**Similar Past Decisions:**

1. `[recovery]` The error is clear:...
2. `[general]` Perfect! TypeScript compiles successfully. Now let me also optimize the SubmitPr...
3. `[planning]` Excellent! The build succeeded. I can see:...

**Applicable Patterns:**

- Planning approach: Excellent! The build succeeded. I can see:...

**Suggested Tools**: Read, Edit, TodoWrite, Bash

**Relevance Score**: 1.00

---

### Scenario 3: Committing Changes

**Task**: I want to commit my changes
**Tools considered**: Bash

#### Projected Context

**Similar Past Decisions:**

1. `[general]` Perfect! The changes look good. Let me now show the user a summary and commit....
2. `[general]` Great! The user confirmed they want to commit both CLAUDE.md and AGENTS.md. Let ...
3. `[general]` The changes aren't committed yet. I need to commit and push them. Let me do that...

**Suggested Tools**: Read, Edit, TodoWrite

**Relevance Score**: 1.00

---

### Scenario 4: Debugging API Issue

**Task**: The API endpoint is returning 404 errors
**Error**: `404 Not Found`
**Tools considered**: Read, Grep

#### Projected Context

**Similar Past Decisions:**

1. `[recovery]` Aha! Found the issue!...
2. `[recovery]` The user is providing the Cloudflare API endpoint for purging cache for their sp...
3. `[recovery]` The user is showing console errors from the deployed site. Let me analyze these:...

**Applicable Patterns:**

- Past recovery: let me re-read the user's message....
- Sequencing: The user wants to work on the screenshot for social previe...

**Suggested Tools**: Bash, Edit, Grep, Read

**Relevance Score**: 1.00

---

### Scenario 5: Writing Tests

**Task**: I need to write unit tests for this function
**Tools considered**: Write, Bash

#### Projected Context

**Similar Past Decisions:**

1. `[planning]` I need to write a Playwright script to take a screenshot of the live site. Since...
2. `[sequencing]` Now I need to wait a moment for GitHub Pages to deploy, then capture a new scree...
3. `[general]` Good, the commit is done. Now I need to push to main....

**Applicable Patterns:**

- Planning approach: I need to write a Playwright script to take a scree...
- Sequencing: Now I need to wait a moment for GitHub Pages to deploy, th...

**Suggested Tools**: Bash, Task, TaskOutput, Read

**Relevance Score**: 1.00

---

## How This Works


1. **Keyword extraction**: Parse the current task for meaningful keywords
2. **Index lookup**: Find traces in the datagraph that share keywords
3. **Error matching**: If handling an error, prioritize recovery precedents
4. **Tool co-occurrence**: Suggest tools that commonly appear together
5. **Pattern extraction**: Pull sequencing/planning patterns from precedents
6. **Relevance scoring**: Score based on number of matching precedents

## Strategic Insight


> **Who controls the projection function controls what the AI can consider.**

The projection function is the chokepoint where:
- Accumulated learning (datagraph) meets current context
- Historical patterns become actionable suggestions
- Implicit knowledge becomes explicit guidance

This is the "operationalized learning" that Venkatraman describes.

