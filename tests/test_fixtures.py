import pytest

class FancyObject:
    def __init__(self):
        self.fancy = True
        print(f"\nFancyObject: {self.fancy}")
    
    def or_is_it(self):
        self.fancy = not self.fancy

    def cleanup(self):
        print(f"\ncleanup: {self.fancy}")


@pytest.fixture # regster following function as a fixture
def so_fancy():
    fancy_object = FancyObject() # create a new FancyObject instance

    # yield is a Python that lets function suspend themselves so the can resume from the same spot later
    yield fancy_object # temporarily halts the so_fancy function, returning the fancy_object instance
    # code will run when so_fancy function resumes
    fancy_object.cleanup()


@pytest.mark.skip()
def test_so_fancy(so_fancy): # testing the fixture by passing it into the test
    assert so_fancy.fancy
    so_fancy.or_is_it()
    assert not so_fancy.fancy


@pytest.fixture # regster following function as a fixture
def empty_list():
    return []

@pytest.mark.skip()
def test_len_of_empty_list(empty_list):
    assert isinstance(empty_list, list)
    assert len(empty_list) == 0


@pytest.fixture # regster following function as a fixture
def one_item(empty_list):
    empty_list.append("item")
    return empty_list

@pytest.mark.skip()
def test_len_of_unary_list(one_item):
    assert isinstance(one_item, list)
    assert len(one_item) == 1
    assert one_item[0] == "item"