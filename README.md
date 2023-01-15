# Gilded Rose: Refactoring exercise

Original code: <https://github.com/emilybache/GildedRose-Refactoring-Kata/tree/main/python>

Junior Developers SG event: <https://www.meetup.com/junior-developers-singapore/events/290662218/>

Special thanks to Nik Tay for making me a PITA when it comes to naming stuff; Don Norman for making me a PITA when it comes to designing stuff, and Junior Developers Singapore for making me spend my weekend doing literally what I do at work.

In all, this exercise was fun. For context, I have been explicitly told not to unit test at work (so that we can "move fast"), so this was definitely a great revision. 10/10 would burn my weekend again.

---

## Testing checklist

### General cases

- [x] The system lowers both sell in and Quality values for every item
- [x] Once the sell by date has passed, Quality degrades twice as fast
- [x] The Quality of an item is never negative [Guaranteed by Pydantic]
- [x] The Quality of an item is never more than 50

### Exceptional cases

- [x] "Aged Brie" actually increases in Quality the older it gets
- [x] "Sulfuras", being a legendary item, never has to be sold or decreases in Quality
- [x] "Backstage passes", like aged brie, increases in Quality as its SellIn value approaches;
- [x] Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but quality drops to 0 after the concert
- [x] "Conjured" items degrade in Quality twice as fast as normal items
- [x] An item can never have its Quality increase above 50, however "Sulfuras" is a legendary item and as such its Quality is 80 and it never alters.
