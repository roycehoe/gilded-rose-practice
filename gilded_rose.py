from enum import Enum

from pydantic import BaseModel, NonNegativeInt

from item import Item

DEXTERITY_VEST = "+5 Dexterity Vest"
AGED_BRIE = "Aged Brie"
ELIXIR = "Elixir of the Mongoose"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
MANA_CAKE = "Conjured Mana Cake"

GOODS_THAT_APPRECIATES_IN_QUALITY = [AGED_BRIE, BACKSTAGE_PASSES]
LEGENDARY_ITEMS = [SULFURAS]


HIGH_PASS_APPRECIATION_SELL_IN = 10
EXTREME_PASS_APPRECIATION_SELL_IN = 5

MAXIMUM_QUALITY = 50
MINIMUM_QUALITY = 0

EXPIRY_THRESHOLD = 0


class PassAppreciationLevel(Enum):
    NORMAL = 0
    HIGH = 1
    EXTREME = 2
    EXPIRED = 3


def get_pass_appreciation_level(sell_in: int) -> PassAppreciationLevel:
    if sell_in > HIGH_PASS_APPRECIATION_SELL_IN:
        return PassAppreciationLevel.NORMAL
    if (
        sell_in <= HIGH_PASS_APPRECIATION_SELL_IN
        and sell_in > EXTREME_PASS_APPRECIATION_SELL_IN
    ):
        return PassAppreciationLevel.HIGH
    if sell_in <= EXTREME_PASS_APPRECIATION_SELL_IN and sell_in > 0:
        return PassAppreciationLevel.EXTREME
    return PassAppreciationLevel.EXPIRED


def will_degrade_in_quality(item: Item) -> bool:
    return (
        item.name not in GOODS_THAT_APPRECIATES_IN_QUALITY
        and item.name not in LEGENDARY_ITEMS
        and item.quality > MINIMUM_QUALITY
    )


def is_expired(sell_in: int) -> bool:
    return sell_in <= EXPIRY_THRESHOLD


def get_item_quality_increase(item: Item) -> int:
    if will_degrade_in_quality(item):
        return -1
    if item.name != BACKSTAGE_PASSES:
        return 1

    pass_appreciation_level = get_pass_appreciation_level(item.sell_in)
    if pass_appreciation_level is PassAppreciationLevel.NORMAL:
        return 1
    if pass_appreciation_level is PassAppreciationLevel.HIGH:
        return 2
    if pass_appreciation_level is PassAppreciationLevel.EXTREME:
        return 3
    if pass_appreciation_level is PassAppreciationLevel.EXPIRED:
        return -item.quality
    raise NotImplementedError


def get_expired_item_quality_increase(item: Item) -> int:
    if item.name not in GOODS_THAT_APPRECIATES_IN_QUALITY:
        if item.quality > 0:
            if item.name not in LEGENDARY_ITEMS:
                return -1
        else:
            return -item.quality
    return item.quality + 1


class GildedRose(BaseModel):
    items: list[Item]

    def update_items(self):
        for item in self.items:
            item.quality = min(
                get_item_quality_increase(item) + item.quality, MAXIMUM_QUALITY
            )

            if item.name not in LEGENDARY_ITEMS:
                item.sell_in = item.sell_in - 1

            if is_expired(item.sell_in):
                item.quality = min(
                    get_expired_item_quality_increase(item) + item.quality,
                    MAXIMUM_QUALITY,
                )
