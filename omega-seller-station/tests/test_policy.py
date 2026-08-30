from omega.policy import audit_asset, audit_text


def test_blacklist_ozempic():
    reasons = audit_text("Start Ozempic this week")
    assert any("ozempic" in r for r in reasons)


def test_bn_price_not_on_kdp(tmp_path):
    (tmp_path / "catalog.json").write_text(
        '{"kdp_paperback": 9.99}', encoding="utf-8"
    )
    result = audit_asset(
        "Buy it on Amazon KDP for $14.99",
        root=tmp_path,
    )
    assert result["ok"] is False
    assert any("pricing_drift" in r for r in result["reasons"])


def test_blocked_kdp_upload(tmp_path):
    result = audit_asset({"action": "kdp_upload", "text": "ok"}, root=tmp_path)
    assert result["ok"] is False
    assert any("blocked_action" in r for r in result["reasons"])


def test_clean_copy_passes(tmp_path):
    (tmp_path / "catalog.json").write_text(
        '{"kdp_paperback": 9.99}', encoding="utf-8"
    )
    result = audit_asset(
        "The Dopamine Menu. Quiet Mind Press. Paperback $9.99. Tracking only.",
        root=tmp_path,
    )
    assert result["ok"] is True
