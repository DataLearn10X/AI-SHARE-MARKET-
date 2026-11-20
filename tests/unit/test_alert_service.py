"""Unit tests for alert service (CRUD only)."""

from services.alert_service import add_alert, delete_alert, list_alerts


def test_alert_crud():
    # clean any existing TESTALERT
    for a in list_alerts():
        if a["symbol"] == "TESTALERT":
            delete_alert(a["id"])
    aid_list_before = [a["id"] for a in list_alerts()]
    assert add_alert("TESTALERT", "ROE %", ">", 10.0) is True
    alerts = list_alerts()
    new = [a for a in alerts if a["symbol"] == "TESTALERT"]
    assert len(new) == 1
    assert delete_alert(new[0]["id"]) is True
    assert not any(a["symbol"] == "TESTALERT" for a in list_alerts())


def test_alert_invalid_operator():
    assert add_alert("X", "Price", ">>", 1.0) is False
