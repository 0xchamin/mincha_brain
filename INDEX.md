# Brain - INDEX (ask here)

> **This is the entry point.** To ask a question of the brain - at the repo root - **start here**:
> this catalog tells you which source or topic covers what, so you (or the agent) read the right
> notes instead of every file. It owns the **brain-wide** scope (all sources + all topics); each
> source's own map lives in its `SOURCE.md` "Reading order", and each topic's detail in
> `brain/topics/*.md`. Keep it a signal store, not a dump.
>
> **Auto-maintained.** This file is a **hard output** of ingest, compound, and close-loop - the
> agent rewrites the affected rows every time media is added, a claim is promoted, or the loop is
> closed. It is **not** hand-curated between those checkpoints.
>
> **Integrity rule (agent must uphold):** every `sources/<folder>/` has **exactly one** row in the
> Sources table below, and every `brain/topics/*.md` has **exactly one** row in the Topics table.
> If a source or topic exists on disk but not here, it is unfindable - add the row. If a row points
> to a folder that no longer exists, remove it.
>
> **Annotate every entry** with a one-line summary + "when to read" - a bare list forces a reader to
> open each link to judge relevance; annotating once does that upfront.
> (Principle from eugeneyan.com/writing/working-with-ai - the annotated INDEX, via `starter-kit`.)
> (No owner column - this is a single-person brain; everything here is yours.)

## Sources

| Source | Type | Summary | Topics | When to read | Folder |
|---|---|---|---|---|---|
| _(none yet)_ | - | Paste a URL (video / blog / paper / **GitHub repo**) to ingest your first source. | - | - | - |

## Topics (living notes)

The compounding synthesis layer - many sources feed each note. See [`brain/topics/`](brain/topics/).

> **Topics are open** - new ones are added as sources introduce a recognizable new area (the
> **architect** persona owns the create-vs-merge call). **Status** advances `seed` (created, no
> source yet) -> `emerging` (one source, needs-check) -> `established` (two or more corroborating
> sources). The six below are seeds, not a whitelist.

| Topic | Status | What it covers | Sources feeding it | Note |
|---|---|---|---|---|
| Agents | seed | Autonomous LLM agents: planning, tools, memory, loops | 0 | [`brain/topics/agents.md`](brain/topics/agents.md) |
| MCP | seed | Model Context Protocol: servers, tools, resources, transport | 0 | [`brain/topics/mcp.md`](brain/topics/mcp.md) |
| Skills | seed | Agent skills: definition, invocation, packaging | 0 | [`brain/topics/skills.md`](brain/topics/skills.md) |
| RAG | seed | Retrieval-augmented generation: chunking, embeddings, retrieval | 0 | [`brain/topics/rag.md`](brain/topics/rag.md) |
| Agent security | seed | Threats + mitigations: prompt injection, tool poisoning, exfiltration | 0 | [`brain/topics/agent-security.md`](brain/topics/agent-security.md) |
| Inferencing | seed | LLM serving: KV cache, batching, quantization, speculative decoding | 0 | [`brain/topics/inferencing.md`](brain/topics/inferencing.md) |

## Deeper layers (brain-wide content INDEX points into)

- [`brain/claims.md`](brain/claims.md) - cross-source **corroborated claims** with citations.
- [`brain/glossary.md`](brain/glossary.md) - 💡 **terms** defined once, reused across sources.
- [`brain/log.md`](brain/log.md) - dated **ingest milestones**.
- [`brain/decisions/`](brain/decisions/) - **ADRs** for durable structural decisions (architect persona).

## Config (taste + workflow)

- [`AGENTS.md`](AGENTS.md) - behavioral contract + the paste-a-URL ingest rule. Read every session.
- [`personas/README.md`](personas/README.md) - role overlays; auto-loaded per the routing table.
- [`prd.md`](prd.md) - the design + rationale.
