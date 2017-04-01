"""Schema Validation."""

from .validators import Validator


class Schema(object):
    """Schema Validator."""

    def __init__(self, scheme):
        self.validator = Validator.create_validator(scheme)

    def validate(self, value):
        return self.validator.validate(value)
