# Cross-Session Decision Pattern Analysis

**Generated**: 2025-12-27 12:33

---

## Sample Overview

- **Sessions analyzed**: 11
- **Projects**: review, api, tldw, latte, illinihunt, genart

- **Total decision traces**: 261

## Sessions Analyzed

| Project | Traces | Session ID |
|---------|--------|------------|
| review | 34 | `34d83fcb-3b3a-4983-8...` |
| review | 101 | `5158ac0f-9aef-4a32-a...` |
| api | 13 | `c3d25df5-d852-49f8-9...` |
| illinihunt | 17 | `932d1e2f-4394-460d-8...` |
| genart | 96 | `6ffea42a-1581-48d4-b...` |

## Decision Type Distribution

| Type | Count | % | Visual |
|------|-------|---|--------|
| general | 114 | 43.7% | ██████████████ |
| sequencing | 53 | 20.3% | ██████ |
| recovery | 40 | 15.3% | █████ |
| planning | 29 | 11.1% | ███ |
| clarification | 22 | 8.4% | ██ |
| context_awareness | 3 | 1.1% |  |

## Tool Usage

| Tool | Times Used |
|------|------------|
| Bash | 999 |
| Edit | 359 |
| Read | 178 |
| Write | 174 |
| Task | 127 |
| TodoWrite | 118 |
| TaskOutput | 84 |
| Glob | 68 |
| Grep | 37 |
| Skill | 35 |
| WebFetch | 28 |
| AskUserQuestion | 23 |

## Recovery Patterns (Error Handling)

These are decisions made when something went wrong:

### Recovery #1
- **Summary**: The git status is clean (no output before ---BRANCH---). Now let me provide the session summary b...
- **Context**: The git status is clean (no output before ---BRANCH---). Now let me provide the ...
- **Action**: let me provide the session summary based on the claude....

### Recovery #2
- **Summary**: I can see the issue - in `constellations.js` line 386, the article stars have a glow sprite with ...
- **Context**: I can see the issue - in `constellations.js` line 386, the article stars have a ...
- **Action**: let me look at the `createglowsprite` function to understand how to tone down th...

### Recovery #3
- **Summary**: The user is reporting a bug where the commit count changes between when the guided tour dialog is...
- **Context**: The user is reporting a bug where the commit count changes between when the guid...
- **Action**: let me re-read the user's message....

### Recovery #4
- **Summary**: I see the issue now. Looking at the screenshot:
- **Context**: I see the issue now. Looking at the screenshot:...
- **Action**: let me re-read their message....

### Recovery #5
- **Summary**: The scripts are loaded synchronously in order:1. data.js
- **Context**: The scripts are loaded synchronously in order:1. data.js...
- **Action**: let me check if maybe articles....

### Recovery #6
- **Summary**: Let me manually count the commits from data.js:
- **Context**: Let me manually count the commits from data.js:...
- **Action**: let me manually count the commits from data....

### Recovery #7
- **Summary**: The tour.js doesn't call updateStats at all. So that's not the issue.
- **Context**: Wait, looking at the user's screenshots again - they both appear identical with ...
- **Action**: let me check if the animatenumber function might be causing a visual glitch wher...

### Recovery #8
- **Summary**: The user confirmed the hard refresh fixed the issue and now wants to close shop. I should use the...
- **Context**: The user confirmed the hard refresh fixed the issue and now wants to close shop....
- **Action**: i should use the close-shop skill to wrap up the session properly....

## Strategic Insights

1. **Primary decision mode**: `general` (114 instances)
2. **Recovery rate**: 15.3% of decisions handle errors
3. **Core tool vocabulary**: Bash, Edit, Read
