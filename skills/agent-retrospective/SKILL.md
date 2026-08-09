---
name: agent-retrospective
description: "Review an agent session for outcome quality, process friction, cost, safety, and actionable improvements. Use after a substantive multi-step session or when the user explicitly asks for an agent/session retrospective; invoke explicitly rather than automatically."
---

# Agent Retrospective

## Overview

Analyze how the work was performed, not only what was produced. Use evidence from the
conversation and current systems to identify avoidable loops, scope drift, unsafe assumptions,
wasted model/tool usage, and concrete operating changes without blaming people or inventing
certainty.

## Workflow

1. Define the review window and objective. Include the whole relevant session or the user-named
   segment; do not silently broaden the scope.

2. Gather evidence without rereading or exporting raw private transcripts:
   - user goals and changes in direction;
   - tool calls, retries, review loops, validations, and external side effects visible in the
     session;
   - current repository/GitHub state when it confirms mutable facts;
   - usage or cost figures supplied by the user, clearly labeled as user-provided.

   Use the evidence-status vocabulary defined by `session-handoff`. In particular, mark
   timeline evidence as `UNAVAILABLE` when context compaction or an inaccessible source removes
   it from the current review window. Do not reconstruct missing history from repository state,
   handoff text, or plausible inference alone.

3. Separate facts from inference. For each material finding, identify the evidence, the
   operational impact, and the likely system/process cause. Avoid attributing intent or judging a
   person.

4. Review these lenses:
   - outcome and definition of done;
   - goal changes and scope drift;
   - unnecessary model calls, duplicate reviews, retries, and waiting;
   - validation strength and missed evidence;
   - external side effects and approval boundaries;
   - secrets/privacy and cost/usage exposure;
   - what reduced risk or made the work efficient.

5. Produce a concise report:
   - **Outcome** — completed, incomplete, or blocked, with evidence;
   - **Timeline** — only the major phases and pivots;
   - **What worked** — practices worth preserving;
   - **Friction and waste** — observable issues and impact;
   - **Root causes** — process or system causes, not personal blame;
   - **Action items** — zero to three bounded changes with owner/trigger and success signal;
   - **Unresolved risks** — items needing a future decision.

## Persistence and safety

- This is an advisory process review. Do not modify repositories, issues, pull requests,
  workflows, settings, branches, or deployments as part of the retrospective.
- If the user explicitly asks to save the retrospective, write only a structured summary to a
  private local location such as `<CODEX_HOME>/agent-retrospectives/YYYY-MM-DD-agent-retrospective.md`.
  When `CODEX_HOME` is unset, use the platform's configured per-user Codex data directory.
  Resolve and verify the actual destination before claiming that persistence succeeded. If it
  cannot be resolved or written, report persistence as `UNAVAILABLE` and do not create a
  misleading reference for a shared handoff.
- Redact tokens, credentials, cookies, personal data, and sensitive command output. Project names,
  commit IDs, and ordinary paths may be retained when the destination is private and they help
  reproduce the finding.
- Do not turn a retrospective recommendation into an implementation or policy change without a
  separate user request.

## Quality bar

A good retrospective produces fewer, better operating changes. Do not invent an action item when
the evidence supports none; record that no actionable improvement was found. Prefer a small number
of evidence-backed actions over generic advice, and state uncertainty whenever the session does
not establish a fact.
