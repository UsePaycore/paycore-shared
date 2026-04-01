import pytest

from paycore_domain.exceptions import ConflictException, DomainException


class TestConflictException:
    def test_stores_message(self):
        exc = ConflictException("Resource already exists")
        assert exc.message == "Resource already exists"

    def test_code_is_conflict(self):
        exc = ConflictException("Conflict")
        assert exc.code == "CONFLICT"

    def test_default_details_is_empty(self):
        exc = ConflictException("Conflict")
        assert exc.details == {}

    def test_custom_details(self):
        exc = ConflictException("Conflict", details={"field": "email"})
        assert exc.details == {"field": "email"}

    def test_is_domain_exception(self):
        exc = ConflictException("Conflict")
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(ConflictException):
            raise ConflictException("Resource already exists")
