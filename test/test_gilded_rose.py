# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose, Item


class GildedRoseTest(unittest.TestCase):
    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals("foo", items[0].name)

    def test_repr_with_correct_arg_ordering(self):
        item = Item("foo", 0, 0)
        assert repr(item) == "foo, 0, 0"


if __name__ == "__main__":
    unittest.main()
