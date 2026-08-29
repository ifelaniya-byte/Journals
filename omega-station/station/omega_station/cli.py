from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import OmegaStation
from .policy import PolicyVerifier


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="omega-station",
        description="Reflective autonomous engineering pipeline "
                    "(Omega/Shadow control architecture).")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("recon", help="dual independent scans + consensus")
    sub.add_parser("missions", help="generate missions from consensus")
    sub.add_parser("run", help="run the full reflective loop (mock by default)")
    sub.add_parser("status", help="station status report")
    sub.add_parser("ledger", help="verify the hash-chained evidence ledger")
    sub.add_parser("integrity", help="verify shadow seals vs filesystem")
    pol = sub.add_parser("policy", help="audit a marketing/copy file")
    pol.add_argument("file")
    pol.add_argument("--banned", help="banned phrases file (one per line)")
    pol.add_argument("--prices", help="JSON catalog {title: price}")
    pol.add_argument("--title", help="catalog title to check price drift")
    pol.add_argument("--require-disclaimer", action="store_true")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    root = Path.cwd()
    station = OmegaStation(root)

    if args.command == "recon":
        c = station.recon()
        print(json.dumps({
            "scan_a": c["scan_a_method"], "scan_b": c["scan_b_method"],
            "confirmed": len(c["confirmed"]),
            "single_source": len(c["single_source"]),
            "disputed": len(c["disputed"]),
        }, indent=2))
        return 0
    if args.command == "missions":
        missions = station.generate_missions()
        print(json.dumps(
            [{"id": m["mission_id"], "type": m["type"], "risk": m["risk"],
              "priority": m["priority"], "title": m["title"]}
             for m in missions], indent=2))
        return 0
    if args.command == "run":
        results = station.run()
        print(json.dumps(results, indent=2, default=str))
        ok = all(r.get("status") in {"complete", "escalated"} for r in results)
        return 0 if ok else 1
    if args.command == "status":
        print(json.dumps(station.status(), indent=2, default=str))
        return 0
    if args.command == "ledger":
        v = station.verify_ledger()
        print(json.dumps(v, indent=2))
        return 0 if v["ok"] else 1
    if args.command == "integrity":
        v = station.verify_integrity()
        print(json.dumps(v, indent=2))
        return 0 if v.get("clean", True) else 1
    if args.command == "policy":
        text = Path(args.file).read_text(encoding="utf-8")
        pv = PolicyVerifier.from_files(
            Path(args.banned) if args.banned else None,
            Path(args.prices) if args.prices else None,
            require_disclaimer=args.require_disclaimer)
        report = pv.check(text, title=args.title)
        print(json.dumps(report, indent=2))
        return 0 if report["pass"] else 1
    return 1
