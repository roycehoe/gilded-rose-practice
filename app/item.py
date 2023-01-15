from typing import Annotated

from pydantic import BaseModel, NonNegativeInt

from constants import MINIMUM_QUALITY


class Item(BaseModel):
    name: str
    sell_in: int
    quality: NonNegativeInt

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"
