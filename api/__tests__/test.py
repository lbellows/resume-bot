from types import SimpleNamespace
from .. import bot

def _run_tests():

    rag_json = bot.chat_rag([{
        'role': 'user',
        'content': "Where was Liam's last job?"
    }])
    print('RAG JSON')
    print({
        'data': rag_json.output_text,
        'id': rag_json.id,
    })


if __name__ == '__main__':
    _run_tests()