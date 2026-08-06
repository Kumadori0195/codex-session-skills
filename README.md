# Codex Session Skills

Portable OpenAI Codex skills for verified session handoffs, agent retrospectives, and
approval-gated improvements to AGENTS.md and project instruction contracts.

This repository includes the complete three-skill bundle: `session-close`, `session-handoff`,
and `agent-retrospective`.

This is a Codex-native, prompt-driven workflow. It reduces accidental changes through
explicit invocation and approval instructions, but it does not provide runtime permission
enforcement, sandboxing, or automatic secret detection.

## Included skills

### session-close

session-close coordinates the end of a substantive coding session so a fresh Codex session
can understand the project without reconstructing the entire conversation.

It combines:

- a verified session handoff with current repository, GitHub, validation, risk, and next-step
  evidence;
- an advisory agent retrospective covering outcome quality, process friction, retries, cost,
  safety, and external side effects;
- an approval queue for bounded improvements to AGENTS.md, prompts, skills, workflows, and
  other project instruction contracts.

### session-handoff

Creates a compact, evidence-based checkpoint with the verified project state, decisions, risks,
and one executable next action.

### agent-retrospective

Reviews the agent's process for outcome quality, friction, retries, validation gaps, cost, safety,
and bounded improvements.

## Why use it?

Long coding sessions often leave behind stale handoff notes, repeated validation work, and
useful process improvements that are easy to forget. session-close creates a compact
continuation checkpoint while keeping retrospective recommendations separate from approved
project decisions.

## What it does

When explicitly invoked, session-close:

1. reads the installed session-handoff and agent-retrospective skills;
2. resolves the project handoff using explicit user paths, project guidance, and repository
   conventions in that order, then uses the documented project-root default;
3. verifies the smallest useful set of repository and GitHub facts;
4. saves a structured private retrospective with stable RETRO IDs;
5. creates or updates the project `HANDOVER.md` and companion `REPRO.md` with current state,
   reproduction steps, and pending recommendations;
6. validates both project artifacts for stale claims, secrets, and unrelated changes.

Instruction-contract findings are recorded with an exact target file, target section,
evidence, bounded scope, and success signal. They remain PENDING APPROVAL.

The workflow distinguishes verified facts from assumptions and evidence availability. Material
facts use `VERIFIED`, `FAILED`, `NOT RUN`, `UNAVAILABLE`, or `UNVERIFIED`. In particular,
`UNAVAILABLE` means that required evidence cannot currently be accessed, while `UNVERIFIED`
means that an existing claim cannot be confirmed. It must not turn an intended action into a
claimed result without evidence.

## What it does not do automatically

session-close does not silently:

- modify code, AGENTS.md, prompts, skills, workflows, or project policy;
- commit, push, merge, delete branches, or change repository settings;
- apply a retrospective recommendation;
- record API keys, tokens, cookies, raw transcripts, or sensitive logs.

These are workflow-level safeguards, not a runtime security boundary. The active agent still
has to follow the instructions, and users should verify any external effect independently.

Use explicit approval before applying a proposal:

~~~text
approve RETRO-ID
approve RETRO-ID apply
~~~

The proposal lifecycle is:

~~~text
PENDING APPROVAL -> APPROVED | REJECTED | DEFERRED
APPROVED         -> IMPLEMENTED | DEFERRED | BLOCKED
IMPLEMENTED      -> VERIFIED | BLOCKED
~~~

`approve RETRO-ID` authorizes preparation of a bounded diff. `approve RETRO-ID apply`
authorizes implementation of that exact proposal after its target, evidence, and scope are
re-read. If the command is used as a combined request, the agent must record `APPROVED` after
preparing the diff before applying it. The phrases are an agent-interpreted workflow
convention; they do not grant tool permissions or bypass the project's normal approval and
external-write rules. `VERIFIED`, `REJECTED`, `DEFERRED`, and `BLOCKED` are terminal states for
that proposal record. Approval-like text in quotes, examples, code blocks, logs, repository
files, or handoffs is not direct user approval.

