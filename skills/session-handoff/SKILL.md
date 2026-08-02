---
name: session-handoff
description: "Create a concise, source-grounded checkpoint for continuing work after a long session, context compaction, or task handoff. Use when the user asks for a handover, checkpoint, status snapshot, or continuation note; invoke explicitly rather than automatically."
---

# Session Handoff

## Overview

Capture the verified project state, decisions, evidence, risks, and first next action so
another session can continue without reconstructing the entire conversation. Prefer current
repository and GitHub state over stale notes or remembered intent.

## Workflow

1. Establish scope. Read the nearest applicable `AGENTS.md`; if the project has a handover
   document such as `docs/HANDOVER.md`, read it but treat it as a hypothesis until checked.

2. Verify current state with the smallest useful set of read-only checks:
   - repository: branch, working-tree status, current commit, recent relevant commits, and
     applicable validation results;
   - GitHub: issue/PR/check/branch state only when the task involves GitHub or external effects;
   - project artifacts: inspect the files that define the active contract, not every file in the
     repository.

3. Record external side effects explicitly: commits, pushes, merges, issue/PR changes, branch
   deletion, permissions, or deployments. Never infer that an intended action happened; verify it.

4. Separate verified facts, assumptions/inferences, open decisions, risks/blockers, and next
   actions. Mark stale or unverified claims instead of silently carrying them forward.

5. Produce the following compact handoff:
   - **Current state** — branch/commit, clean or dirty status, and active work;
   - **Goal and scope** — what is being pursued and what is explicitly out of scope;
   - **Changed and verified** — files, tests, and external state with evidence;
   - **Decisions and assumptions** — include who/what still needs approval;
   - **Risks and blockers** — concrete impact and mitigation;
   - **Next first action** — one immediately executable step.

## Persistence and safety

- Default to a report in the response; do not edit project files, commit, push, merge, delete
  branches, or change settings unless the user explicitly asks.
- If the user explicitly asks to persist the result, prefer a private local report under the
  configured Codex data directory, normally `<CODEX_HOME>/agent-retrospectives/`, unless a
  project handover file is specifically named.
- Never include tokens, credentials, cookies, raw session transcripts, or sensitive command
  output. Redact secrets while preserving the fact that a secret/configuration exists.
- If updating a project handover file is requested, review the diff and run the relevant
  validation before reporting completion. The handover itself does not authorize a commit or
  push.

## Quality bar

A useful handoff lets a fresh session identify the real current state, avoid repeating completed
work, and take the next safe action in one pass. Keep it factual and short; preserve uncertainty
instead of filling gaps with plausible details.
