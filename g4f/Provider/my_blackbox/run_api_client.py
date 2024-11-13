import json

import requests

LOCAL_HOST = 'localhost'
REMOTE_HOST = '119.28.43.197'
PORT = 6337

g_is_local_host = False
HOST = LOCAL_HOST if g_is_local_host else REMOTE_HOST


def api_chat_completions(role: str, prompt: str, provider: str = None, model: str = None) -> str:
    url = f"http://{HOST}:{PORT}/v1/chat/completions"
    body = {
        "provider": provider if provider is not None else "Blackbox AI",
        "model": model if model is not None else "gpt-3.5-turbo",
        "stream": False,
        "messages": [
            {"role": role, "content": prompt}
        ]
    }

    json_response = requests.post(url, json=body).json().get('choices', [])
    choice = json_response[0]
    return choice.get('message', {}).get('content', '')


def api_generate_image(prompt: str, is_url: bool = True, model: str = None) -> str:
    url = f"http://{HOST}:{PORT}/v1/images/generate"
    body = {
        "model": model if model is not None else "flux",
        "response_format": "url" if is_url else "b64_json",
        "prompt": prompt
    }
    response = requests.post(url, json=body).json()
    return response['data'][0]['url'] if is_url else response['data'][0]['b64_json']


def api_list_models() -> dict:
    url = f"http://{HOST}:{PORT}/v1/models"
    return requests.get(url).json()


if __name__ == "__main__":
    # models = api_list_models()
    # print(json.dumps(models, ensure_ascii=False, indent=4))

    img = api_generate_image(prompt='a beautiful castle', is_url=True)
    print(json.dumps(img, ensure_ascii=False, indent=4))

    # reply = api_chat_completions()
    # print(reply)
