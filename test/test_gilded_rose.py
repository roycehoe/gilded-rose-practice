# -*- coding: utf-8 -*-
import unittest

import pytest

from gilded_rose import GildedRose
from item import Item


@pytest.fixture
def mock_items() -> list[Item]:
    return [
        Item(name="+5 Dexterity Vest", sell_in=10, quality=20),
        Item(name="Aged Brie", sell_in=2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=3, quality=6),  # <-- :O
    ]


@pytest.fixture
def mock_negative_items() -> list[Item]:
    return [
        Item(name="+5 Dexterity Vest", sell_in=-10, quality=20),
        Item(name="Aged Brie", sell_in=-2, quality=0),
        Item(name="Elixir of the Mongoose", sell_in=-5, quality=7),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
        Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=-15, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=-10, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=-5, quality=20),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=-10, quality=49),
        Item(name="Backstage passes to a TAFKAL80ETC concert", sell_in=-5, quality=49),
        Item(name="Conjured Mana Cake", sell_in=-3, quality=6),  # <-- :O
    ]


def test_item_quality_reduces_by_one(mock_items):
    gilded_rose = GildedRose(items=mock_items)

    assert gilded_rose.items[0].quality == 20
    gilded_rose.update_quality()
    assert gilded_rose.items[0].quality == 19


def test_backstage_item_increaes_in_quality_as_sell_in_date_approaches_medium_sell_in_low_quantity(
    mock_items: list[Item],
):
    gilded_rose = GildedRose(items=mock_items)
    backstage_item = gilded_rose.items[6]

    assert backstage_item.name == "Backstage passes to a TAFKAL80ETC concert"
    assert backstage_item.quality == 20
    assert backstage_item.sell_in == 10
    gilded_rose.update_quality()
    assert backstage_item.quality == 22


def test_backstage_item_increaes_in_quality_as_sell_in_date_approaches_low_sell_in_low_quantity(
    mock_items: list[Item],
):
    gilded_rose = GildedRose(items=mock_items)
    backstage_item = gilded_rose.items[7]

    assert backstage_item.name == "Backstage passes to a TAFKAL80ETC concert"
    assert backstage_item.quality == 20
    assert backstage_item.sell_in == 5
    gilded_rose.update_quality()
    assert backstage_item.quality == 23


def test_negative_sell_in_reduces_quality_twice_as_fast(
    mock_negative_items: list[Item],
):
    gilded_rose = GildedRose(items=mock_negative_items)
    negative_sell_in_item = gilded_rose.items[0]

    assert negative_sell_in_item.sell_in < 0
    assert negative_sell_in_item.quality == 20

    gilded_rose.update_quality()

    assert negative_sell_in_item.quality == 18


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        # items = [Item("foo", 0, 0)]
        items = [Item(name="foo", sell_in=0, quality=0)]
        gilded_rose = GildedRose(items=items)
        gilded_rose.update_quality()
        assert "foo" == items[0].name

    def test_repr_with_correct_arg_ordering(self):
        assert repr(Item(name="foo", sell_in=0, quality=0)) == "foo, 0, 0"


if __name__ == "__main__":
    unittest.main()
