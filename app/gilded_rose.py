from pydantic import BaseModel

from app.item import Item
from constants import (
    APPRECIABLE_ITEMS,
    BACKSTAGE_PASSES,
    DEFAULT_APPRECIATION,
    DEFAULT_DEPRECIATION,
    EXPIRY_THRESHOLD,
    EXTREME_INFLATION_THRESHOLD,
    HIGH_INFLATION_THRESHOLD,
    LEGENDARY_ITEMS,
    MAXIMUM_QUALITY,
    MINIMUM_QUALITY,
)
from enums import QualityInflationMultiplier
from utils import clamp

PASS_INFLATION_TO_QUALITY_INCREASE_MULTIPLIER_MAP: dict[
    QualityInflationMultiplier, int
] = {
    QualityInflationMultiplier.NORMAL: 1,
    QualityInflationMultiplier.HIGH: 2,
    QualityInflationMultiplier.EXTREME: 3,
}


def _get_pass_inflation_level(sell_in: int) -> QualityInflationMultiplier:
    if sell_in <= EXPIRY_THRESHOLD:
        return QualityInflationMultiplier.ZERO
    if sell_in <= EXTREME_INFLATION_THRESHOLD:
        return QualityInflationMultiplier.EXTREME
    if sell_in <= HIGH_INFLATION_THRESHOLD:
        return QualityInflationMultiplier.HIGH
    return QualityInflationMultiplier.NORMAL


def _will_degrade_in_quality(item: Item) -> bool:
    if item.name in LEGENDARY_ITEMS:
        return False
    if item.name in APPRECIABLE_ITEMS:
        return False
    return True


def _get_item_quality_increase(item: Item) -> int:
    if _will_degrade_in_quality(item):
        return DEFAULT_DEPRECIATION
    if item.name != BACKSTAGE_PASSES:
        return DEFAULT_APPRECIATION

    pass_inflation_level = _get_pass_inflation_level(item.sell_in)
    multiplier = PASS_INFLATION_TO_QUALITY_INCREASE_MULTIPLIER_MAP.get(
        pass_inflation_level, -item.quality
    )
    return DEFAULT_APPRECIATION * multiplier


def _is_item_expired(sell_in: int) -> bool:
    return sell_in <= EXPIRY_THRESHOLD


def _get_expired_item_quality_increase(item: Item) -> int:
    if item.name in LEGENDARY_ITEMS:
        return 0
    if item.name == BACKSTAGE_PASSES:
        return -item.quality
    if item.name in APPRECIABLE_ITEMS:
        return item.quality + 1

    return -1


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
