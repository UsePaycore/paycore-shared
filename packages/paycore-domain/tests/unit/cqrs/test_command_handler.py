from dataclasses import dataclass

from paycore_domain.cqrs import Command, CommandHandler


@dataclass(frozen=True)
class GreetCommand(Command):
    name: str


class GreetCommandHandler(CommandHandler[GreetCommand, str]):
    def handle(self, command: GreetCommand) -> str:
        return f"Hello, {command.name}!"


class TestCommandHandler:
    def test_handle_returns_result(self):
        handler = GreetCommandHandler()
        result = handler.handle(GreetCommand(name="Alice"))
        assert result == "Hello, Alice!"

    def test_handle_with_different_input(self):
        handler = GreetCommandHandler()
        result = handler.handle(GreetCommand(name="Bob"))
        assert result == "Hello, Bob!"
