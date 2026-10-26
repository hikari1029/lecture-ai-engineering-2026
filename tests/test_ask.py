"""素のLLMとの対話テスト（Google APIは呼ばない）。"""

import sys
from types import SimpleNamespace

from app import ask as ask_module


def test_main_keeps_chat_history_between_questions(monkeypatch, capsys):
    sent_messages = []

    class Chat:
        def send_message(self, message):
            sent_messages.append(message)
            return SimpleNamespace(text=f"回答: {message}")

    chat = Chat()
    fake_client = SimpleNamespace(chats=SimpleNamespace(create=lambda model: chat))
    monkeypatch.setattr(ask_module.genai, "Client", lambda api_key: fake_client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(sys, "argv", ["app.ask", "最初の質問"])
    answers = iter(["続きの質問", ""])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    ask_module.main()

    assert sent_messages == ["最初の質問", "続きの質問"]
    assert "回答: 最初の質問" in capsys.readouterr().out