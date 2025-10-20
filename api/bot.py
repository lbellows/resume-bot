
import os  
from openai import AzureOpenAI
from types import SimpleNamespace
from dotenv import load_dotenv
import json
import urllib.parse
import urllib.request
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
search_endpoint = os.getenv("SEARCH_ENDPOINT")  
search_key = os.getenv("SEARCH_KEY")  
search_index = os.getenv("SEARCH_INDEX_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
additional_prompt = os.getenv("ADDITIONAL_PROMPT")
api = os.getenv("API_VERSION")

client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version=api,
)

sys_prompt = """You are an AI assistant that helps people find information.
    You have Liam's resume and professional history as context.
    Respond in Markdown. 
    If asked about "He" or "You", assume they are asking about Liam.
    Don't make suggestions about what to ask next.
    If you don't know the answer, just say you don't know. Do not make up answers.
    """ + (additional_prompt or '')

def chat_rag(input):
    """Accepts either:
    - a list of message dicts (old behavior), or
    - a single JS-like user message object with fields like
      { id, time, name, text, isUser, role, content }

    Uses the Azure Responses API 'instructions' parameter for the
    system prompt and, when the incoming message contains an 'id', passes
    it as 'previous_response_id' to provide chat history context.
    """

    # Normalize messages into a list of message dicts
    messages = []
    previous_response_id = None

    if isinstance(input, list):
        messages = input[:]  # assume already in {role, content} form
    elif isinstance(input, dict):
        # JS-like object: prefer 'content' then 'text'
        content = input.get('content') or input.get('text') or ''
        role = input.get('role', 'user')
        messages = [{"role": role, "content": content}]
        # capture id if present to forward as previous_response_id
        previous_response_id = input.get('id')
    else:
        # fallback: treat as raw string
        messages = [{"role": "user", "content": str(input)}]

    # Responses API: run an Azure Cognitive Search query locally and include
    # the top documents in the prompt (the Responses API does not accept
    # 'data_sources' in this SDK call).
    user_texts = [m.get('content') for m in messages if m.get('role') == 'user']
    input_text = "\n\n".join(user_texts) if user_texts else ""

    # Build a simple Azure Cognitive Search query to fetch top documents
    try:
        query = urllib.parse.quote(input_text)
        url = f"{search_endpoint}/indexes/{search_index}/docs/search?api-version=2020-06-30"
        body = json.dumps({"search": input_text, "top": 5}).encode('utf-8')
        req = urllib.request.Request(url, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('api-key', search_key)
        with urllib.request.urlopen(req, timeout=10) as resp:
            search_resp = json.load(resp)
        docs = []
        for d in search_resp.get('value', [])[:5]:
            # try to get a content field or the whole document
            content = d.get('content') or d.get('text') or json.dumps(d)
            docs.append(content)
        docs_text = "\n\n---\n\n".join(docs)
    except Exception:
        docs_text = ""

    # Compose the final input by including system prompt, retrieved docs,
    # then the user's input
    # Compose the final input by including retrieved docs then the user's input
    full_input = f"CONTEXT:\n{docs_text}\n\nUSER:\n{input_text}"

    # Build request kwargs for Responses API. Use 'instructions' for system prompt
    # and include previous_response_id when available.
    request_kwargs = {
        "model": deployment,
        "input": full_input,
        "instructions": sys_prompt,
    }

    if previous_response_id:
        request_kwargs["previous_response_id"] = previous_response_id

    print("Request kwargs:", request_kwargs.get('previous_response_id'))
    # Some Azure deployments don't accept temperature/top_p on Responses API
    completion = client.responses.create(**request_kwargs)

    return completion
