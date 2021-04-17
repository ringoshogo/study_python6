import api

def test_get_item_list_1():
    """返却値の型をチェックする"""
    res = api.get_item_list()
    assert type(res) == list

def test_get_item_list_2():
    """返却値の要素数"""
    res = api.get_item_list()
    assert len(res[0]) == 2


