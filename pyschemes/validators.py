import abc
import collections


COMPARABLE, CALLABLE, VALIDATOR, TYPE, DICT, ITERABLE = range(6)


def get_entry_type(s):
    """Return entry type for a given entry."""
    if type(s) in (list, tuple, set, frozenset):
        return ITERABLE
    if type(s) is dict:
        return DICT
    if issubclass(type(s), type):
        return TYPE
    if hasattr(s, 'validate'):
        return VALIDATOR
    if callable(s):
        return CALLABLE
    else:
        return COMPARABLE


class Validator(object):

    def __init__(self, scheme):
        self.scheme = scheme

    def __call__(self, value):
        return self.validate(value)

    def validate(self, value):
        raise NotImplementedError("{}.{}(value)".format(
            self.__class__.__name__, "validate"))

    @staticmethod
    def create_validator(spec):
        _type = get_entry_type(spec)
        if _type is ITERABLE:
            return IterableSchemeValidator(spec)
        elif _type is VALIDATOR:
            return spec
        elif _type is DICT:
            return MappingValidator(spec)
        elif _type is TYPE:
            return TypeValidator(spec)
        elif _type is CALLABLE:
            return CallableValidator(spec)
        elif _type is COMPARABLE:
            return ValueValidator(spec)


class CallableValidator(Validator):

    def __init__(self, _callable, fail_flag=False):
        self._callable = _callable
        self.fail_flag = fail_flag

    def validate(self, value):
        result = self._callable(value)
        if result == self.fail_flag:
            msg = "validator '{}' failed for value '{}'"
            raise ValueError(msg.format(self._callable.__name__, value))
        return value


class TypeValidator(Validator):

    def __init__(self, _type):
        if type(_type) not in [type, abc.ABCMeta]:
            raise TypeError("'_type' must be a type")
        self._type = _type

    def validate(self, value):
        if isinstance(value, self._type):
            return value
        else:
            msg = "expected type: '{}', got '{}'"
            expected = self._type.__name__
            actual = type(value).__name__
            raise TypeError(msg.format(expected, actual))


class LengthValidator(Validator):

    def __init__(self, length):
        self.length = length

    def validate(self, value):
        actual = len(value)
        if actual != self.length:
            raise ValueError("expected length '{}', got '{}'".format(
                self.length, actual
            ))
        return value


class ValueValidator(Validator):

    def validate(self, value):
        if value != self.scheme:
            raise ValueError("expected value '{}', got '{}'".format(
                self.scheme, value))
        return value


class All(Validator):
    """Check that all validators pass."""

    def __init__(self, schemes):
        TypeValidator(collections.Iterable).validate(schemes)
        self.__schemes = []
        for scheme in schemes:
            self.__schemes.append(Validator.create_validator(scheme))

    def validate(self, value):
        for scheme in self.__schemes:
            scheme.validate(value)
        return value


class Any(Validator):
    """Check if any value is valid as per any one scheme"""

    def __init__(self, schemes):
        TypeValidator(collections.Iterable).validate(schemes)
        self.__schemes = []
        for scheme in schemes:
            self.__schemes.append(Validator.create_validator(scheme))

    def validate(self, value):
        for scheme in self.__schemes:
            try:
                scheme.validate(value)
                return value
            except Exception:
                pass
        raise ValueError("value did not pass any validation")


class IterableSchemeValidator(Validator):

    def __init__(self, iterable, ignore_type=False):
        self.__iterable = iterable
        self.__type = object
        if not ignore_type:
            self.__type = type(iterable)
        if not isinstance(iterable, collections.Iterable):
            raise TypeError("'iterable' must be an iterable")

    def validate(self, value):
        validated = []
        TypeValidator(self.__type).validate(value)
        LengthValidator(len(self.__iterable)).validate(value)
        for i in range(len(self.__iterable)):
            item = self.__iterable[i]
            try:
                if type(item) is type:
                    validated_value = TypeValidator(item).validate(value[i])
                else:
                    validated_value = ValueValidator(item).validate(value[i])
            except Exception as ex:
                raise type(ex)("element at index {} ({})".format(i, ex))
            validated.append(validated_value)
        return type(value)(validated)  # return value of sample type


class Optional(Validator):
    """Optional Scheme."""

    def __init__(self, _type, default):
        self.__scheme = TypeValidator(_type)
        self.default = default

    def validate(self, *value):
        if len(value) > 0:
            val = value[0]
            return self.__scheme.validate(val)
        return self.default



class MappingValidator(Validator):

    def __init__(self, mapping, ignore_unknown=False):
        TypeValidator(collections.Mapping).validate(mapping)
        self.__mapping = dict(mapping)
        self.ignore_unknown = ignore_unknown

    def validate(self, value):
        TypeValidator(collections.Mapping).validate(value)
        for k, v in value.items():
            try:
                key_type = type(k)
                value_rule = self.__mapping.get(k, None)
                if value_rule:
                    validator = Validator.create_validator(value_rule)
                else:
                    type_rule = self.__mapping.get(key_type, None)
                    if type_rule is None:
                        if self.ignore_unknown is False:
                            raise ValueError("not allowed")
                    else:
                        validator = Validator.create_validator(type_rule)
                validator.validate(v)
            except Exception as ex:
                raise type(ex)("at key '{}' ({})".format(
                    k, ex
                ))
        for k in self.__mapping:
            _type = get_entry_type(k)
            if _type is COMPARABLE:
                if k not in value:
                    expected = self.__mapping.get(k, None)
                    if isinstance(expected, Optional):
                        value[k] = expected.default
                    else:
                        raise ValueError("missing key '{}'".format(k))
        return value
