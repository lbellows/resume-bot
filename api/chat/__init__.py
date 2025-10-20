import azure.functions as func
import json
from ..bot import chat_rag
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        ip_address = req.headers.get('x-forwarded-for') or 'IP address not found'
        logging.info(ip_address)
    except Exception as e:
        logging.warning('Error getting IP')

    try:
                
        user_chat = ''
        if(req.method == 'GET'):
            user_chat = req.params.get('text')
        else:
            req_body = req.get_json()
            user_chat = req_body.get('text')
            chats = req_body.get('chats')

        prompt_input = chats if chats else user_chat
        logging.info(prompt_input)
        # do AI stuff
        llm_res = chat_rag(prompt_input)
        logging.info(llm_res.model_dump_json(indent=2))
        response_text = llm_res.output_text

        return func.HttpResponse(
            body=json.dumps({'data': response_text}),
            mimetype='application/json',
            status_code=200
        )

    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
                body=json.dumps({"data": str(e)}),
                mimetype='application/json',
                status_code=500
        )