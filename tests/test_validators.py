"""Test Validators."""


import pytest
from collections import Mapping, Iterable
from types import FunctionType
from pyschemes.validators import TypeValidator, LengthValidator, ValueValidator
from pyschemes.validators import CallableValidator, All, Any, Optional
from pyschemes.validators import IterableValidator, MappingValidator
from pyschemes.validators import IterableValidator, RegexValidator


def test_type_validator():
    TypeValidator(int).validate(10)
    TypeValidator(float).validate(10.3)
    TypeValidator(str).validate("hello world")
    TypeValidator(dict).validate({})
    TypeValidator(FunctionType).validate(lambda x: x)
    TypeValidator(Iterable).validate([])
    TypeValidator(Mapping).validate({})
    with pytest.raises(TypeError):
        TypeValidator(FunctionType).validate(None)
        TypeValidator(int).validate(10.3)


def test_length_validator():
    LengthValidator(10).validate(range(10))
    with pytest.raises(ValueError):
        LengthValidator(10).validate(range(20))


def test_value_validator():
    ValueValidator({}).validate({})
    ValueValidator(10).validate(10)
    ValueValidator(["hello", "world"]).validate(["hello", "world"])
    with pytest.raises(ValueError):
        ValueValidator(10).validate(100)


def test_callable_validator():
    CallableValidator(lambda x: x < 10).validate(9)
    with pytest.raises(ValueError):
        CallableValidator(lambda x: x < 10).validate(10)


def test_All():
    tests = [int, 6]
    All(tests).validate(6)
    with pytest.raises(ValueError):
        All(tests).validate(10)
    with pytest.raises(TypeError):
        All(tests).validate(10.5)


def test_Any():
    must_be_number = [int, float, complex]
    Any(must_be_number).validate(1+2j)
    Any(must_be_number).validate(1)
    Any(must_be_number).validate(1.6)
    with pytest.raises(ValueError):
        Any(must_be_number).validate("hello")


def test_Iterable_validator():
    schema = [str, int, Any([2, 3, 4])]
    IterableValidator(schema).validate(["hello", 2, 4])
    with pytest.raises(ValueError):
        IterableValidator(schema).validate(["hello", 2, 5])
    with pytest.raises(TypeError):
        IterableValidator(schema).validate([10, 2, 4])


def test_optional_validator():
    optional = Optional(str, "hello")
    assert optional.validate("world") == "world"
    assert optional.validate() == "hello"
    with pytest.raises(TypeError):
        optional.validate(10)


def test_mapping_validator():
    map_scheme = {
        "height": All([Any([int, float]), lambda x: x < 8]),
        "name": str,
        "phone": All([str, lambda x: len(x) == 10]),
        "likes": Optional({
            str: str
        }, {})
    }
    MappingValidator(map_scheme).validate({
        "height": 6.7,
        "name": "bob",
        "phone": "0123456789",
        "likes": {
            "movie": "Inglourius Basterds"
        }
    })
    with pytest.raises(ValueError):
        MappingValidator(map_scheme).validate({
            "name": "bob",
            "phone": "0123456789"
        })
    with pytest.raises(TypeError):
        MappingValidator(map_scheme).validate({
            "name": "bob",
            "phone": 1234567890
        })
    with pytest.raises(ValueError):
        MappingValidator(map_scheme).validate({
            "name": "bob",
            "phone": "1234567890",
            "balh-not-allowed": "hello"
        })



def test_regex_validator():
    pattern = r"\w+\d+\w+"  # e.g. hello4world
    RegexValidator(pattern).validate("hello4world")
    with pytest.raises(ValueError):
        RegexValidator(pattern).validate("helloworld")
    with pytest.raises(TypeError):
        RegexValidator(pattern).validate([1,2,3])
