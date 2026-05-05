import pytest

from pmpge.game_object import GameObject, update_hierarchy
from pmpge.traits.lifetime import Lifetime


def test_constructor():
    """
    Simple test to ensure that Lifetime works.
    """
    trait = Lifetime()
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime is None

    trait = Lifetime(10)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 10


def test_update_when_no_lifetime_set():
    """
    Validates that destroy is not set when no lifetime set.
    """
    trait = Lifetime()
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime is None

    trait.update(1)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime is None

    trait.update(0)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime is None

    trait.update(2)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime is None

    # Now test when used as a GameObject
    go = GameObject(Lifetime())
    assert trait.lifetime is None
    update_hierarchy(go, 1)
    assert trait.lifetime is None


# noinspection PyUnresolvedReferences
def test_update_when_lifetime_set():
    """
    Validates that lifetime decreased when lifetime set and triggers destroy.
    """
    trait = Lifetime(5)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 5

    trait.update(1)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 4

    trait.update(1)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 3

    trait.update(2)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 1

    trait.update(0)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 1

    trait.update(0.5)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 0.5

    # This will error because it is not part of a GameObject
    with pytest.raises(AttributeError):
        trait.update(0.5)

    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 0

    # Now test when used as a GameObject
    go = GameObject(Lifetime(2))
    assert go.lifetime == 2
    assert go.alive
    update_hierarchy(go, 1)
    assert go.lifetime == 1
    assert go.alive
    update_hierarchy(go, 1)
    assert go.lifetime == 0
    assert not go.alive


def test_update_when_extending_lifetime():
    """
    Validates that lifetime can be extended.
    """
    trait = Lifetime(5)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 5

    trait.update(1)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 4

    trait.lifetime = 6
    trait.update(1)
    assert not hasattr(trait, 'destroy')
    assert trait.lifetime == 5

    # Now test when used as a GameObject
    go = GameObject(Lifetime(2))
    assert go.lifetime == 2
    assert go.alive
    update_hierarchy(go, 1)
    assert go.lifetime == 1
    assert go.alive
    go.lifetime = 6
    update_hierarchy(go, 1)
    assert go.lifetime == 5
    assert go.alive
