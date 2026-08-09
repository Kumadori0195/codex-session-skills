---
name: session-close
description: "Close a substantive Codex session with one adaptive, evidence-based workflow that saves a verified project handoff, updates reproduction guidance only when it changed, and records a private retrospective only when actionable findings exist. Keep improvement proposals pending until the user explicitly approves them. Use when the user invokes $session-close, wants to end a long project session, or asks to save close results for the next session."
---

# Session Close

## Purpose

Close a substantive session through one adaptive workflow. Always leave a compact, verified
project handoff. Update reproduction guidance, run external checks, rerun validation, audit
instructions, and save a private retrospective only when current-session evidence triggers that
work. The user does not choose a mode.

This skill is self-contained for ordinary close operations. Do not load the bundled
`session-handoff` or `agent-retrospective` SKILL.md files during a normal close; they provide the
same capabilities when invoked independently. Load
[`references/approval-lifecycle.md`](references/approval-lifecycle.md) only when handling a later
approval, rejection, deferral, implementation, or verification of a RETRO proposal.

This is a prompt-driven workflow, not a runtime permission system, sandbox, or secret scanner.
It may persist the selected local close artifacts, but it must not commit, push, merge, delete,
change repository settings, or implement a retrospective proposal unless the user separately
authorizes that action.

## Core evidence contract

Use these statuses for material checks:

- `VERIFIED` — directly observed in the current context or through a successful check;
- `FAILED` — attempted and failed;
- `NOT RUN` — known but intentionally not executed;
- `UNAVAILABLE` — required evidence cannot currently be accessed;
- `UNVERIFIED` — a claim or artifact exists but cannot be confirmed.

Never infer an external effect or reconstruct missing conversation history from repository state.
Separate facts, inferences, decisions, risks, and next actions.

## Adaptive close workflow

### 1. Resolve scope and artifact paths

- Review the current session since the last explicit handoff unless the user names a narrower
  window.
- Establish the active project root from the workspace and nearest applicable guidance. A nested
  Git repository does not silently replace a parent project root when the work spans both.
- Resolve the handoff by this precedence: explicit user path, explicit project-guidance path,
  repository convention (`HANDOVER.md` before `docs/HANDOVER.md`), then `HANDOVER.md` at the active
  project root.
- Resolve an explicitly named reproduction path by the same precedence; otherwise use `REPRO.md`
  beside the handoff as its candidate path. Resolving the path does not require creating or
  updating it.
- Stop on tied candidates or unrelated or ambiguous edits in an artifact that would be changed.
  If the active project root is unavailable, report artifact persistence as `UNAVAILABLE` and ask
  for an explicit path.

Treat existing handoff and reproduction records as hypotheses until current evidence confirms
them.

### 2. Gather evidence once

In one read-only evidence pass, always inspect the smallest useful current state:

- branch, working-tree status, current commit, and relevant changed files;
- current-session validation commands and results that remain visible;
- the active project guidance already needed to interpret the work;
- observed external effects and unresolved risks.

Default to omission for every additional check. Run it only when the corresponding trigger is
visible in the current session:

- **Validation rerun:** the completion claim depends on a check that has no usable result, or
  relevant files changed after the last result. Reuse a visible successful result when the
  command, outcome, and unchanged relevant state are established. Handoff-only edits do not
  invalidate product validation.
- **GitHub or service check:** a push, PR, issue, merge, deployment, permission change, or other
  external effect occurred or its result is material to the handoff. Verify only the affected
  object.
- **Branch or worktree check:** branch or worktree creation, cleanup, deletion, synchronization,
  or an associated risk occurred.
- **Instruction audit:** project guidance caused friction, contradicted observed behavior, became
  stale because of this session, or omitted a boundary needed to complete the work. Do not run a
  broad AGENTS.md or policy audit merely because an instruction file exists.

Gather independent checks together when practical. Do not repeat a successful check unless later
changes invalidate it.

### 3. Decide conditional artifacts

Always create or update the selected handoff.

Create or update the reproduction record only when at least one trigger is present:

- environment or prerequisites changed;
- start or stop instructions changed;
- reproduction steps or expected outputs changed;
- validation commands changed;
- a new failure or limitation materially affects continuation;
- the user explicitly requested a reproduction record.