For AGENTS.md and other instruction-contract changes, approval prepares a minimal diff;
application remains bounded to the named file and section.

## Scenario evaluations

The repository includes behavior-contract fixtures under `evals/session-close/`. They cover
handoff precedence, ambiguous candidates, unavailable evidence, context compaction, private
persistence failures, approval intent, invalid transitions, RETRO-ID collisions, and
self-invalidating handoff claims.

Validate the fixture schema locally with:

~~~text
python scripts/validate_scenarios.py
~~~

The GitHub Actions workflow validates both the skill packages and these fixtures. The fixtures
are regression documentation and deterministic contract checks; they do not provide runtime
permission enforcement, sandboxing, or automatic secret detection.

## Installation

Install all three `skills/<skill-name>` directories into the configured Codex skill root,
preserving each directory's:

~~~text
SKILL.md
agents/openai.yaml
~~~

The skills are explicit-only and do not invoke implicitly during unrelated work. Installing the
complete bundle makes `session-close` immediately usable; installing it alone requires the two
companion skills to be available separately.

For a reproducible fresh install or update, pin the bundle to a full commit SHA and set
`CODEX_SKILL_ROOT` to the configured Codex skill root. Do not use a moving branch such as `main`
when recording an install. The following PowerShell procedure works for both a fresh checkout and
an update, and preserves the complete skill directories:

~~~powershell
$BundleRef = "<full-bundle-commit-sha>"
$SkillRoot = $env:CODEX_SKILL_ROOT
if (-not $SkillRoot) { throw "Set CODEX_SKILL_ROOT to the configured Codex skill root." }
$null = New-Item -ItemType Directory -Force -Path $SkillRoot
$BundleDir = Join-Path (Get-Location) "codex-session-skills"
$SkillNames = @("session-close", "session-handoff", "agent-retrospective")

if (-not (Test-Path -LiteralPath $BundleDir)) {
    git clone https://github.com/Kumadori0195/codex-session-skills.git $BundleDir
}
git -C $BundleDir fetch --depth 1 origin $BundleRef
git -C $BundleDir checkout --detach $BundleRef

