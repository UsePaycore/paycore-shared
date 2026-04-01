import pytest

from paycore_domain.exceptions import DomainException, NotFoundException


class TestNotFoundException:
    def test_message_with_entity_id(self):
        exc = NotFoundException("User", "abc-123")
        assert exc.message == "User with id 'abc-123' not found"

    def test_message_without_entity_id(self):
        exc = NotFoundException("User not found in the system")
        assert exc.message == "User not found in the system"

    def test_code_is_not_found(self):
        exc = NotFoundException("User", "abc-123")
        assert exc.code == "NOT_FOUND"

    def test_details_include_entity_info(self):
        exc = NotFoundException("User", "abc-123")
        assert exc.details == {"entity_type": "User", "entity_id": "abc-123"}

    def test_details_empty_without_entity_id(self):
        exc = NotFoundException("Something missing")
        assert exc.details == {}

    def test_is_domain_exception(self):
        exc = NotFoundException("User", "abc-123")
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(NotFoundException):
            raise NotFoundException("User", "abc-123")
