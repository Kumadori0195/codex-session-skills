---
name: session-handoff
description: "Create a concise, source-grounded checkpoint and reproduction record for continuing work after a long session, context compaction, or task handoff. Use when the user asks for a handover, checkpoint, status snapshot, or continuation note; invoke explicitly rather than automatically."
---

# Session Handoff

## Overview

Capture the verified project state, decisions, evidence, risks, and first next action so
another session can continue without reconstructing the entire conversation. Prefer current
repository and GitHub state over stale notes or remembered intent.

## Active project root

Use the project root established by the current workspace and nearest applicable project
guidance. A nested Git repository does not silently replace the workspace project root when the
task spans parent-level scripts, assets, or configuration. If multiple roots are equally
plausible, mark the artifact paths `UNAVAILABLE` and ask for an explicit path.

## Handoff discovery

Resolve the project handoff through this precedence order:

1. A path explicitly named in the current user request;
2. a path explicitly named by the nearest applicable `AGENTS.md` or project instruction file;
3. repository conventions, with `HANDOVER.md` preferred over `docs/HANDOVER.md`;
4. the documented default `HANDOVER.md` at the active project root when no candidate exists.

Do not scan arbitrary filenames or select a candidate by modification time. The default path is
an explicit project convention, not a guess based on file age. If multiple paths are supplied at
the same precedence without a documented tie-breaker, stop and report the ambiguity without
updating either project artifact. If the active project root cannot be resolved, mark the path
`UNAVAILABLE` and ask for an explicit project handoff path instead of writing elsewhere.

Record the selected path and the precedence source in the close result. Preserve unrelated or
ambiguous edits in an existing candidate instead of overwriting them.

## Companion reproduction record

Every selected project handoff has a companion reproduction record. Resolve it through the same
precedence order when a `REPRO.md` path is explicitly named; otherwise use `REPRO.md` beside the
selected handoff. When the default handoff is created, create the default `REPRO.md` beside it
at the same time. Report both selected paths and their precedence sources in the close result.

The reproduction record is a compact, executable continuation guide with these headings:

- **Environment and prerequisites** — required tools, versions, services, and local assets;
- **Start and stop** — commands or UI actions to bring the project into the required state;
- **Reproduction steps** — the smallest ordered procedure for the current behavior;
- **Expected outputs** — files, responses, screenshots, or other observable success signals;
- **Validation commands and results** — checks with their evidence status;
- **Known failures and limitations** — blockers, unavailable evidence, and unsafe assumptions.

## Evidence status

Use these statuses for every material claim or check:

- `VERIFIED` — directly observed through the current context or a successful check;
- `FAILED` — the check was attempted and failed;
- `NOT RUN` — the check was known but intentionally not executed;
- `UNAVAILABLE` — required evidence cannot currently be accessed, such as after context
  compaction, an unavailable service, or an unreadable private record;
- `UNVERIFIED` — a claim or artifact exists but cannot be confirmed from the available evidence.

Do not use `UNAVAILABLE` and `UNVERIFIED` interchangeably. After context compaction, use only
the current accessible context and newly verified external state. Never reconstruct a missing
conversation timeline from repository state alone. A handoff may be partial when evidence is
unavailable, but unsupported claims must remain marked as such.

## Workflow

1. Establish scope. Read the nearest applicable `AGENTS.md`; read the selected handoff and its
   companion reproduction record when they exist, but treat both as hypotheses until checked.

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

   Also produce or update the companion `REPRO.md` using the reproduction headings above. Keep
   it executable and source-grounded; do not copy raw transcripts or sensitive logs.

## Persistence and safety

- Default to a report in the response; do not edit project files, commit, push, merge, delete
  branches, or change settings unless the user explicitly asks.
- If the user explicitly asks to persist a handoff, use the selected project handoff and
  companion reproduction paths. When `session-close` is explicitly invoked and no candidate
  exists, create the documented default pair at the active project root. A private local report
  under the configured Codex data directory, normally `<CODEX_HOME>/agent-retrospectives/`, is
  separate from those project artifacts.
- If the configured private-report path cannot be resolved or written, report persistence as
  `UNAVAILABLE` and do not add a misleading private-file reference to a shared handoff.
- Never include tokens, credentials, cookies, raw session transcripts, or sensitive command
  output. Redact secrets while preserving the fact that a secret/configuration exists.
- If updating project handoff artifacts is requested, review both diffs and run the relevant
  validation before reporting completion. The artifacts themselves do not authorize a commit or
  push.

## Quality bar

A useful handoff lets a fresh session identify the real current state, avoid repeating completed
work, and take the next safe action in one pass. Keep it factual and short; preserve uncertainty
instead of filling gaps with plausible details.
