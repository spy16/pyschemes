# PySchemes
PySchemes is a library for validating data structures in Python. PySchemes is designed to be simple and Pythonic.

![https://travis-ci.org/shivylp/pyschemes](https://secure.travis-ci.org/shivylp/pyschemes.svg?branch=master)



## Features
* Simple representation of schema using primitive Python types (Or Complex types as well)
* Sane Schema Structures
* Sane errors
* Power of PySchemes lies in its validators (take a look at tests to understand usage of various validators)
* Lambda functions or any callable can be easily used as a validator

## Examples

```python
# Execute this before executing any of the examples
>>> from pyschemes import Scheme, validators
```

1. Simple TypeChecking
```python
>>> Scheme(int).validate(10)
10

>>> Scheme(int).validate(10.3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: expected type: 'int', got 'float'

>>> from collections import Iterable
>>> Scheme(Iterable).validate([1, 2])
[1, 2]

>>> Scheme(Iterable).validate(("hello", ))
("hello", )

>>> Scheme(Iterable).validate({"a": "b", "c": "d"})
{"a": "b", "c": "d"}

>>> Scheme(Iterable).validate(range(100))
range(0, 100)

>>> Scheme(Iterable).validate(lambda x: x)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: expected type: 'Iterable', got 'function'
```

2. Simple Value Validation
```python
>>> Scheme(10).validate(10)
10

>>> Scheme(10).validate(10.3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: expected value '10', got '10.3'
```

3. Simple Choices Validation
```python
>>> choices = validators.Any(["choiceA", "choiceB", "choiceC"])

>>> Scheme(choices).validate("choiceA")
'choiceA'

>>> Scheme(choices).validate("hello")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: value did not pass any validation
```

4. Validating a List/Iterable Scheme

```python
>>> Scheme([str, 2, int]).validate(["hello", 2, 15])
["hello", 2, 15]

>>> Scheme((str, 2, int)).validate(("hello", 2, 15))
("hello", 2, 15)

>>> Scheme((str, 2, int)).validate(["hello", 2, 15])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: expected type: 'tuple', got 'list'

>>> Scheme([str, 2, int]).validate(["hello", 3, 130])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: element at index 1 (expected value '2', got '3')

>>> Scheme([str, 2, int]).validate(["hello", 2, 4.5])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: element at index 2 (expected type: 'int', got 'float')
```


5. Validating a Dictionary/Mapping Scheme
```python
>>> Scheme({str: int}).validate({"a": 1, "b": 2})
{'a': 1, 'b': 2}

>>> Scheme({str: int}).validate({"a": 1, "b": 3.5})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: at key 'b' (expected type: 'int', got 'float')

>>> Scheme({"hello": 10, str: object}).validate({"hello": 10, "world": 12})
{"hello": 10, "world": 12}

>>> Scheme({"required-key": int}).validate({})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: missing key 'required-key'

>>> from pyschemes.validators import Optional
>>> Scheme({"k": Optional(str, "hello")}).validate({})
{'k': 'hello'}

>>> Scheme({"k": Optional(str, "hello")}).validate({"k": "world"})
{'k': 'world'}

>>> Scheme({"k": Optional(int, 10)}).validate({"k": "world"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: at key 'k' (expected type: 'int', got 'str')

>>> Scheme({"only-key": str}).validate({"only-key": "hello", "b": "not-allowed"})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: at key 'b' (not allowed)
```


6. Lambda/Callable Scheme
```python
>>> Scheme(lambda x: x < 100).validate(10)
10

>>> Scheme(lambda x: x < 100).validate(101)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: validator '<lambda>' failed for value '101'

>>> def CustomValidator(value):
...    if value == "foo" or value in range(100):
...       return value
...    else:
...       return False
...
>>> Scheme(CustomValidator).validate(101)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: validator 'CustomValidator' failed for value '10'

>>> Scheme(CustomValidator).validate(9)
9
>>> Scheme(CustomValidator).validate("foo")
'foo'
```


7. Compund Schemes
```python
>>> Scheme({"test": lambda x: x < 100}).validate({"test": 10})
{'test': 10}

>>> Scheme({"test": lambda x: x < 100}).validate({"test": 101})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: at key 'test' (validator '<lambda>' failed for value '101')

>>> Scheme({"test": Scheme({"a": str, "b": int})}).validate({"test": {}})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: at key 'test' (missing key 'a')

>>> Scheme({"test": Scheme({"b": int})}).validate({"test": {"b": 1.5}})
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: at key 'test' (at key 'b' (expected type: 'int', got 'float'))

>>> Scheme({"t": {str: int}}).validate({"t": {"a": 1}})
{'t': {'a': 1}}

>>> Scheme({"t": (str, int)}).validate({"t": ("a", 1)})
{'t': ('a', 1)}
```

And more to come in tests!
