from paycore_domain.exceptions import DomainException


class TestDomainException:
    def test_stores_message(self):
        exc = DomainException("Something went wrong")
        assert exc.message == "Something went wrong"

    def test_default_code_is_class_name(self):
        exc = DomainException("Something went wrong")
        assert exc.code == "DomainException"

    def test_custom_code(self):
        exc = DomainException("Error", code="CUSTOM_CODE")
        assert exc.code == "CUSTOM_CODE"

    def test_default_details_is_empty_dict(self):
        exc = DomainException("Error")
        assert exc.details == {}

    def test_custom_details(self):
        details = {"field": "email"}
        exc = DomainException("Error", details=details)
        assert exc.details == details

    def test_to_dict(self):
        exc = DomainException("Something went wrong", code="ERR", details={"key": "val"})
        result = exc.to_dict()
        assert result == {
            "error": "ERR",
            "message": "Something went wrong",
            "details": {"key": "val"},
        }

    def test_is_exception(self):
        exc = DomainException("Error")
        assert isinstance(exc, Exception)

    def test_str_is_message(self):
        exc = DomainException("Something went wrong")
        assert str(exc) == "Something went wrong"
