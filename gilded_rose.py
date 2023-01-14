from enum import Enum

from pydantic import BaseModel, NonNegativeInt

DEXTERITY_VEST = "+5 Dexterity Vest"
AGED_BRIE = "Aged Brie"
ELIXIR = "Elixir of the Mongoose"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
MANA_CAKE = "Conjured Mana Cake"

GOODS_THAT_AGE_WELL = [AGED_BRIE, BACKSTAGE_PASSES]
LEGENDARY_ITEMS = [SULFURAS]


HIGH_TICKET_APPRECIATION_SELL_IN = 10
EXTREME_TICKET_APPRECIATION_SELL_IN = 5


class NonNegativeSellInValue(Exception):
    pass


class TicketAppreciationLevel(Enum):
    NORMAL = 0
    HIGH = 1
    EXTREME = 2
    EXPIRED = 3


def get_ticket_appreciation_level(sell_in: int) -> TicketAppreciationLevel:
    if sell_in > HIGH_TICKET_APPRECIATION_SELL_IN:
        return TicketAppreciationLevel.NORMAL
    if sell_in <= HIGH_TICKET_APPRECIATION_SELL_IN:
        return TicketAppreciationLevel.HIGH
    if sell_in <= EXTREME_TICKET_APPRECIATION_SELL_IN:
        return TicketAppreciationLevel.EXTREME
    if sell_in == 0:
        return TicketAppreciationLevel.EXPIRED
    raise NonNegativeSellInValue


class Item(BaseModel):
    name: str
    sell_in: int
    quality: NonNegativeInt

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"


class GildedRose(BaseModel):
    items: list[Item]

    def update_quality(self):
        for item in self.items:
            if (
                item.name not in GOODS_THAT_AGE_WELL
                and item.name not in LEGENDARY_ITEMS
                and item.quality > 0
            ):
                item.quality = item.quality - 1

            else:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.name == BACKSTAGE_PASSES:
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1

            if item.name not in LEGENDARY_ITEMS:
                item.sell_in = item.sell_in - 1

            if item.sell_in < 0:
                if item.name not in GOODS_THAT_AGE_WELL:
                    if item.quality > 0:
                        if item.name not in LEGENDARY_ITEMS:
                            item.quality = item.quality - 1
                    else:
                        item.quality = item.quality - item.quality
                else:
                    if item.quality < 50:
                        item.quality = item.quality + 1
