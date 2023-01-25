from app.item import Item


def test_item_repr():
    assert repr(Item(name="foo", sell_in=1337, quality=69)) == "foo, 1337, 69"
