import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_registered_exactly_at_limit():
    assert can_register("honors", 24, 4, True) == "registered"

def test_unknown_status():
    with pytest.raises(ValueError):
        can_register("alumni", 10, 4, True)

def test_invalid_course_credits_zero():
    with pytest.raises(ValueError):
        can_register("regular", 10, 0, True)

def test_invalid_course_credits_negative():
    with pytest.raises(ValueError):
        can_register("honors", 10, -3, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_invalid_capacity_zero():
    with pytest.raises(ValueError):
        waitlist_position(10, 0, 0)

def test_invalid_capacity_negative():
    with pytest.raises(ValueError):
        waitlist_position(10, -5, 0)

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4

def test_waitlist_last_slot():
    assert waitlist_position(45, 40, 9) == 10


# ---------- late_fee ----------
def test_not_late():
    assert late_fee(0, 18, False) == 0

def test_negative_days():
    assert late_fee(-2, 18, False) == 0

def test_late_with_waiver():
    assert late_fee(5, 18, True) == 0

def test_late_within_week_normal_load():
    # days <= 7, credits <= 20, fee <= 2000
    assert late_fee(7, 20, False) == 500

def test_late_within_week_heavy_load():
    # days <= 7, credits > 20
    assert late_fee(3, 22, False) == 750

def test_late_beyond_week_normal_load():
    # days > 7, credits <= 20, fee not capped
    assert late_fee(10, 18, False) == 800

def test_late_beyond_week_heavy_load_not_capped():
    assert late_fee(10, 21, False) == 1050

def test_late_beyond_week_capped():
    # fee > 2000 -> capped
    assert late_fee(30, 22, False) == 2000
