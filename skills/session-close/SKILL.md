---
name: session-close
description: "Close a substantive Codex session by coordinating an evidence-based retrospective and a verified project handoff, including recommendations for stale or incomplete AGENTS.md and project-instruction contracts. Save approved-state summaries locally while keeping all improvement proposals pending until the user explicitly approves them. Use when the user invokes $session-close, wants to end a long project session, or asks to save handoff and retrospective results for the next session."
---

# Session Close

## Purpose

Coordinate the installed session-handoff and agent-retrospective skills at the end of a
substantive session. Save a compact, source-grounded handoff for the next session and a
private retrospective with 1–3 bounded improvement proposals. Keep every proposal advisory
until the user explicitly approves it.

This skill is an explicit close operation. It may persist the local handoff and retrospective
when invoked, but it must not commit, push, merge, delete, change repository settings, or
implement retrospective proposals unless the user separately authorizes that action.

## Companion skills and order

Read and follow both companion skills completely before acting:

- the skill named session-handoff;
- the skill named agent-retrospective.

This repository bundles both companion skills. When the three skill directories are installed
together, they provide the complete close workflow. If session-close is installed by itself,
the two companion skills must still be available through the active Codex skill catalog or
configured skill root. Never hardcode a username, machine path, or project path to locate them.

Run the retrospective reasoning first and finalize the handoff second. This lets the handoff
list the retrospective proposal IDs that remain pending approval.

## Close workflow

### 1. Establish the review window and scope

- Treat the relevant window as the current Codex session since the last explicit handoff,
  unless the user names a narrower segment.
- Read the nearest project AGENTS.md and the project's configured handoff file, if one
  exists. Common names include docs/HANDOVER.md and HANDOVER.md, but do not assume a
  project-specific path without checking the project guidance.
- Treat the existing handoff as a hypothesis until current repository and GitHub state
  confirm it.
- Preserve unrelated user changes. If the handoff file already contains unrelated or
  ambiguous edits, stop and ask before overwriting them.

### 2. Verify current state

Use the smallest useful read-only checks for the project:

- current branch, working-tree status, current commit, recent relevant commits;
- worktrees and local/remote branch state when cleanup or branch facts matter;
- relevant tests or validation results, without rerunning expensive checks unnecessarily;
- GitHub issue, PR, check, merge, branch, and secret-existence state when external effects
  occurred. Never print secret values.

Record observed external effects explicitly: commits, pushes, merges, issue/PR changes,
branch/worktree deletion, permissions, deployments, and API usage or cost observations.
Separate verified facts from inference, decisions, risks, and next actions.

Review AGENTS.md and other active project instruction files as contracts, not as unquestioned
truth. Look for evidence-backed instruction debt:

- stale branch, PR, tool, model, path, or validation claims;
- contradictory rules or duplicated policy with different precedence;
- missing scope, approval, testing, secret, cost, or external-write boundaries;
- instructions that require an impossible, unobservable, or unsafe completion check;
- project behavior that has changed but the instruction contract has not recorded.

Do not “fix” instruction debt during verification. Turn it into a retrospective proposal only
when the evidence shows a concrete maintenance benefit.

### 3. Produce the retrospective

Apply agent-retrospective to the defined review window. Save only a structured summary,
never raw transcripts, JSONL, credentials, cookies, or sensitive command output.

Save the full retrospective privately under the current user's configured Codex data
directory, normally CODEX_HOME/agent-retrospectives:

~~~
<CODEX_HOME>/agent-retrospectives/YYYY-MM-DD-HHmm-<project>-retrospective.md
~~~

If CODEX_HOME is unset, use the Codex installation's configured per-user data directory.
Resolve the actual path from the current environment; never hardcode a username. Use a
timestamp or collision-safe suffix so a later close does not overwrite an earlier session
review. Include:

- Outcome
- Major timeline and pivots
- What worked
- Friction and waste
- Root causes
- 1–3 action items
- Unresolved risks

Each action item must have a stable ID and these fields:

~~~
ID: RETRO-YYYYMMDD-NN
Status: PENDING APPROVAL
Target artifact:
Target section:
Recommendation:
Evidence:
Bounded scope:
Trigger or owner:
Success signal:
~~~

