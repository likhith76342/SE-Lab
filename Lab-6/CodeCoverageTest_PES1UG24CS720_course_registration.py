import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_unknown_status():
    with pytest.raises(ValueError):
        can_register("alumni", 10, 4, True)

def test_invalid_course_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, 0, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_invalid_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, 0, 0)

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_position_assigned():
    assert waitlist_position(40, 40, 3) == 4


# ---------- late_fee ----------
def test_not_late():
    assert late_fee(0, 18, False) == 0

def test_late_with_waiver():
    assert late_fee(5, 18, True) == 0

def test_late_within_week_heavy_load():
    assert late_fee(3, 22, False) == 750

def test_late_beyond_week_capped():
    assert late_fee(30, 22, False) == 2000
