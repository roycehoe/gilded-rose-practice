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

---

### Principles followed when writing unit tests

Test cases should follow a predictable structure to improve code readability because [readability counts](https://peps.python.org/pep-0020/). This is the syntax that I have used for my test cases:

1. "test"
2. The name of the method being tested
3. The name of the item group being tested
4. The predicted behaviour
5. The attribute that the predicted behaviour would be applied to
6. Any exceptional cases [Optional]

To improve predictablility, I have decided to deliberately constrain the way I have written my tests. Here are some examples:

- [3] The name of the item group must be held consistent throughout the testing suite; it must also match the name of the item group of the module being tested
- [4] The vocabulary of predicted behaviour should also be predictable. As such, I have constrained myself to use only the following words to describe fluctuations in quality: "keep", "increase", "decrease" in their singular and plural forms
- [6] All exceptional cases appended at the back of my testing functions would be prepended with the word "if" as a signifier that the description of an exceptional case is about to follow

My testing suite also attempts to follow the [principle of least astonishment](https://en.wikipedia.org/wiki/Principle_of_least_astonishment).

The order of my tests was designed with a logical structure. I decided to cluster `sell_in` attribute tests in one block, and `quality` attribute tests in another block. For the `quality` attribute tests, they are further clusered in three logical blocks: Tests of `quality` increase, tests of `quality` remaining constant, and tests of `quality` decreaseing. These blocks are further clusered into item type.

As for the tests themselves, they follow a predictable and logical pattern: Initialise object, apply method on object, assert expected behaviour on object. Each of these logical blocks are separated by a line break to separate logical sections of my code, making it more visually appealing and easier to read.

---

### A final word on clean code

Before signing off, I would like to mention one last thing: Clean code creates good tests, and good code creates clean code. For extra emphasis, let me do that with clap emojis:

Clean 👏 code 👏 creates 👏 good 👏 tests, 👏 and 👏 good 👏 tests 👏 creates 👏 clean 👏 code

Clean code makes it easy to understand the logic behind your code. Understanding the logic behind your code is crucial to write tests, and tests are meant to validate the logic behind your code. The faster you are able to understand your own code, the faster you can write tests.

If a test highlights a bug in your code, a clean code base would shorten the amount of time it takes to resolve the bug.

Lastly, as put succinetly by Bjarne Stroustrup, the inventor of C++, "[clean code] make it hard for bugs to hide".