For an AGENTS.md or project-instruction proposal, Target artifact must name the exact file
and Target section must identify the relevant heading or rule. State the smallest proposed
contract change and its compatibility or behavior impact. Do not turn a general preference
into a policy recommendation.

Do not convert a recommendation into an implemented change while producing the retrospective.

### 4. Finalize the project handoff

Apply session-handoff and update the project's configured handoff file only when it exists
or the user explicitly names a project handoff path. Keep the current section compact and
use these headings:

- Current state
- Goal and scope
- Changed and verified
- Decisions and assumptions
- Risks and blockers
- Next first action
- Pending retrospective proposals

The pending section should contain only the proposal IDs, one-line recommendations, status,
and a pointer to the private retrospective. Do not copy the full retrospective into the
project document.

Keep historical detail in Git history or the private retrospective instead of endlessly
appending session logs to the current handoff.

### 5. Avoid self-invalidating handoff facts

Do not put the handoff commit's own HEAD SHA or statements such as “this document is
uncommitted” or “this will be pushed” into the current handoff. The handoff commit changes
those facts immediately.

Prefer:

- “main was verified clean and synchronized with origin/main at close time”;
- the last functional or product commit when that is useful;
- executable verification commands such as git fetch origin --prune and
  git rev-parse HEAD origin/main;
- a separate statement of whether this close was local-only or explicitly published.

If an exact SHA is necessary, describe it as the last verified functional change rather than
the metadata commit that stores the handoff.

### 6. Validate and report

Before reporting completion:

- review the handoff diff for stale self-references, secrets, unrelated edits, and incorrect
  claims;
- run git diff --check and any proportionate documentation or project validation;
- verify the final local status. If the user explicitly requested commit/push, verify the
  remote ref afterward; otherwise leave Git state untouched beyond the requested handoff edit;
- report whether files were changed, where the private retrospective was saved, pending
  proposal IDs, validation results, and any approval still needed.

Do not claim a clean tree if the handoff itself is intentionally uncommitted. Do not claim a
remote push or merge without verifying it.

## Approval gate for retrospective proposals

Pending proposals are advisory and must not silently alter code, prompts, skills, workflows,
settings, or project policy.

On a later session:

1. Read the current handoff and the referenced private retrospective.
2. Show pending proposal IDs and their bounded scope before starting unrelated work.
3. Treat “approve RETRO-ID” as approval to prepare the bounded change.
4. Treat “approve RETRO-ID apply” as approval to implement that bounded change, subject to the
   project's normal Issue/PR, testing, and external-write rules.
5. Mark the proposal APPROVED, then IMPLEMENTED only after the change is actually made, and
   VERIFIED only after its success signal is observed.
6. Keep rejected or deferred proposals visible as REJECTED or DEFERRED with a short reason.

For proposals targeting AGENTS.md or another instruction contract:

- approval alone does not edit the file;
- prepare a minimal diff limited to the named target section and show its effect on future
  agent behavior;
- apply it only after the user explicitly requests the bounded implementation;
- validate that the new rule does not contradict closer project guidance, higher-priority
  instructions, or existing approval and safety boundaries;
- record the resulting commit or local-only change as evidence in the next handoff.

Approval of a retrospective recommendation does not by itself authorize unrelated scope,
secret handling, production actions, commit/push, or merge operations.

## User-facing close modes

Interpret explicit requests as follows:

- $session-close or “save session close”: run the full retrospective and local handoff flow;
  do not commit or push.
- “report the session close results only”: produce the reports in the response without persisting
  project files.
- “commit/push after session close”: persist, validate, then commit and push only the intended
  handoff change; do not create a PR unless separately requested.

If no project handoff file exists, save the private retrospective and report that no project
handoff was created rather than inventing a project-specific convention.

## Safety boundaries

- Never include API keys, tokens, cookies, raw transcripts, or full sensitive logs.
- Never apply retrospective recommendations automatically.
- Never stage unrelated user changes.
- Never use the close operation to conceal failing tests, unresolved review comments, dirty
  worktrees, or unverified external effects.
- Keep the handoff factual and short; preserve uncertainty instead of filling gaps with guesses.
