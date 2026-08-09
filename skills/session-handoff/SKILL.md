---
name: session-handoff
description: "Create a concise, source-grounded checkpoint for continuing work after a long session, context compaction, or task handoff, and update reproduction guidance only when continuation details materially changed. Use when the user asks for a handover, checkpoint, status snapshot, continuation note, or reproducible continuation guide; invoke explicitly rather than automatically."
---

# Session Handoff

## Overview

Capture verified project state, decisions, risks, and one executable next action so another
session can continue without reconstructing the conversation. Prefer current repository and
GitHub state over stale notes or remembered intent.

## Artifact discovery

Establish the active project root from the workspace and nearest applicable guidance. Do not let
a nested Git repository silently replace a parent project root when the work spans both.

Resolve the handoff through this precedence:

1. a path explicitly named in the current user request;
2. a path explicitly named by the nearest applicable project guidance;
3. repository convention, preferring `HANDOVER.md` over `docs/HANDOVER.md`;
4. `HANDOVER.md` at the active project root.

If candidates tie, stop and report the ambiguity. If the active root is unavailable, report the
artifact path as `UNAVAILABLE` and ask for an explicit path. Preserve unrelated or ambiguous
edits instead of overwriting them.

Resolve an explicitly named reproduction path through the same precedence; otherwise use
`REPRO.md` beside the selected handoff as its candidate path. Path resolution alone does not
require creating or updating the reproduction record.

## Evidence status

- `VERIFIED` — directly observed through the current context or a successful check;
- `FAILED` — attempted and failed;
- `NOT RUN` — known but intentionally not executed;
- `UNAVAILABLE` — required evidence cannot currently be accessed;
- `UNVERIFIED` — a claim or artifact exists but cannot be confirmed.

Do not reconstruct missing history from repository state. Separate facts, assumptions, open
decisions, risks, and next actions.

## Workflow

1. Read applicable guidance and existing selected artifacts, treating old content as a hypothesis.
2. In one evidence pass, inspect branch, working-tree status, current commit, relevant changes,
   and applicable validation already visible in the session.
3. Check GitHub, branches, worktrees, deployments, or other external state only when the session
   changed that state or the result is material to continuation.
4. Reuse a visible successful validation result when its command, outcome, and unchanged relevant
   state are established. Do not rerun product tests solely because handoff documentation changed.
5. Create or update the handoff with:
   - **Current state**
   - **Goal and scope**
   - **Changed and verified**
   - **Decisions and assumptions**
   - **Risks and blockers**
   - **Next first action**

Create or update the reproduction record only when environment, start/stop instructions,
reproduction steps, expected outputs, validation commands, or known failures materially changed,
or when the user explicitly requests it. Otherwise leave an existing record unchanged and do not
create an empty one. When triggered, use:

- **Environment and prerequisites**
- **Start and stop**
- **Reproduction steps**
- **Expected outputs**
- **Validation commands and results**
- **Known failures and limitations**

## Persistence and safety

- Default to a report in the response. Persist artifacts only when the user explicitly asks or
  when `session-close` invokes this capability under its persistence contract.
- Do not commit, push, merge, delete branches, change settings, or modify unrelated files without
  separate authorization.
- Never include tokens, credentials, cookies, transcripts, or sensitive logs.
- Review only changed artifact diffs and run proportionate validation before reporting success.
- Report whether the reproduction record was changed or intentionally omitted.

A useful handoff is short, factual, and immediately actionable. Preserve uncertainty rather than
filling gaps with plausible details.
