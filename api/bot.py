
import os  
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv("ENDPOINT_URL")  
deployment = os.getenv("DEPLOYMENT_NAME")  
search_endpoint = os.getenv("SEARCH_ENDPOINT")  
search_key = os.getenv("SEARCH_KEY")  
search_index = os.getenv("SEARCH_INDEX_NAME")  
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

client = AzureOpenAI(  
    azure_endpoint=endpoint,  
    api_key=subscription_key,  
    api_version="2024-08-01-preview",
)

sys_prompt = """You are an AI assistant that helps people find information. 
    Respond in Markdown. 
    Use the name Liam instead of Liam C. Bellows.
    """

def chat_no_rag(input):


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

    # Generate the completion  
    completion = client.chat.completions.create(  
        model=deployment,
        messages=prompt,
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,
        stop=None,  
        stream=False
    )

    return completion #.to_json()

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

    completion = client.chat.completions.create(  
    model=deployment,
    messages=prompt,
    max_tokens=800,  
    temperature=0.7,  
    top_p=0.95,  
    frequency_penalty=0,  
    presence_penalty=0,
    stop=None,  
    stream=False,
    extra_body={
      "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": search_index,
            "semantic_configuration": "default",
            "query_type": "simple",
            "fields_mapping": {},
            "in_scope": False,
            "role_information": sys_prompt,
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            }
          }
        }]
    }
    )

    return completion