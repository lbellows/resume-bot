
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
    Respond in Markdown. 
    Use the name "Liam" instead of Liam C. Bellows when responding.
    If asked about "He" or "You", assume they are asking about Liam.
    """ + (additional_prompt or '')

def chat_rag(input):
    
    prompt = [
        {
            "role": "system",
            "content": sys_prompt
        }
    ] 

    if isinstance(input, list):
        prompt.extend(input)
    else:
        prompt.append({
            "role": "user",
            "content": input
        })

    # Responses API: run an Azure Cognitive Search query locally and include
    # the top documents in the prompt (the Responses API does not accept
    # 'data_sources' in this SDK call).
    user_texts = [m.get('content') for m in prompt if m.get('role') == 'user']
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
    full_input = f"SYSTEM:\n{sys_prompt}\n\nCONTEXT:\n{docs_text}\n\nUSER:\n{input_text}"

    # Some Azure deployments don't accept temperature/top_p on Responses API
    completion = client.responses.create(
        model=deployment,
        input=full_input,
    )

    return completion

    # return _normalize_to_chat_like(completion)


def _normalize_to_chat_like(response_obj):
    """Convert a Responses API response (or a ChatCompletion response) into
    an object with `.choices[0].message.content` to keep compatibility with
    existing callers and tests.
    """
    # If it already looks like chat completions, return as-is
    if hasattr(response_obj, 'choices'):
        return response_obj

    text = None

    # try common attributes
    if hasattr(response_obj, 'output_text'):
        try:
            text = getattr(response_obj, 'output_text')
        except Exception:
            text = None

    if not text and hasattr(response_obj, 'output'):
        out = getattr(response_obj, 'output')
        try:
            # output may be a list of blocks
            if isinstance(out, list) and out:
                first = out[0]
                # first may be dict-like
                if isinstance(first, dict):
                    for c in first.get('content', []):
                        if isinstance(c, dict) and c.get('type') == 'output_text' and c.get('text'):
                            text = c.get('text')
                            break
                else:
                    # try attr access
                    for c in getattr(first, 'content', []) or []:
                        t = getattr(c, 'text', None) or (c.get('text') if isinstance(c, dict) else None)
                        if t:
                            text = t
                            break
        except Exception:
            text = None

    if not text and hasattr(response_obj, 'generations'):
        try:
            gens = getattr(response_obj, 'generations')
            if isinstance(gens, list) and gens:
                first = gens[0]
                # first may be a list or object
                cand = first[0] if isinstance(first, list) and first else first
                text = getattr(cand, 'text', None) or (cand.get('text') if isinstance(cand, dict) else None)
        except Exception:
            text = None

    if text is None:
        # final fallback: stringify the response
        try:
            text = str(response_obj)
        except Exception:
            text = ''

    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=text))])