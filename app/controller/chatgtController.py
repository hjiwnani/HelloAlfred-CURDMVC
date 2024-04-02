import requests
import json
from ..utils.common import jsonCommonStatus
import logging


def chat_gpt_asker(req):
    req_body = req
    url = "https://hai1.openai.azure.com/openai/deployments/HA_Test/chat/completions?api-version=2023-07-01-preview"
    payload = json.dumps({
    "max_tokens": 800,
    "messages": [
        {
        "role": "user",
        "content": req_body["message"]
        }
    ]
    })
    headers = {
        'Content-Type': 'application/json',
        'api-key': 'd1a9d04651ec4405a1ce74ffaa8a7b57'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        return jsonCommonStatus("API Call Successful!",json_data["choices"][0]["message"]["content"],200,True)
    except Exception as e:
        logging.error(e)
        return jsonCommonStatus("Internal server error", None, 500, False)