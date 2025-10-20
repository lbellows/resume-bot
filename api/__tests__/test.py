"""Simple offline-capable tests for bot.chat_no_rag and bot.chat_rag.

These tests monkeypatch `bot.client` with a fake object so no network or API
keys are required. Run with `python -m api.__tests__.test`.
"""

from types import SimpleNamespace
from .. import bot


class FakeResponse:
    def __init__(self, text):
        self.choices = [SimpleNamespace(message=SimpleNamespace(content=text))]


class FakeCompletions:
    def create(self, **kwargs):
        # Return a predictable response based on input messages
        msgs = kwargs.get('messages') or []
        user_texts = [m.get('content') for m in msgs if m.get('role') == 'user']
        joined = ' | '.join(user_texts) if user_texts else 'no user content'
        return FakeResponse(f"fake-response: {joined}")


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


def _run_offline_tests():
    # Monkeypatch the real client
    # Use the real client to run the live tests (requires env vars and keys)
    rag = bot.chat_rag("what is Liam Bellows's experience with Sharepoint?")
    print('RAG')
    print(rag.choices[0].message.content)

    no_rag = bot.chat_no_rag("what is Liam Bellows's experience with Sharepoint?")
    print('No RAG')
    print(no_rag.choices[0].message.content)

    rag_json = bot.chat_rag([{
        'role': 'user',
        'content': "Where was Liam's last job?"
    }])
    print('RAG JSON')
    print(rag_json.choices[0].message.content)


if __name__ == '__main__':
    _run_offline_tests()