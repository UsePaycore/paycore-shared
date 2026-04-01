from dataclasses import dataclass

from paycore_domain.cqrs import Command


@dataclass(frozen=True)
class CreateUserCommand(Command):
    name: str
    email: str


class TestCommand:
    def test_is_frozen_dataclass(self):
        cmd = CreateUserCommand(name="Alice", email="alice@example.com")
        try:
            cmd.name = "Bob"
            assert False, "Should not reach here"
        except AttributeError:
            pass

    def test_stores_fields(self):
        cmd = CreateUserCommand(name="Alice", email="alice@example.com")
        assert cmd.name == "Alice"
        assert cmd.email == "alice@example.com"

    def test_equal_commands_are_equal(self):
        cmd1 = CreateUserCommand(name="Alice", email="alice@example.com")
        cmd2 = CreateUserCommand(name="Alice", email="alice@example.com")
        assert cmd1 == cmd2

    def test_different_commands_are_not_equal(self):
        cmd1 = CreateUserCommand(name="Alice", email="alice@example.com")
        cmd2 = CreateUserCommand(name="Bob", email="bob@example.com")
        assert cmd1 != cmd2
