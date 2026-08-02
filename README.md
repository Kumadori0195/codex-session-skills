# Codex Session Skills

Portable Codex skills for preserving project context across sessions and turning
retrospective findings into explicitly approved improvements.

## Included

### session-close

Use $session-close at the end of a substantive session to:

1. review the session with the installed agent-retrospective skill;
2. queue bounded improvement proposals, including AGENTS.md or project-instruction
   contract changes, as PENDING APPROVAL;
3. finalize a verified handoff with the installed session-handoff skill;
4. leave implementation, commit, push, and merge actions to explicit user approval.

The skill is designed to be project-agnostic. It discovers the active project's
AGENTS.md, configured handoff file, repository state, validation evidence, and external
effects instead of embedding a repository name or user-specific filesystem path.

## Installation

Install the skills/session-close directory into the Codex skill root, preserving the
SKILL.md and agents/openai.yaml files. The skill is explicit-only and does not invoke
implicitly during unrelated work.

## Approval model

Retrospective proposals receive stable RETRO-... IDs and remain pending until explicitly
approved. An instruction-contract proposal must identify its exact target file and section,
show a bounded diff before application, and pass the project's normal validation rules.
