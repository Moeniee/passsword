import string
 
import pytest
 
from passsword.generate import generate_password
 
# Random output: repeat checks so a rare failure doesn't slip through.
REPEATS = 100
 
# Keys must match the parameter names of generate_password.
GROUPS = {
    "uppercase": string.ascii_uppercase,
    "lowcase": string.ascii_lowercase,
    "number": string.digits,
    "symbol": string.punctuation,
}
 
 
def only(enabled):
    """Kwargs with just the `enabled` group turned on."""
    return {name: name == enabled for name in GROUPS}
 
 
def all_except(disabled):
    """Kwargs with every group on except `disabled`."""
    return {name: name != disabled for name in GROUPS}
 
 
# --- size ---------------------------------------------------------------
 
 
def test_default_size_is_16():
    assert len(generate_password()) == 16
 
 
@pytest.mark.parametrize("size", [4, 8, 16, 32, 64])
def test_password_has_requested_size(size):
    for _ in range(REPEATS):
        assert len(generate_password(size=size)) == size
 
 
def test_returns_a_string():
    assert isinstance(generate_password(), str)
 
 
def test_size_equal_to_number_of_filters_is_valid():
    password = generate_password(
        size=2, uppercase=True, lowcase=True, number=False, symbol=False
    )
    assert len(password) == 2
 
 
# --- groups -------------------------------------------------------------
 
 
def test_every_enabled_group_appears():
    # size=4 with 4 groups: only the "required" characters, no free slots
    for _ in range(REPEATS):
        password = generate_password(size=4)
        for characters in GROUPS.values():
            assert any(c in characters for c in password)
 
 
@pytest.mark.parametrize("disabled", list(GROUPS))
def test_disabled_group_never_appears(disabled):
    forbidden = GROUPS[disabled]
    for _ in range(REPEATS):
        password = generate_password(size=20, **all_except(disabled))
        assert not any(c in forbidden for c in password)
 
 
@pytest.mark.parametrize("enabled", list(GROUPS))
def test_single_group_only_uses_that_group(enabled):
    allowed = GROUPS[enabled]
    for _ in range(REPEATS):
        password = generate_password(size=12, **only(enabled))
        assert all(c in allowed for c in password)
 
 
# --- errors -------------------------------------------------------------
 
 
@pytest.mark.parametrize("size", [0, -1, -100])
def test_zero_or_negative_size_raises(size):
    with pytest.raises(ValueError):
        generate_password(size=size)
 
 
def test_no_filter_raises():
    with pytest.raises(ValueError):
        generate_password(
            uppercase=False, lowcase=False, number=False, symbol=False
        )
 
 
def test_size_smaller_than_number_of_filters_raises():
    # 4 groups enabled by default, size 3 can't fit one of each
    with pytest.raises(ValueError):
        generate_password(size=3)
 
 
# --- randomness ---------------------------------------------------------
 
 
def test_passwords_are_different_each_time():
    passwords = {generate_password() for _ in range(50)}
    assert len(passwords) == 50
 
