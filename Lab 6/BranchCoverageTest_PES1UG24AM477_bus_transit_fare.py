import pytest
from bus_transit_fare import process_commute_manifest, inspect_smartcard_turnstiles

def test_invalid_input_raises_value_error():
    with pytest.raises(ValueError):
        process_commute_manifest("invalid_manifest_format", 5.0)
    with pytest.raises(ValueError):
        process_commute_manifest([], -1.0)

def test_inactive_route():
    manifests = [{"route_active": False}]
    result = process_commute_manifest(manifests, 2.0)
    assert result["status"] == "ZERO_RIDERSHIP"
    assert result["total_fare"] == 0.0

def test_unknown_route_type_rejection():
    manifests = [{"route_active": True, "route_type": "hyperloop"}]
    result = process_commute_manifest(manifests, 2.0)
    assert result["status"] == "ZERO_RIDERSHIP"

def test_express_clean_ride():
    manifests = [
        {
            "route_active": True,
            "route_type": "express",
            "priority_boarding": False,
            "commuters": [{"zones": 3, "type": "regular", "blacklisted": False}]
        }
    ]
    # base_seat = 6.0 + 3*1.0 = 9.0
    result = process_commute_manifest(manifests, 5.0)
    assert result["total_fare"] == 9.0
    assert result["status"] == "COMPLETED"

def test_shuttle_and_concessions_with_priority():
    manifests = [
        {
            "route_active": True,
            "route_type": "shuttle",
            "priority_boarding": True,
            "commuters": [
                {"zones": 2, "type": "student", "blacklisted": False},
                {"zones": 2, "type": "senior", "blacklisted": False},
                {"zones": 2, "type": "regular", "blacklisted": False},
            ]
        }
    ]
    result = process_commute_manifest(manifests, 3.0)
    assert result["total_fare"] == 15.0
    assert result["status"] == "COMPLETED"

def test_invalid_zone_and_non_express_blacklist():
    manifests = [
        {
            "route_active": True,
            "route_type": "local",
            "commuters": [
                {"zones": 0, "type": "regular"},
                {"zones": 1, "blacklisted": True}
            ]
        }
    ]
    result = process_commute_manifest(manifests, 0.0)
    assert result["status"] == "ZERO_RIDERSHIP"

def test_express_blacklisted_card_break():
    manifests = [
        {
            "route_active": True,
            "route_type": "express",
            "commuters": [
                {"zones": 2, "blacklisted": True},
                {"zones": 2, "type": "regular"}
            ]
        }
    ]
    result = process_commute_manifest(manifests, 0.0)
    assert result["status"] == "ZERO_RIDERSHIP"

def test_audit_rejected_threshold():
    manifests = [{"route_active": True, "route_type": f"unknown_{i}"} for i in range(5)]
    result = process_commute_manifest(manifests, 1.0)
    assert result["status"] == "AUDIT_REJECTED"

def test_turnstiles_no_data():
    assert inspect_smartcard_turnstiles([]) == "NO_DATA"

def test_turnstiles_jam_streak():
    matrix = [[1, 4, 5, 2]]
    assert inspect_smartcard_turnstiles(matrix) == "TURNSTILE_JAM"

def test_turnstiles_streak_reset_operational():
    matrix = [[4, 1, 4, 2]]
    assert inspect_smartcard_turnstiles(matrix) == "OPERATIONAL"

