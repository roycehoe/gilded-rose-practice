# -*- coding: utf-8 -*-
import unittest

from app.gilded_rose import GildedRose
from app.item import Item


def test_update_lowers_sell_in_for_all_non_legendary_items():
    ticket_item = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=18, quality=49
    )
    non_ticket_appreciable_item = Item(name="Aged Brie", sell_in=1000, quality=0)
    normal_item = Item(name="+5 Dexterity Vest", sell_in=300, quality=20)

    gilded_rose = GildedRose(
        items=[ticket_item, non_ticket_appreciable_item, normal_item]
    )

    gilded_rose.update_items()
    assert gilded_rose.items[0].sell_in == 17
    assert gilded_rose.items[1].sell_in == 999
    assert gilded_rose.items[2].sell_in == 299


def test_update_increases_aged_brie_quality():
    aged_brie_high_sell_in_zero_quality = Item(
        name="Aged Brie", sell_in=1000, quality=0
    )
    aged_brie_low_sell_in_zero_quality = Item(name="Aged Brie", sell_in=1000, quality=0)
    aged_brie_negative_sell_in_zero_quality = Item(
        name="Aged Brie", sell_in=1000, quality=0
    )
    gilded_rose = GildedRose(
        items=[
            aged_brie_high_sell_in_zero_quality,
            aged_brie_low_sell_in_zero_quality,
            aged_brie_negative_sell_in_zero_quality,
        ]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 1
    assert gilded_rose.items[1].quality == 1
    assert gilded_rose.items[2].quality == 1


def test_update_increases_backstage_pass_quality_normally_when_there_are_more_than_10_days_in_sell_in():
    backstage_pass_low_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=11, quality=20
    )
    backstage_pass_high_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=1000, quality=20
    )
    gilded_rose = GildedRose(
        items=[backstage_pass_low_sell_in, backstage_pass_high_sell_in]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 21
    assert gilded_rose.items[1].quality == 21


def test_update_increases_backstage_pass_quality_twice_as_fast_when_there_are_10_days_or_less_but_more_than_5_days():
    backstage_pass_high_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=20
    )
    backstage_pass_low_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=6, quality=20
    )
    gilded_rose = GildedRose(
        items=[backstage_pass_high_sell_in, backstage_pass_low_sell_in]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 22
    assert gilded_rose.items[1].quality == 22


def test_update_increases_backstage_pass_quality_thrice_as_fast_when_there_are_5_days_or_less_excluding_zero_days():
    backstage_pass_high_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=5, quality=20
    )
    # Two is the sell_in threshold, not one, because, if it is one, the update would reduce the sell_in
    # to zero, which brings the sell-in date to zero, which makes the quality zero. This behaviour will be endorsd in subsequent tests
    backstage_pass_low_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=2, quality=20
    )
    gilded_rose = GildedRose(
        items=[backstage_pass_high_sell_in, backstage_pass_low_sell_in]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 23
    assert gilded_rose.items[1].quality == 23


def test_update_increases_backstage_pass_quality_drops_to_zero_days_when_final_sell_in_is_less_or_equal_to_zero():
    backstage_pass_high_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=1, quality=20
    )
    backstage_pass_zero_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20
    )
    backstage_pass_negative_sell_in = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=20
    )
    gilded_rose = GildedRose(
        items=[
            backstage_pass_high_sell_in,
            backstage_pass_zero_sell_in,
            backstage_pass_negative_sell_in,
        ]
    )

    gilded_rose.update_items()
    assert gilded_rose.items[0].sell_in <= 0
    assert gilded_rose.items[1].sell_in <= 0
    assert gilded_rose.items[2].sell_in <= 0

    assert gilded_rose.items[0].quality == 0
    assert gilded_rose.items[1].quality == 0
    assert gilded_rose.items[2].quality == 0


def test_update_cannot_increase_non_legendary_item_quality_above_50():
    backstage_pass_normal_appreciation = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=200, quality=50
    )
    backstage_pass_high_appreciation = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=9, quality=50
    )
    backstage_pass_extreme_appreciation = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=4, quality=50
    )
    backstage_pass_zero_appreciation = Item(
        name="Backstage passes to a TAFKAL80ETC concert", sell_in=0, quality=50
    )
    aged_brie_high_sell_in_zero_quality = Item(
        name="Aged Brie", sell_in=1000, quality=50
    )
    aged_brie_low_sell_in_zero_quality = Item(name="Aged Brie", sell_in=0, quality=0)
    aged_brie_negative_sell_in_zero_quality = Item(
        name="Aged Brie", sell_in=-99, quality=0
    )
    normal_item_positive_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=300, quality=50
    )
    normal_item_negative_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=-300, quality=50
    )

    gilded_rose = GildedRose(
        items=[
            backstage_pass_normal_appreciation,
            backstage_pass_high_appreciation,
            backstage_pass_extreme_appreciation,
            backstage_pass_zero_appreciation,
            aged_brie_high_sell_in_zero_quality,
            aged_brie_low_sell_in_zero_quality,
            aged_brie_negative_sell_in_zero_quality,
            normal_item_positive_sell_in,
            normal_item_negative_sell_in,
        ]
    )

    gilded_rose.update_items()

    for item in gilded_rose.items:
        assert item.quality <= 50


def test_update_does_not_modify_sell_in_for_legendary_items():
    legendary_item = Item(name="Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)
    gilded_rose = GildedRose(items=[legendary_item])

    gilded_rose.update_items()
    assert gilded_rose.items[0].sell_in == 10


def test_update_keeps_legendary_items_quality_at_80():
    legendary_item = Item(name="Sulfuras, Hand of Ragnaros", sell_in=10, quality=80)
    gilded_rose = GildedRose(items=[legendary_item])

    gilded_rose.update_items()
    assert gilded_rose.items[0].quality == 80


def test_normal_items_degrade_twice_as_fast_after_sell_date():
    normal_item_positive_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=300, quality=50
    )
    normal_item_negative_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=-300, quality=50
    )
    gilded_rose = GildedRose(
        items=[normal_item_positive_sell_in, normal_item_negative_sell_in]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 49
    assert gilded_rose.items[1].quality == 48


def test_conjured_items_degrade_twice_as_fast_as_normal_items():
    normal_item_positive_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=300, quality=50
    )
    normal_item_negative_sell_in = Item(
        name="+5 Dexterity Vest", sell_in=-300, quality=50
    )
    conjured_item_positive_sell_in = Item(
        name="Conjured Mana Cake", sell_in=300, quality=50
    )
    conjured_item_negative_sell_in = Item(
        name="Conjured Mana Cake", sell_in=-300, quality=50
    )

    gilded_rose = GildedRose(
        items=[
            normal_item_positive_sell_in,
            normal_item_negative_sell_in,
            conjured_item_positive_sell_in,
            conjured_item_negative_sell_in,
        ]
    )

    gilded_rose.update_items()

    assert gilded_rose.items[0].quality == 49
    assert gilded_rose.items[1].quality == 48
    assert gilded_rose.items[2].quality == 48
    assert gilded_rose.items[3].quality == 46


if __name__ == "__main__":
    unittest.main()
