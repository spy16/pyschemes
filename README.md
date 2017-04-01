# PySchemes
PySchemes is a library for validating data structures in Python. PySchemes is desinged to be simple and Pythonic.

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
```