If an existing reproduction record remains valid, leave it unchanged. If none exists and no
trigger is present, do not create an empty one.

Create a private retrospective only when evidence supports at least one actionable finding:

- avoidable retry, loop, waiting, or duplicate work;
- incomplete outcome, material scope drift, or a significant pivot;
- validation gap or unsafe assumption;
- approval, privacy, external-effect, or cost concern;
- concrete instruction debt observed during the session;
- unresolved risk that benefits from a bounded future action.

If no trigger is present, do not create a private retrospective or RETRO ID. Record no pending
proposals in the handoff. Never invent a generic improvement to satisfy a quota.

### 4. Save a triggered retrospective

When triggered, write only a structured summary—never a transcript, JSONL, credential, cookie,
or sensitive command output—to the configured per-user Codex data directory, normally:

~~~text
<CODEX_HOME>/agent-retrospectives/YYYY-MM-DD-HHmm-<project>-retrospective.md
~~~

Resolve the actual directory from the environment. Use these headings:

- Outcome
- Major timeline and pivots
- What worked
- Friction and waste
- Root causes
- Action items
- Unresolved risks

Include zero to three action items. Each genuine proposal must contain:

~~~text
ID: RETRO-YYYYMMDD-HHmm-XXXX
Status: PENDING APPROVAL
Target artifact:
Target section:
Recommendation:
Evidence:
Bounded scope:
Trigger or owner:
Success signal:
~~~

Generate the four-character uppercase Crockford Base32 suffix from a secure random source when
available. Check the complete candidate ID with an exact-string search against existing private
records and the current handoff; regenerate only on collision. Never load old retrospectives into
model context merely to check identity.

For an instruction proposal, name the exact target file and section, the smallest contract
change, and its compatibility or behavior impact. Keep every proposal advisory. If private
persistence is unavailable, report `UNAVAILABLE` and do not add a misleading private reference
to the shared handoff.

### 5. Finalize the handoff

Write the compact current handoff with these headings:

- Current state
- Goal and scope
- Changed and verified
- Decisions and assumptions
- Risks and blockers
- Next first action
- Pending retrospective proposals

Use `None` for pending proposals when no proposal was created. Otherwise list only proposal IDs,
one-line recommendations, status, and a non-sensitive pointer to the private record. Do not put a
machine-specific absolute path, username, or full retrospective in a shared handoff.

When the reproduction record is triggered, use these headings:

- Environment and prerequisites
- Start and stop
- Reproduction steps
- Expected outputs
- Validation commands and results
- Known failures and limitations

Do not record facts invalidated by the close itself. Avoid the handoff commit's own SHA and future
claims such as “this will be pushed.” Prefer close-time state, the last functional change, and
commands that a later session can execute.

### 6. Validate and report

Use one write pass and one final validation pass. Additional passes are justified only by a
failure, contradiction, or intervening change.

- Review only changed close-artifact diffs for stale claims, secrets, unrelated edits, and
  incorrect statements.
- Run `git diff --check` and proportionate artifact validation. Do not rerun product tests solely
  because close documentation changed.
- Verify final local status. If commit or push was explicitly requested, verify the resulting
  commit and remote ref; otherwise leave Git state untouched beyond the requested artifacts.
- Report the handoff path, whether the reproduction record and retrospective were changed or
  omitted, proposal IDs, validation results, and remaining uncertainty or approval.

Do not claim a clean tree when close artifacts are intentionally uncommitted. Do not claim a
remote effect without observing it.

## Failure and safety behavior

- Preserve unrelated user changes; never stage them with close artifacts.
- On a failed or unavailable check, record `FAILED`, `UNAVAILABLE`, or `UNVERIFIED` and continue
  only with supported facts.
- When context compaction removed evidence, mark it `UNAVAILABLE`; do not reconstruct it.
- Omit or redact any value that may be a secret.
- Never apply a retrospective recommendation during close.
- Never use close to conceal failing tests, unresolved review comments, dirty worktrees, or
  unverified external effects.

## Request semantics

- `$session-close` or “save session close”: run this adaptive flow and persist only triggered
  local artifacts; do not commit or push.
- “report the session close results only”: report without persisting project files.
- “commit/push after session close”: persist and validate, then commit and push only intended
  close artifacts; do not create a PR unless separately requested.
