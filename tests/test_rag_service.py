from app.rag import rag_service
from app.rag.rag_service import RAGService


class FakeVectorDB:
    def search(self, query_embedding):
        return {
            "documents": [["Fall protection is required above 6 feet."]],
            "metadatas": [[{"source": "01_construction_safety_regulations.pdf"}]],
        }


class FakeLLM:
    def __init__(self):
        self.messages = None

    def chat(self, messages):
        self.messages = messages
        return "stub answer"


def make_service(monkeypatch):
    monkeypatch.setattr(rag_service, "ChromaStore", FakeVectorDB)
    monkeypatch.setattr(rag_service, "LLMClient", FakeLLM)
    return RAGService()


def test_ask_returns_the_llm_answer(monkeypatch):
    assert make_service(monkeypatch).ask("When is fall protection required?") == "stub answer"


def test_prompt_contains_retrieved_context_and_source(monkeypatch):
    service = make_service(monkeypatch)
    service.ask("When is fall protection required?")
    user_prompt = service.llm.messages[1]["content"]
    assert "Fall protection is required above 6 feet." in user_prompt
    assert "01_construction_safety_regulations.pdf" in user_prompt
    assert "When is fall protection required?" in user_prompt


def test_system_prompt_restricts_answers_to_the_context(monkeypatch):
    service = make_service(monkeypatch)
    service.ask("anything")
    system_prompt = service.llm.messages[0]["content"]
    assert "ONLY using the provided context" in system_prompt
    assert "couldn't find that information" in system_prompt
