import pytest

from worldobject import WorldObject


@pytest.fixture
def wo():
    wo = WorldObject()
    return wo

def test_default_initialization(wo):
    assert wo.color is None
    assert wo.value == 0
    assert wo.rect is None
    assert wo.can_react is False
    assert wo.primed_collision is True

def test_should_remove(wo):
    assert wo.should_remove() is False

def test_allow_collision(wo):
    assert wo.allow_collision() is True