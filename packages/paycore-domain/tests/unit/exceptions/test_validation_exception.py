import pytest

from paycore_domain.exceptions import DomainException, ValidationException


class TestValidationException:
    def test_stores_message(self):
        exc = ValidationException("Invalid email")
        assert exc.message == "Invalid email"

    def test_code_is_validation_error(self):
        exc = ValidationException("Invalid email")
        assert exc.code == "VALIDATION_ERROR"

    def test_field_included_in_details(self):
        exc = ValidationException("Invalid email", field="email")
        assert exc.details["field"] == "email"

    def test_custom_details(self):
        exc = ValidationException("Error", details={"min": 0, "max": 100})
        assert exc.details == {"min": 0, "max": 100}

    def test_field_and_details_combined(self):
        exc = ValidationException("Error", field="age", details={"min": 0})
        assert exc.details == {"min": 0, "field": "age"}

    def test_is_domain_exception(self):
        exc = ValidationException("Invalid")
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(ValidationException):
            raise ValidationException("Invalid email", field="email")
