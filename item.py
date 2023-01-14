from pydantic import BaseModel, NonNegativeInt


class Item(BaseModel):
    name: str
    sell_in: int
    quality: NonNegativeInt

    def __repr__(self):
        return f"{self.name}, {self.sell_in}, {self.quality}"
