from enum import Enum

from pydantic import BaseModel

from constants import (
    BACKSTAGE_PASSES,
    EXPIRY_THRESHOLD,
    EXTREME_PASS_APPRECIATION_FLOOR,
    GOODS_THAT_APPRECIATES_IN_QUALITY,
    HIGH_PASS_APPRECIATION_FLOOR,
    LEGENDARY_ITEMS,
    MAXIMUM_QUALITY,
    MINIMUM_QUALITY,
)
from enums import PassAppreciationLevel
from item import Item
from utils import clamp


def _get_pass_appreciation_level(sell_in: int) -> PassAppreciationLevel:
    if sell_in > HIGH_PASS_APPRECIATION_FLOOR:
        return PassAppreciationLevel.NORMAL
    if sell_in > EXTREME_PASS_APPRECIATION_FLOOR:
        return PassAppreciationLevel.HIGH
    if sell_in > 0:
        return PassAppreciationLevel.EXTREME
    return PassAppreciationLevel.EXPIRED


def _will_degrade_in_quality(item: Item) -> bool:
    return (
        item.name not in GOODS_THAT_APPRECIATES_IN_QUALITY
        and item.name not in LEGENDARY_ITEMS
        and item.quality > MINIMUM_QUALITY
    )


def _is_item_expired(sell_in: int) -> bool:
    return sell_in <= EXPIRY_THRESHOLD


def _get_item_quality_increase(item: Item) -> int:
    if _will_degrade_in_quality(item):
        return -1
    if item.name != BACKSTAGE_PASSES:
        return 1

    pass_appreciation_level = _get_pass_appreciation_level(item.sell_in)

    if pass_appreciation_level is PassAppreciationLevel.NORMAL:
        return 1
    if pass_appreciation_level is PassAppreciationLevel.HIGH:
        return 2
    if pass_appreciation_level is PassAppreciationLevel.EXTREME:
        return 3
    return -item.quality


def _get_expired_item_quality_increase(item: Item) -> int:
    if item.name not in GOODS_THAT_APPRECIATES_IN_QUALITY:
        if item.quality > 0 and item.name not in LEGENDARY_ITEMS:
            return -1
        return -item.quality

    return item.quality + 1


class GildedRose(BaseModel):
    items: list[Item]

    def update_items(self):
        for item in self.items:
            self.update_item(item)

    def update_item(self, item: Item):
        item.quality = clamp(
            _get_item_quality_increase(item) + item.quality,
            MINIMUM_QUALITY,
            MAXIMUM_QUALITY,
        )

        if item.name not in LEGENDARY_ITEMS:
            item.sell_in = item.sell_in - 1

        if _is_item_expired(item.sell_in):
            item.quality = clamp(
                _get_expired_item_quality_increase(item) + item.quality,
                MINIMUM_QUALITY,
                MAXIMUM_QUALITY,
            )
