from types import SimpleNamespace
from .. import bot

def _run_tests():
    print('RAG JSON:')
    rag_json = bot.chat_rag({
        'role': 'user',
        'content': "Where was Liam's last job?"
    })

    print({
        'data': rag_json.output_text,
        'id': rag_json.id,
    })

    rag_json = bot.chat_rag({
        'role': 'user',
        'content': "Say one thing about Liam",
        'id': rag_json.id
    })

    print({
        'data': rag_json.output_text,
        'id': rag_json.id,
    })

    rag_json = bot.chat_rag({
        'role': 'user',
        'content': "How many questions have I asked so far?",
        'id': rag_json.id
    })

    print({
        'data': rag_json.output_text,
        'id': rag_json.id,
    })



if __name__ == '__main__':
    _run_tests()