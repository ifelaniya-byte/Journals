from omega.scanners import ShadowScanner, independent_dual_scan


def test_independent_order_and_no_peer(tmp_path):
    (tmp_path / "a.py").write_text("print(1)", encoding="utf-8")
    (tmp_path / "b.py").write_text("print(2)", encoding="utf-8")
    (tmp_path / "c.py").write_text("print(3)", encoding="utf-8")
    scan_a, scan_b = independent_dual_scan(tmp_path)
    assert scan_a["scanner"] == "A"
    assert scan_b["scanner"] == "B"
    assert "peer" not in scan_a
    assert "peer" not in scan_b
    order_a = [f["path"] for f in scan_a["files"]]
    order_b = [f["path"] for f in scan_b["files"]]
    assert set(order_a) == set(order_b)
    # Salted traversal — order is allowed to differ.
    key_a = ShadowScanner(tmp_path, "A")._order_key("a.py")
    key_b = ShadowScanner(tmp_path, "B")._order_key("a.py")
    assert key_a != key_b


def test_secret_regex_ignores_architecture_prose(tmp_path):
    (tmp_path / "notes.md").write_text(
        "Shadow stores a seal. Stationary never writes a secret fix.",
        encoding="utf-8",
    )
    (tmp_path / "leaked.pem").write_text(
        "-----BEGIN RSA PRIVATE KEY-----\nAAAA\n-----END RSA PRIVATE KEY-----\n",
        encoding="utf-8",
    )
    scan_a, _ = independent_dual_scan(tmp_path)
    assert "notes.md" not in scan_a["secrets_suspects"]
    assert "leaked.pem" in scan_a["secrets_suspects"]


def test_overseer_ignores_test_fixtures():
    from omega.overseers import Overseer

    verdict = Overseer("A").judge(
        {"action": "draft_copy"},
        {"verdict": "PASS"},
        {"verdict": "PASS"},
        consensus={"secrets_suspects": ["tests/test_scanners.py"]},
    )
    assert verdict["accept"] is True
    blocked = Overseer("A").judge(
        {"action": "draft_copy"},
        {"verdict": "PASS"},
        {"verdict": "PASS"},
        consensus={"secrets_suspects": ["id_rsa"]},
    )
    assert blocked["accept"] is False
