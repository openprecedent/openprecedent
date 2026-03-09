from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from openprecedent.config import get_db_path
from openprecedent.schemas import EventActor, EventType
from openprecedent.services import AppendEventInput, CreateCaseInput, OpenPrecedentService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openprecedent")
    subparsers = parser.add_subparsers(dest="resource", required=True)

    case_parser = subparsers.add_parser("case")
    case_subparsers = case_parser.add_subparsers(dest="action", required=True)
    case_create = case_subparsers.add_parser("create")
    case_create.add_argument("--title", required=True)
    case_create.add_argument("--case-id")
    case_create.add_argument("--user-id")
    case_create.add_argument("--agent-id")
    case_subparsers.add_parser("list")
    case_show = case_subparsers.add_parser("show")
    case_show.add_argument("case_id")

    event_parser = subparsers.add_parser("event")
    event_subparsers = event_parser.add_subparsers(dest="action", required=True)
    event_append = event_subparsers.add_parser("append")
    event_append.add_argument("case_id")
    event_append.add_argument("event_type", choices=[item.value for item in EventType])
    event_append.add_argument("actor", choices=[item.value for item in EventActor])
    event_append.add_argument("--payload", default="{}")
    event_append.add_argument("--event-id")
    event_import = event_subparsers.add_parser("import-jsonl")
    event_import.add_argument("path")
    event_import.add_argument("--case-id")

    replay_parser = subparsers.add_parser("replay")
    replay_subparsers = replay_parser.add_subparsers(dest="action", required=True)
    replay_case = replay_subparsers.add_parser("case")
    replay_case.add_argument("case_id")
    replay_case.add_argument("--json", action="store_true", dest="as_json")

    extract_parser = subparsers.add_parser("extract")
    extract_subparsers = extract_parser.add_subparsers(dest="action", required=True)
    extract_decisions = extract_subparsers.add_parser("decisions")
    extract_decisions.add_argument("case_id")

    decisions_parser = subparsers.add_parser("decisions")
    decisions_subparsers = decisions_parser.add_subparsers(dest="action", required=True)
    decisions_show = decisions_subparsers.add_parser("show")
    decisions_show.add_argument("case_id")
    decisions_show.add_argument("--json", action="store_true", dest="as_json")

    precedent_parser = subparsers.add_parser("precedent")
    precedent_subparsers = precedent_parser.add_subparsers(dest="action", required=True)
    precedent_find = precedent_subparsers.add_parser("find")
    precedent_find.add_argument("case_id")
    precedent_find.add_argument("--limit", type=int, default=3)

    runtime_parser = subparsers.add_parser("runtime")
    runtime_subparsers = runtime_parser.add_subparsers(dest="action", required=True)
    runtime_import = runtime_subparsers.add_parser("import-openclaw")
    runtime_import.add_argument("path")
    runtime_import.add_argument("--case-id", required=True)
    runtime_import.add_argument("--title", required=True)
    runtime_import.add_argument("--user-id")
    runtime_import.add_argument("--agent-id", default="openclaw")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    service = OpenPrecedentService.from_path(get_db_path())

    try:
        if args.resource == "case":
            return _handle_case(args, service)
        if args.resource == "event":
            return _handle_event(args, service)
        if args.resource == "replay":
            return _handle_replay(args, service)
        if args.resource == "extract":
            return _handle_extract(args, service)
        if args.resource == "decisions":
            return _handle_decisions(args, service)
        if args.resource == "precedent":
            return _handle_precedent(args, service)
        if args.resource == "runtime":
            return _handle_runtime(args, service)
    except KeyError as error:
        print(f"case not found: {error.args[0]}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1

    parser.error("unknown command")
    return 2


def run() -> None:
    raise SystemExit(main())


def _handle_case(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    if args.action == "create":
        case = service.create_case(
            CreateCaseInput(
                case_id=args.case_id,
                title=args.title,
                user_id=args.user_id,
                agent_id=args.agent_id,
            )
        )
        _print_json(case.model_dump(mode="json"))
        return 0
    if args.action == "list":
        _print_json([case.model_dump(mode="json") for case in service.list_cases()])
        return 0
    if args.action == "show":
        case = service.get_case(args.case_id)
        if case is None:
            print(f"case not found: {args.case_id}", file=sys.stderr)
            return 1
        _print_json(case.model_dump(mode="json"))
        return 0
    return 2


def _handle_event(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    if args.action == "append":
        payload = json.loads(args.payload)
        event = service.append_event(
            args.case_id,
            AppendEventInput(
                event_id=args.event_id,
                event_type=EventType(args.event_type),
                actor=EventActor(args.actor),
                payload=payload,
            ),
        )
        _print_json(event.model_dump(mode="json"))
        return 0
    if args.action == "import-jsonl":
        imported = service.import_events_jsonl(Path(args.path), default_case_id=args.case_id)
        _print_json([event.model_dump(mode="json") for event in imported])
        return 0
    return 2


def _handle_replay(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    replay = service.replay_case(args.case_id)
    if args.as_json:
        _print_json(replay.model_dump(mode="json"))
        return 0

    print(f"Case {replay.case.case_id}: {replay.case.title}")
    print(f"Status: {replay.case.status.value}")
    print("Events:")
    for event in replay.events:
        print(f"  [{event.sequence_no}] {event.event_type.value} ({event.actor.value})")
    print("Decisions:")
    for decision in replay.decisions:
        print(f"  [{decision.sequence_no}] {decision.decision_type.value}: {decision.title}")
        print(f"      why: {decision.explanation.selection_reason}")
        if decision.explanation.result:
            print(f"      result: {decision.explanation.result}")
    print("Artifacts:")
    for artifact in replay.artifacts:
        print(f"  - {artifact.artifact_type.value}: {artifact.uri_or_path}")
        if artifact.summary:
            print(f"      summary: {artifact.summary}")
    if replay.summary:
        print(f"Summary: {replay.summary}")
    return 0


def _handle_extract(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    decisions = service.extract_decisions(args.case_id)
    _print_json([decision.model_dump(mode="json") for decision in decisions])
    return 0


def _handle_decisions(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    decisions = service.list_decisions(args.case_id)
    if args.as_json:
        _print_json([decision.model_dump(mode="json") for decision in decisions])
        return 0

    for decision in decisions:
        print(f"[{decision.sequence_no}] {decision.decision_type.value}: {decision.title}")
        print(f"  question: {decision.question}")
        print(f"  chosen_action: {decision.chosen_action}")
        print(f"  confidence: {decision.confidence:.2f}")
        print(f"  goal: {decision.explanation.goal}")
        print(f"  why: {decision.explanation.selection_reason}")
        if decision.explanation.evidence:
            print(f"  evidence: {', '.join(decision.explanation.evidence)}")
        if decision.explanation.constraints:
            print(f"  constraints: {', '.join(decision.explanation.constraints)}")
        if decision.explanation.result:
            print(f"  result: {decision.explanation.result}")
    return 0


def _handle_precedent(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    precedents = service.find_precedents(args.case_id, limit=args.limit)
    _print_json([precedent.model_dump(mode="json") for precedent in precedents])
    return 0


def _handle_runtime(args: argparse.Namespace, service: OpenPrecedentService) -> int:
    if args.action == "import-openclaw":
        result = service.import_openclaw_jsonl(
            Path(args.path),
            case_id=args.case_id,
            title=args.title,
            user_id=args.user_id,
            agent_id=args.agent_id,
        )
        _print_json(
            {
                "case": result.case.model_dump(mode="json"),
                "imported_event_count": len(result.imported_events),
                "events": [event.model_dump(mode="json") for event in result.imported_events],
            }
        )
        return 0
    return 2


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
