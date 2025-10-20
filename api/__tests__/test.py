from types import SimpleNamespace
from .. import bot


def _run_tests():

    rag_json = bot.chat_rag([{
        'role': 'user',
        'content': "Where was Liam's last job?"
    }])
    print('RAG JSON')
    print(rag_json.output_text)


if __name__ == '__main__':
    _run_tests()