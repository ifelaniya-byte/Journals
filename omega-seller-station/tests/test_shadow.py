from omega.shadow import ShadowStore, seal


def test_seal_stable():
    assert seal({"a": 1, "b": 2}) == seal({"b": 2, "a": 1})


def test_corruption_detected_and_resealed(tmp_path):
    store = ShadowStore(tmp_path / "shadow.json")
    payload = {"tree": "ok"}
    store.put("map", payload, reason="create")
    assert store.verify("map")["ok"] is True
    store._data["map"]["payload"] = {"tree": "tampered"}
    result = store.verify("map")
    assert result["ok"] is False
    assert result["reason"] == "CORRUPTION"
    store.reseal("map", {"tree": "ok"}, reason="verified-restore")
    assert store.verify("map")["ok"] is True
    assert "reseal" in store._data["map"]["history"][-1]["reason"]
