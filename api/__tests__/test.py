from ..bot import chat_no_rag, chat_rag


rag = chat_rag("what is Liam Bellows's experience with Sharepoint?")
print('RAG')
print(rag.choices[0].message.content)

no_rag = chat_no_rag("what is Liam Bellows's experience with Sharepoint?")
print('No RAG')
print(no_rag.choices[0].message.content)

rag_json = chat_rag([{
    'role': 'user',
    'content': "Where was Liam's last job?"
}])
print('RAG JSON')
print(rag_json.choices[0].message.content)