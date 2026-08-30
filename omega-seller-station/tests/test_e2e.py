import json

from omega.station import SellerStation


def test_mock_mission_reaches_human_or_pass(tmp_path):
    (tmp_path / "catalog.json").write_text(
        json.dumps({"kdp_paperback": 9.99, "imprints": ["Quiet Mind Press"]}),
        encoding="utf-8",
    )
    (tmp_path / ".seller-station.json").write_text(
        json.dumps({"model_provider": "mock", "auto_merge": False}),
        encoding="utf-8",
    )
    station = SellerStation(tmp_path)
    station.add_mission(
        {
            "mission_id": "MKT-001",
            "title": "Draft pin for The Dopamine Menu",
            "requirements": ["tracking only"],
            "files": ["generated/dopamine_pins.json"],
            "output_path": "generated/dopamine_pins.json",
            "action": "draft_copy",
            "priority": 10,
            "mock_body": (
                "The Dopamine Menu — Quiet Mind Press. "
                "Paperback $9.99 on KDP. Tracking and management only."
            ),
        }
    )
    results = station.run()
    assert results
    assert results[0]["status"] in {"complete", "hold"}
    asset = tmp_path / "generated" / "dopamine_pins.json"
    assert asset.exists()
    text = asset.read_text(encoding="utf-8")
    assert "Ozempic" not in text
    assert (tmp_path / ".omega" / "evidence.jsonl").exists()
    assert station.shadow.verify("consensus")["ok"] is True


def test_poison_copy_is_reworked_or_escalated(tmp_path):
    (tmp_path / "catalog.json").write_text(
        json.dumps({"kdp_paperback": 9.99}), encoding="utf-8"
    )
    station = SellerStation(tmp_path)
    station.add_mission(
        {
            "mission_id": "MKT-BAD",
            "title": "Poison",
            "files": ["generated/bad.json"],
            "output_path": "generated/bad.json",
            "action": "draft_copy",
            "mock_body": "Take Ozempic and you are cured.",
        }
    )
    results = station.run()
    assert results[0]["status"] in {"rework", "escalated"}
