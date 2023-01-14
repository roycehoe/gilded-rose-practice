from pydantic import BaseModel

from app.item import Item
from constants import (
    BACKSTAGE_PASSES,
    EXPIRY_THRESHOLD,
    EXTREME_INFLATION_THRESHOLD,
    GOODS_THAT_APPRECIATES_IN_QUALITY,
    HIGH_INFLATION_THRESHOLD,
    LEGENDARY_ITEMS,
    MAXIMUM_QUALITY,
    MINIMUM_QUALITY,
)
from enums import PassInflationLevel
from utils import clamp


def _get_pass_inflation_level(sell_in: int) -> PassInflationLevel:
    if sell_in > HIGH_INFLATION_THRESHOLD:
        return PassInflationLevel.NORMAL
    if sell_in > EXTREME_INFLATION_THRESHOLD:
        return PassInflationLevel.HIGH
    if sell_in > 0:
        return PassInflationLevel.EXTREME
    return PassInflationLevel.EXPIRED


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

    pass_inflation_level = _get_pass_inflation_level(item.sell_in)

    if pass_inflation_level is PassInflationLevel.NORMAL:
        return 1
    if pass_inflation_level is PassInflationLevel.HIGH:
        return 2
    if pass_inflation_level is PassInflationLevel.EXTREME:
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
