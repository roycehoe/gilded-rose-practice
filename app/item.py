from typing import Annotated

from pydantic import BaseModel, conint

from constants import MAXIMUM_QUALITY, MINIMUM_QUALITY


class Item(BaseModel):
    name: str
    sell_in: int
    quality: Annotated[int, conint(ge=MINIMUM_QUALITY, le=MAXIMUM_QUALITY)]

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"
