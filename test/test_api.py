import json

import requests


def api_chat_completions(role: str, prompt: str) -> str:
    url = "http://localhost:1337/v1/chat/completions"
    body = {
        "provider": "Blackbox AI",
        "model": "gpt-3.5-turbo",
        "stream": False,
        "messages": [
            {"role": role, "content": prompt}
        ]
    }

    json_response = requests.post(url, json=body).json().get('choices', [])
    choice = json_response[0]
    return choice.get('message', {}).get('content', '')


def api_generate_image(prompt: str, is_url: bool = True) -> str:
    url = "http://localhost:1337/v1/images/generate"
    body = {
        "model": "flux",
        "response_format": "url" if is_url else "b64_json",
        "prompt": prompt
    }
    response = requests.post(url, json=body).json()
    return response['data'][0]['url'] if is_url else response['data'][0]['b64_json']


def api_list_models() -> dict:
    url = "http://localhost:1337/v1/models"
    return requests.get(url).json()


if __name__ == "__main__":
    # models = api_list_models()
    # print(json.dumps(models, ensure_ascii=False, indent=4))

    img = api_generate_image(prompt='a beautiful castle', is_url=True)
    print(json.dumps(img, ensure_ascii=False, indent=4))

    # reply = api_chat_completions()
    # print(reply)
