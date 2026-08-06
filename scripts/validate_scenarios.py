#!/usr/bin/env python3
"""Validate the repository-local session-close behavior scenario contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_SCENARIO_FILE = (
    Path(__file__).resolve().parents[1] / "evals" / "session-close" / "scenarios.json"
)
SCENARIO_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _transition_list(value: Any) -> bool:
    return isinstance(value, list) and all(
        isinstance(pair, list)
        and len(pair) == 2
        and all(isinstance(item, str) for item in pair)
        for pair in value
    )


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"scenario file does not exist: {path}"]
    except json.JSONDecodeError as exc:
        return [f"invalid JSON at {path}:{exc.lineno}:{exc.colno}: {exc.msg}"]

    if not isinstance(document, dict):
        return ["scenario document must be a JSON object"]

    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if document.get("skill") != "session-close":
        errors.append("skill must be session-close")

    evidence_statuses = document.get("evidence_statuses")
    if not _string_list(evidence_statuses) or not evidence_statuses:
        errors.append("evidence_statuses must be a non-empty string list")
        evidence_statuses = []
    evidence_status_set = set(evidence_statuses)

    proposal_states = document.get("proposal_states")
    if not _string_list(proposal_states) or not proposal_states:
        errors.append("proposal_states must be a non-empty string list")
        proposal_states = []
    proposal_state_set = set(proposal_states)

    allowed_transitions = document.get("allowed_transitions")
    if not _transition_list(allowed_transitions):
        errors.append("allowed_transitions must contain [from, to] string pairs")
        allowed_transitions = []
    allowed_transition_set = {tuple(pair) for pair in allowed_transitions}
    for source, target in allowed_transition_set:
        if source not in proposal_state_set or target not in proposal_state_set:
            errors.append(f"allowed transition uses an unknown state: {source} -> {target}")

    required_ids = document.get("required_scenario_ids")
    if not _string_list(required_ids) or not required_ids:
        errors.append("required_scenario_ids must be a non-empty string list")
        required_ids = []

    scenarios = document.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        errors.append("scenarios must be a non-empty list")
        scenarios = []

    seen_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        prefix = f"scenario[{index}]"
        if not isinstance(scenario, dict):
            errors.append(f"{prefix} must be an object")
            continue

        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not SCENARIO_ID.fullmatch(scenario_id):
            errors.append(f"{prefix}.id must be lowercase kebab-case")
        elif scenario_id in seen_ids:
            errors.append(f"duplicate scenario id: {scenario_id}")
        else:
            seen_ids.add(scenario_id)

        for field in ("category", "request"):
            if not isinstance(scenario.get(field), str) or not scenario[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        if not isinstance(scenario.get("setup"), dict):
            errors.append(f"{prefix}.setup must be an object")

        expected = scenario.get("expected")
        if not isinstance(expected, dict):
            errors.append(f"{prefix}.expected must be an object")
            continue

        discovery = expected.get("discovery")
        if not isinstance(discovery, dict):
            errors.append(f"{prefix}.expected.discovery must be an object")
        else:
            for field in ("status", "reason"):
                if not isinstance(discovery.get(field), str) or not discovery[field].strip():
                    errors.append(f"{prefix}.expected.discovery.{field} must be a non-empty string")
            if discovery.get("selected_path") is not None and not isinstance(
                discovery.get("selected_path"), str
            ):
                errors.append(f"{prefix}.expected.discovery.selected_path must be a string or null")
            repro_path = discovery.get("selected_repro_path")
            if discovery.get("status") in {"SELECTED", "DEFAULT_CREATED"}:
                if not isinstance(repro_path, str) or not repro_path.strip():
                    errors.append(
                        f"{prefix}.expected.discovery.selected_repro_path must be a non-empty string "
                        "when a project handoff is selected or created"
                    )
            elif repro_path is not None and not isinstance(repro_path, str):
                errors.append(
                    f"{prefix}.expected.discovery.selected_repro_path must be a string or null"
                )

        evidence = expected.get("evidence_statuses")
        if not _string_list(evidence) or not evidence:
            errors.append(f"{prefix}.expected.evidence_statuses must be a non-empty string list")
        else:
            for status in evidence:
                if status not in evidence_status_set:
                    errors.append(f"{prefix} uses unknown evidence status: {status}")

        states = expected.get("proposal_states")
        if not _string_list(states):
            errors.append(f"{prefix}.expected.proposal_states must be a string list")
        else:
            for state in states:
                if state not in proposal_state_set:
                    errors.append(f"{prefix} uses unknown proposal state: {state}")

        for field in ("allowed_writes", "forbidden_effects", "observations"):
            values = expected.get(field)
            if not _string_list(values) or not values:
                errors.append(f"{prefix}.expected.{field} must be a non-empty string list")

        transitions = expected.get("transitions", [])
        if not _transition_list(transitions):
            errors.append(f"{prefix}.expected.transitions must contain [from, to] string pairs")
        else:
            for pair in transitions:
                if tuple(pair) not in allowed_transition_set:
                    errors.append(f"{prefix} contains disallowed transition: {pair[0]} -> {pair[1]}")

        invalid_transitions = expected.get("invalid_transitions", [])
        if not _transition_list(invalid_transitions):
            errors.append(
                f"{prefix}.expected.invalid_transitions must contain [from, to] string pairs"
            )
        else:
            for pair in invalid_transitions:
                if tuple(pair) in allowed_transition_set:
                    errors.append(
                        f"{prefix} marks an allowed transition as invalid: {pair[0]} -> {pair[1]}"
                    )

    missing_ids = sorted(set(required_ids) - seen_ids)
    if missing_ids:
        errors.append(f"required scenarios are missing: {', '.join(missing_ids)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=DEFAULT_SCENARIO_FILE,
        help="scenario JSON file (default: evals/session-close/scenarios.json)",
    )
    args = parser.parse_args()
    path = args.path.resolve()

    errors = validate(path)
    if errors:
        print("Scenario validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    document = json.loads(path.read_text(encoding="utf-8"))
    print(
        f"Validated {len(document['scenarios'])} session-close scenarios and "
        f"{len(document['allowed_transitions'])} proposal transitions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
