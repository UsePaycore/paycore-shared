import pytest

from paycore_domain.exceptions import BusinessRuleException, DomainException


class TestBusinessRuleException:
    def test_rule_is_used_as_message_when_no_message(self):
        exc = BusinessRuleException("max_overdraft_exceeded")
        assert exc.message == "max_overdraft_exceeded"

    def test_custom_message_overrides_rule(self):
        exc = BusinessRuleException("max_overdraft", message="Overdraft limit exceeded")
        assert exc.message == "Overdraft limit exceeded"

    def test_code_is_business_rule_violation(self):
        exc = BusinessRuleException("some_rule")
        assert exc.code == "BUSINESS_RULE_VIOLATION"

    def test_details_include_rule(self):
        exc = BusinessRuleException("max_overdraft")
        assert exc.details["rule"] == "max_overdraft"

    def test_custom_details_merged_with_rule(self):
        exc = BusinessRuleException("max_overdraft", details={"limit": 500})
        assert exc.details == {"limit": 500, "rule": "max_overdraft"}

    def test_is_domain_exception(self):
        exc = BusinessRuleException("some_rule")
        assert isinstance(exc, DomainException)

    def test_can_be_raised_and_caught(self):
        with pytest.raises(BusinessRuleException):
            raise BusinessRuleException("some_rule")
