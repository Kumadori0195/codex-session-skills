# Codex Session Skills

Portable OpenAI Codex skills for verified session handoffs, agent retrospectives, and
approval-gated improvements to AGENTS.md and project instruction contracts.

## session-close

session-close coordinates the end of a substantive coding session so a fresh Codex session
can understand the project without reconstructing the entire conversation.

It combines:

- a verified session handoff with current repository, GitHub, validation, risk, and next-step
  evidence;
- an advisory agent retrospective covering outcome quality, process friction, retries, cost,
  safety, and external side effects;
- an approval queue for bounded improvements to AGENTS.md, prompts, skills, workflows, and
  other project instruction contracts.

## Why use it?

Long coding sessions often leave behind stale handoff notes, repeated validation work, and
useful process improvements that are easy to forget. session-close creates a compact
continuation checkpoint while keeping retrospective recommendations separate from approved
project decisions.

## What it does

When explicitly invoked, session-close:

1. reads the installed session-handoff and agent-retrospective skills;
2. reads the nearest AGENTS.md and the project's configured handoff file;
3. verifies the smallest useful set of repository and GitHub facts;
4. saves a structured private retrospective with stable RETRO IDs;
5. updates the project handoff with current state and pending recommendations;
6. validates the handoff for stale claims, secrets, and unrelated changes.

Instruction-contract findings are recorded with an exact target file, target section,
evidence, bounded scope, and success signal. They remain PENDING APPROVAL.

## What it does not do automatically

session-close does not silently:

- modify code, AGENTS.md, prompts, skills, workflows, or project policy;
- commit, push, merge, delete branches, or change repository settings;
- apply a retrospective recommendation;
- record API keys, tokens, cookies, raw transcripts, or sensitive logs.

Use explicit approval before applying a proposal:

~~~text
approve RETRO-ID
approve RETRO-ID apply
~~~

For AGENTS.md and other instruction-contract changes, approval prepares a minimal diff;
application remains bounded to the named file and section.

## Installation

Install the skills/session-close directory into the configured Codex skill root, preserving:

~~~text
SKILL.md
agents/openai.yaml
~~~

The skill is explicit-only and does not invoke implicitly during unrelated work. It expects
the companion skills named session-handoff and agent-retrospective to be available.

## Usage

At the end of a substantive session:

~~~text
$session-close
~~~

The default close flow saves the local handoff and private retrospective without committing
or pushing. Request commit or push separately when the handoff should be published.

## Portability and privacy

The skill is project-agnostic:

- it resolves companion skills from the active Codex skill catalog;
- it discovers AGENTS.md and the project's configured handoff file;
- it uses the current user's configured Codex data directory for private retrospectives;
- it does not embed a username, machine path, repository name, or model-specific setup.

## Repository layout

~~~text
skills/
└── session-close/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
~~~

## License

Released under the [MIT License](LICENSE).
