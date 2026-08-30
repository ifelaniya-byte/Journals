from __future__ import annotations

import argparse
import json
from pathlib import Path

from .station import SellerStation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omega",
        description="Omega/Shadow seller station — missions, not vibes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("scan")
    sub.add_parser("status")
    sub.add_parser("run")
    missions = sub.add_parser("missions")
    missions.add_argument("file")
    seal = sub.add_parser("seal-check")
    seal.add_argument("name")
    sub.add_parser("gate")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path.cwd()
    station = SellerStation(root)

    if args.command == "init":
        station.scan()
        print(
            json.dumps(
                {"initialized": True, "workspace": str(station.workspace)},
                indent=2,
            )
        )
        return 0
    if args.command == "scan":
        print(json.dumps(station.scan(), indent=2, default=str))
        return 0
    if args.command == "missions":
        count = station.import_missions(Path(args.file))
        print(f"Imported {count} mission(s).")
        return 0
    if args.command == "status":
        print(json.dumps(station.status(), indent=2, default=str))
        return 0
    if args.command == "run":
        results = station.run()
        print(json.dumps(results, indent=2, default=str))
        hold = all(r.get("status") in {"complete", "hold"} for r in results) if results else True
        return 0 if hold else 1
    if args.command == "seal-check":
        print(json.dumps(station.shadow.verify(args.name), indent=2))
        return 0 if station.shadow.verify(args.name).get("ok") else 1
    if args.command == "gate":
        print(
            json.dumps(
                {
                    "auto_merge": station.config.auto_merge,
                    "human_required": True,
                    "blocked_actions": station.config.blocked_actions,
                },
                indent=2,
            )
        )
        return 0
    return 1
