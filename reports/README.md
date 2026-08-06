# reports/ - generated study material

Synthesized, cross-source reports built by the **synthesizer** persona when you ask across the
brain. Markdown by default; self-contained HTML (visuals inline) on request. Each report cites
every claim (`source@timestamp` deep-links / `source, §/Figure N` / GitHub blob permalink with SHA
for code) and embeds the best corroborated visuals across sources. Any diagram the synthesizer
*generates* (rather than lifts from a source) is labelled **"synthesized"** and cites its underlying
nodes, so generated material is never mistaken for sourced evidence.

| Report | Built from | When to read |
|---|---|---|
| [`260725_agent-fundamentals-ramp-up.md`](260725_agent-fundamentals-ramp-up.md) | S2 (12-Factor Agents) + S1 (Uber closed-loop evals) | Onboarding an engineer onto agent work - the mental model, what to own, the four traps, and a first-week plan. Written mentor-voice; section 10 lists what to distrust. |
| [`mcp-shark-isolation-ceiling/`](mcp-shark-isolation-ceiling/) | claim 178 + the decision report below | **A handoff pack for another repo, and the first artifact here written to be *consumed by a coding agent* rather than read by a person.** [`background.md`](mcp-shark-isolation-ceiling/background.md) is self-contained context - threat model, defence landscape, the finding, and five hard constraints. [`spec.md`](mcp-shark-isolation-ceiling/spec.md) is the build, whose **Phase 1 is a blocking validation gate**, not a step. **Links are pinned to commit `638ebe9`** rather than `main`, because this repo's notes get rewritten and a spec must cite the sentence it was written against. |
| [`260805_isolation-ceiling-of-an-mcp-config.md`](260805_isolation-ceiling-of-an-mcp-config.md) | claims 149, 152, 153, 155, 166, 167, 173 + conjecture **h7** + R3 (AgentDyn) | **Deciding whether to build it**: a proposal to measure, statically, the fraction of an MCP config's tool surface on which no plan-time isolation defence can help. Written as a defensible position rather than a pitch - **§3 flags that one load-bearing step is a conjecture**, §6 names the survey most likely to have got there first, and §7 lists what would kill it. Read §8 for the two-step validation that tests the idea before any code. |
