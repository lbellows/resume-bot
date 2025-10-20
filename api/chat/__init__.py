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
                
        req_body = req.get_json()
        logging.info(req_body)
        llm_res = chat_rag(req_body.get('newUserChat'))
        logging.info(llm_res.model_dump_json(indent=2))

        return func.HttpResponse(
            body=json.dumps({
                'data': llm_res.output_text,
                'id': llm_res.id,
            }),
            mimetype='application/json',
            status_code=200
        )

    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
                body=json.dumps({"data": str(e), 'id': ''}),
                mimetype='application/json',
                status_code=500
        )