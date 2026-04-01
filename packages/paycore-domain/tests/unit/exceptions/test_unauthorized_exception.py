import pytest

from paycore_domain.exceptions import DomainException, UnauthorizedException


class TestUnauthorizedException:
    def test_default_message(self):
        exc = UnauthorizedException()
        assert exc.message == "Unauthorized"

    def test_custom_message(self):
        exc = UnauthorizedException("Token expired")
        assert exc.message == "Token expired"

    def test_code_is_unauthorized(self):
        exc = UnauthorizedException()
        assert exc.code == "UNAUTHORIZED"

    def test_is_domain_exception(self):
        exc = UnauthorizedException()
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(UnauthorizedException):
            raise UnauthorizedException()
