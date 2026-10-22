from app.llm import client
from app.llm.client import LLMClient


class _Response:
    def raise_for_status(self):
        pass

    def json(self):
        return {"message": {"content": "hi there"}}


def test_chat_posts_to_ollama_and_returns_content(monkeypatch):
    captured = {}

    def fake_post(url, json):
        captured["url"] = url
        captured["json"] = json
        return _Response()

    monkeypatch.setattr(client.requests, "post", fake_post)
    answer = LLMClient().chat([{"role": "user", "content": "hello"}])

    assert answer == "hi there"
    assert captured["url"].endswith("/api/chat")
    assert captured["json"]["stream"] is False
    assert captured["json"]["messages"][0]["content"] == "hello"


def test_config_has_defaults(monkeypatch):
    from app import config
    assert config.OLLAMA_HOST
    assert config.OLLAMA_MODEL
