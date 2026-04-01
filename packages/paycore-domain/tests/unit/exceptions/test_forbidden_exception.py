import pytest

from paycore_domain.exceptions import DomainException, ForbiddenException


class TestForbiddenException:
    def test_default_message(self):
        exc = ForbiddenException()
        assert exc.message == "Forbidden"

    def test_custom_message(self):
        exc = ForbiddenException("Access denied to resource")
        assert exc.message == "Access denied to resource"

    def test_code_is_forbidden(self):
        exc = ForbiddenException()
        assert exc.code == "FORBIDDEN"

    def test_permission_included_in_details(self):
        exc = ForbiddenException("Forbidden", permission="admin:write")
        assert exc.details == {"permission": "admin:write"}

    def test_no_permission_means_empty_details(self):
        exc = ForbiddenException()
        assert exc.details == {}

    def test_is_domain_exception(self):
        exc = ForbiddenException()
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(ForbiddenException):
            raise ForbiddenException()
