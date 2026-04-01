from paycore_domain.value_objects.primitives import ValueObject


class ConcreteValueObject(ValueObject):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age


class OtherValueObject(ValueObject):
    def __init__(self, name: str) -> None:
        self.name = name


class TestValueObject:
    def test_equal_objects_are_equal(self):
        vo1 = ConcreteValueObject("Alice", 30)
        vo2 = ConcreteValueObject("Alice", 30)
        assert vo1 == vo2

    def test_different_objects_are_not_equal(self):
        vo1 = ConcreteValueObject("Alice", 30)
        vo2 = ConcreteValueObject("Bob", 25)
        assert vo1 != vo2

    def test_not_equal_to_different_type(self):
        vo = ConcreteValueObject("Alice", 30)
        assert vo != "Alice"

    def test_not_equal_to_different_value_object_class(self):
        vo1 = ConcreteValueObject("Alice", 30)
        vo2 = OtherValueObject("Alice")
        assert vo1 != vo2

    def test_equal_objects_have_same_hash(self):
        vo1 = ConcreteValueObject("Alice", 30)
        vo2 = ConcreteValueObject("Alice", 30)
        assert hash(vo1) == hash(vo2)

    def test_can_be_used_in_set(self):
        vo1 = ConcreteValueObject("Alice", 30)
        vo2 = ConcreteValueObject("Alice", 30)
        vo3 = ConcreteValueObject("Bob", 25)
        result = {vo1, vo2, vo3}
        assert len(result) == 2
