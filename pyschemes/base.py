"""Schema Validation."""

from .validators import Validator


class Scheme(object):
    """Scheme Validator."""

    def __init__(self, scheme_spec):
        self.validator = Validator.create_validator(scheme_spec)

    def validate(self, value):
        return self.validator.validate(value)
