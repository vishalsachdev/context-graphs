# Framework Synthesis: Context Graphs

Comparing Foundation Capital (2025) vs Venkatraman/Govindarajan (2022) perspectives.

## The Two Frameworks

### Foundation Capital (Gupta/Garg, Dec 2025)
**Core thesis**: The next trillion-dollar platforms will be "systems of record for decisions, not just objects."

**The problem they identify**:
- Current systems of record (Salesforce, Workday, SAP) own canonical data about *objects*
- Missing: **decision traces** - the reasoning connecting data to action
- Examples of missing context:
  - Exception logic ("we always give healthcare companies 10% extra")
  - Approval chains (decisions made on Slack, not in CRM)
  - Tribal knowledge passed through onboarding

**Their solution**:
- Instrument agent orchestration layer to emit decision traces
- Build "context graphs" - living maps of relationships, history, and decisions
- Decision traces = business-level semantics on top of execution telemetry

**Key quote**:
> "Decision traces operate at a higher level of abstraction than execution traces—not 'the agent called this tool with these parameters' but 'this decision was made under this policy, with this exception, approved by this person, based on this precedent.'"

**Strategic frame**: Software competition (incumbents vs AI-native startups)

---

### Venkatraman (LinkedIn, Dec 2025) + Venkatraman/Govindarajan (HBR 2022)

**Source**: [Why Context Graphs Make Datagraphs Strategically Decisive](https://www.linkedin.com/pulse/why-context-graphs-make-datagraphs-strategically-venkat-venkatraman-xfdqf/)

**Core thesis**: Datagraphs create a new source of competitive advantage through data network effects. Context graphs are projections of datagraphs that operationalize learning in moments that matter.

**Their taxonomy**:
1. **Knowledge graphs** - semantic layer (what things mean)
   - Solve: Representing meaning at scale so machines understand entities/concepts
   - Examples: Google Knowledge Graph, Wikipedia/Wikidata

2. **Datagraphs** - learning layer (strategic)
   - Solve: Capturing product-in-use behavior so learning compounds
   - Examples: Facebook social graph, Netflix movie graph, Amazon purchase graph
   - Key mechanism: Data network effects (usage → learning → better outcomes → more usage)

3. **Context graphs** - action layer
   - Solve: Assembling the right slice of meaning + learning for human-machine coordination
   - Purpose: Operationalize learning in moments that matter

**Key insight**:
> Context graphs are "moment-specific projections of a much larger asset" - the datagraph.

**Strategic frame**: Broader business competition (any industry, not just software)

---

## Synthesis: Where They Agree

| Dimension | Foundation Capital | Venkatraman | Agreement |
|-----------|-------------------|-------------|-----------|
| Current gap | Decision reasoning not captured | Product-in-use behavior not captured | ✅ There's a missing data layer |
| Nature of gap | Decisions as first-class data | Behaviors as first-class data | ✅ It's about *actions*, not just *records* |
| Solution | Instrument for decision traces | Build datagraphs with network effects | ✅ Structured representation of activity |
| Who wins | Whoever captures decision context | Whoever compounds learning | ✅ Data moats, not model moats |

---

## Synthesis: Where They Diverge

### 1. Level of Abstraction

**Foundation Capital** operates at the **application layer**:
- Focus: Individual agentic workflows
- Scope: A specific enterprise tool (CRM, ERP)
- Time horizon: The current task/session

**Venkatraman** operates at the **platform layer**:
- Focus: Cross-workflow learning
- Scope: An entire business ecosystem
- Time horizon: Cumulative over years

**Implication**: Foundation Capital describes *how to build* context graphs. Venkatraman describes *why they matter strategically*.

### 2. The Projection Question

Venkatraman's insight that context graphs are "projections" of datagraphs raises a key question Foundation Capital doesn't address:

**What is the projection function?**

```
projection_function(datagraph, moment_context) → context_graph
```

The projection function must answer:
- What subset of the datagraph is relevant now?
- What relationships matter for this specific decision?
- What historical patterns should inform this moment?

**Hypothesis**: The projection function itself is a strategic asset. Whoever defines "relevance" shapes what the AI system can even consider.

### 3. Ownership & Lock-in

**Foundation Capital** implies lock-in through:
- Decision traces (hard to recreate)
- Agent orchestration (switching costs)
- Approval chain history (institutional memory)

**Venkatraman** implies lock-in through:
- Data network effects (compounding returns)
- Cross-system learning (broader scope = more value)
- Customer behavior patterns (harder to replicate than decision logic)

**Implication**: Foundation Capital describes *defensive* moats. Venkatraman describes *offensive* moats that actively compound.

---

## Unified Framework

Combining both perspectives:

```
┌─────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE LAYER                            │
│  Knowledge graphs: Entities, concepts, relationships            │
│  (Semantic grounding - what things mean)                        │
├─────────────────────────────────────────────────────────────────┤
│                      LEARNING LAYER                             │
│  Datagraphs: Product-in-use behavior + data network effects     │
│  (Strategic asset - compounds over time)                        │
│                                                                 │
│  Contains:                                                      │
│  - User behavior patterns                                       │
│  - Decision traces (Foundation Capital contribution)            │
│  - Exception logic and tribal knowledge                         │
│  - Approval chains and policy deviations                        │
├─────────────────────────────────────────────────────────────────┤
│                      ACTION LAYER                               │
│  Context graphs: Moment-specific projections                    │
│  (Operational - what matters right now)                         │
│                                                                 │
│  Assembled by:                                                  │
│  - Projection function (defines relevance)                      │
│  - Current user/task/constraints                                │
│  - Historical precedents                                        │
└─────────────────────────────────────────────────────────────────┘
```

**Key insight**: Foundation Capital's "decision traces" are a *specific type of data* that enriches the datagraph. They're not separate from it—they're the business-level semantic layer that makes the datagraph actionable for agentic systems.

---

## Strategic Implications

### For Incumbents (Salesforce, SAP, etc.)
- **Advantage**: Already have systems of record (object data)
- **Gap**: Missing decision traces and behavioral data
- **Strategy**: Instrument AI copilots to capture decision context
- **Risk**: If they only capture decisions *within* their tool, they miss cross-system learning

### For AI-Native Startups
- **Advantage**: Can design for decision traces from day one
- **Gap**: No existing customer relationships or data
- **Strategy**: Position as the "orchestration layer" that sits above systems of record
- **Risk**: Incumbents can add same capability and bundle it

### For Enterprises (Users of these tools)
- **Advantage**: Own the actual decision-making processes
- **Gap**: Decisions scattered across tools, Slack, email, meetings
- **Strategy**: Treat decision capture as strategic infrastructure, not just a vendor feature
- **Risk**: Vendor lock-in if decision traces are siloed

---

## Open Questions

1. **Technical**: What schema captures decision traces effectively? (JSON-LD? RDF? Custom?)

2. **Strategic**: Can a pure-play "context graph" company exist, or does it require owning the execution layer?

3. **Meta**: Claude Code session transcripts contain execution traces. What would it take to extract *decision* traces from them?

4. **Architectural**: Should the projection function be:
   - Hardcoded business rules?
   - Learned from data?
   - LLM-driven (ask the model what's relevant)?

---

## Next Steps

- [ ] Prototype a decision trace schema
- [ ] Analyze a Claude Code session transcript as a decision trace source
- [ ] Map specific enterprise workflows to this framework