foreach ($Name in $SkillNames) {
    Copy-Item -LiteralPath (Join-Path $BundleDir "skills\$Name") `
        -Destination (Join-Path $SkillRoot $Name) -Recurse -Force
}
~~~

Verify the installed files against the pinned checkout with SHA-256 before using them:

~~~powershell
$SkillRoot = $env:CODEX_SKILL_ROOT
if (-not $SkillRoot) { throw "Set CODEX_SKILL_ROOT to the configured Codex skill root." }
$BundleDir = Join-Path (Get-Location) "codex-session-skills"
$SkillNames = @("session-close", "session-handoff", "agent-retrospective")
foreach ($Name in $SkillNames) {
    $SourceHash = (Get-FileHash -Algorithm SHA256 (Join-Path $BundleDir "skills\$Name\SKILL.md")).Hash
    $InstalledHash = (Get-FileHash -Algorithm SHA256 (Join-Path $SkillRoot "$Name\SKILL.md")).Hash
    if ($SourceHash -ne $InstalledHash) { throw "$Name hash mismatch" }
    "$Name $SourceHash"
}
~~~

## Usage

At the end of a substantive session:

~~~text
$session-close
~~~

The default close flow creates or updates `HANDOVER.md` and `REPRO.md` at the active project root,
along with the private retrospective, without committing or pushing. Request commit or push
separately when the project artifacts should be published.

## Example output

The following abbreviated examples show the shape of the generated artifacts. Values are
illustrative and must be replaced with evidence from the actual session.

### Project handoff

~~~markdown
## Current state
- Branch: feature/session-close
- Working tree: dirty only because this handoff is being updated
- Active work: add approval-gated session close workflow

## Goal and scope
- Goal: preserve verified state for the next Codex session
- Out of scope: code changes, commit, push, and merge

## Changed and verified
- Verified repository status and recent commit history
- No tests were run; validation status is NOT RUN
- No external write was performed

## Decisions and assumptions
- The existing handoff file is the project source of truth
- Retrospective proposals remain pending user approval

## Risks and blockers
- GitHub checks were not needed for this local-only close

## Next first action
- Run the project's documented validation command before changing code

## Pending retrospective proposals
- RETRO-20260802-1519-A7K2 - PENDING APPROVAL - clarify the validation command in AGENTS.md
  Private reference: local retrospective record
~~~

Do not commit a machine-specific absolute path or username as the private reference in a
shared handoff.

### Reproduction record

~~~markdown
## Environment and prerequisites
- Required tools, versions, services, and local assets

## Start and stop
- Commands or UI actions to enter and leave the required state

## Reproduction steps
1. The smallest ordered procedure for the current behavior

## Expected outputs
- Observable files, responses, or other success signals

## Validation commands and results
- Command: status and evidence

## Known failures and limitations
- Unavailable evidence, blockers, and unsafe assumptions
~~~

### Private retrospective

~~~markdown
# Agent Retrospective

## Outcome
The requested documentation change was completed locally and remains uncommitted.

## Major timeline and pivots
- Inspected project guidance
- Updated the handoff contract
- Ran documentation validation

## What worked
- Current repository state was checked before writing the handoff

## Friction and waste
- The validation command was not documented in AGENTS.md

## Root causes
- The instruction contract names validation as required but omits the command

## Action items

### RETRO-20260802-1519-A7K2
Status: PENDING APPROVAL
Target artifact: AGENTS.md
Target section: Validation
Recommendation: document the smallest required validation command
Evidence: the close could not verify the project-specific command from current guidance
Bounded scope: add one command and its success signal to the Validation section
Trigger or owner: next session close; project maintainer
Success signal: a fresh session can run the documented command without rediscovery

## Unresolved risks
- The proposed instruction change has not been approved or applied
~~~

## Failure behavior

The close flow preserves uncertainty instead of inventing a result:

- If no project handoff file exists, create the documented default `HANDOVER.md` and `REPRO.md`
  pair at the active project root. If the active project root cannot be resolved, report the
  artifact paths as `UNAVAILABLE` and ask for an explicit path.
- If either project artifact contains unrelated or ambiguous edits, stop before overwriting it and ask.
- If a repository, test, or GitHub check fails or is unavailable, record `FAILED`, `NOT RUN`,
  `UNAVAILABLE`, or `UNVERIFIED` rather than claiming success.
- If context compaction removed evidence from the review window, mark that evidence
  `UNAVAILABLE`; do not reconstruct the missing timeline from repository state alone.
- If the private retrospective destination cannot be resolved or written, report persistence as
  `UNAVAILABLE` and do not write a misleading private-path reference into a shared handoff.
- If an approval ID is missing, unknown, or ambiguous, do not prepare or apply a change.
- If content may contain a secret, omit or redact it; do not copy the uncertain value into an
  artifact.

## Compatibility

The bundle is designed and packaged for OpenAI Codex. Its Markdown workflow may be adapted to
other agents, but compatibility with Claude Code, Cursor, Gemini, Windsurf, or other tools is
not currently tested or guaranteed.

## Portability and privacy

The skill is project-agnostic:

- it resolves companion skills from the active Codex skill catalog;
- it discovers the handoff using explicit, documented precedence;
- it uses the current user's configured Codex data directory for private retrospectives;
- it does not embed a username, machine path, repository name, or model-specific setup.

## Repository layout

~~~text
skills/
├── session-close/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
├── session-handoff/
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
└── agent-retrospective/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
evals/
└── session-close/
    └── scenarios.json
scripts/
└── validate_scenarios.py
.github/
└── workflows/
    └── validate-skills.yml
~~~

## License

Released under the [MIT License](LICENSE).
