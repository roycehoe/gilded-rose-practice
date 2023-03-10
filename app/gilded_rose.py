from pydantic import BaseModel

from app.item import Item
from constants import (
    APPRECIABLE_ITEMS,
    BACKSTAGE_PASSES,
    CONJURED_ITEMS,
    CONJURED_ITEMS_DEPRECIATION_MULTIPLIER,
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

PASS_INFLATION_TO_QUALITY_MULTIPLIER_MAP: dict[QualityInflationMultiplier, int] = {
    QualityInflationMultiplier.NORMAL: 1,
    QualityInflationMultiplier.HIGH: 2,
    QualityInflationMultiplier.EXTREME: 3,
}


def _get_quality_inflation_level(sell_in: int) -> QualityInflationMultiplier:
    if sell_in <= EXPIRY_THRESHOLD:
        return QualityInflationMultiplier.ZERO
    if sell_in <= EXTREME_INFLATION_THRESHOLD:
        return QualityInflationMultiplier.EXTREME
    if sell_in <= HIGH_INFLATION_THRESHOLD:
        return QualityInflationMultiplier.HIGH
    return QualityInflationMultiplier.NORMAL


def _get_appreciable_item_quality_increase(appreciable_item: Item) -> int:
    if appreciable_item.name != BACKSTAGE_PASSES:
        return DEFAULT_APPRECIATION

    backstage_pass_inflation_level = _get_quality_inflation_level(
        appreciable_item.sell_in
    )
    multiplier = PASS_INFLATION_TO_QUALITY_MULTIPLIER_MAP.get(
        backstage_pass_inflation_level, -appreciable_item.quality
    )
    return DEFAULT_APPRECIATION * multiplier


def _get_item_quality_increase(item: Item) -> int:
    if item.name in CONJURED_ITEMS:
        return DEFAULT_DEPRECIATION * CONJURED_ITEMS_DEPRECIATION_MULTIPLIER

    if item.name not in APPRECIABLE_ITEMS:
        return DEFAULT_DEPRECIATION

    if item.name != BACKSTAGE_PASSES:
        return DEFAULT_APPRECIATION

    quality_increase = _get_appreciable_item_quality_increase(item)
    return quality_increase


def _is_item_expired(sell_in: int) -> bool:
    return sell_in <= EXPIRY_THRESHOLD


def _get_expired_item_quality_increase(item: Item) -> int:
    if item.name == BACKSTAGE_PASSES:
        return -item.quality
    if item.name in APPRECIABLE_ITEMS:
        return item.quality + DEFAULT_APPRECIATION
    if item.name in CONJURED_ITEMS:
        return DEFAULT_DEPRECIATION * CONJURED_ITEMS_DEPRECIATION_MULTIPLIER

    return DEFAULT_DEPRECIATION


class GildedRose(BaseModel):
    items: list[Item]

    def update_items(self) -> None:
        for item in self.items:
            self._update_item(item)

    def _update_item(self, item: Item) -> None:
        if item.name in LEGENDARY_ITEMS:
            return
        item.quality = clamp(
            _get_item_quality_increase(item) + item.quality,
            MINIMUM_QUALITY,
            MAXIMUM_QUALITY,
        )

        item.sell_in = item.sell_in - 1

        if not _is_item_expired(item.sell_in):
            return
        item.quality = clamp(
            _get_expired_item_quality_increase(item) + item.quality,
            MINIMUM_QUALITY,
            MAXIMUM_QUALITY,
        )
