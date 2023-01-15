# Test checklist

## General cases

- [x] The system lowers both sell in and Quality values for every item
- [x] Once the sell by date has passed, Quality degrades twice as fast
- [x] The Quality of an item is never negative [Guaranteed by Pydantic]
- [x] The Quality of an item is never more than 50

## Exceptional cases

- [x] "Aged Brie" actually increases in Quality the older it gets

- [x] "Sulfuras", being a legendary item, never has to be sold or decreases in Quality

- [x] "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
- [x] Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but quality drops to 0 after the concert

- [x] "Conjured" items degrade in Quality twice as fast as normal items

- [x] An item can never have its Quality increase above 50, however "Sulfuras" is a legendary item and as such its Quality is 80 and it never alters.
