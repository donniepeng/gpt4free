import json
import requests

from g4f.requests import forward_tool

LOCAL_HOST = 'localhost'
REMOTE_HOST = '119.28.43.197'
PORT = 6337

g_is_local_host = False
HOST = LOCAL_HOST if g_is_local_host else REMOTE_HOST

# 是否使用转发
g_is_use_forwarder = True


def _do_get(url: str) -> dict:
    if g_is_use_forwarder:
        status, content = forward_tool.request_get_and_decrypt_response(headers=None, url=url)
        return json.loads(content)
    else:
        return requests.get(url=url).json()


def _do_post(url: str, json_obj: dict) -> dict:
    if g_is_use_forwarder:
        status, content = forward_tool.request_post_and_decrypt_response(headers=None, url=url, json_obj=json_obj)
        return json.loads(content)
    else:
        return requests.post(url=url, json=json_obj).json()


class TextPrompt:
    role: str
    content: str

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


async def api_chat_completions(prompts: [TextPrompt], provider: str = None, model: str = None,
                               stream: bool = False) -> str:
    url = f"http://{HOST}:{PORT}/v1/chat/completions"
    body = {
        "provider": provider if provider is not None else "Blackbox AI",
        "model": model if model is not None else "gpt-3.5-turbo",
        "stream": False,
        "messages": [
            {
                "role": prompt.role,
                "content": prompt.content
            }
            for prompt in prompts
        ]
    }

    resp_data = _do_post(url=url, json_obj=body).get('choices', [])
    choice = resp_data[0]
    return choice.get('message', {}).get('content', '')


async def api_generate_image(prompt: str, is_url: bool = True, model: str = None) -> str:
    url = f"http://{HOST}:{PORT}/v1/images/generate"
    body = {
        "model": model if model is not None else "flux",
        "response_format": "url" if is_url else "b64_json",
        "prompt": prompt
    }
    resp_data = _do_post(url=url, json_obj=body).get('data', [])
    return resp_data[0]['url'] if is_url else resp_data[0]['b64_json']


async def api_list_models() -> dict:
    url = f"http://{HOST}:{PORT}/v1/models"
    return _do_get(url=url)


if __name__ == "__main__":
    # models = api_list_models()
    # print(json.dumps(models, ensure_ascii=False, indent=4))

    img = api_generate_image(prompt='a beautiful castle', is_url=True)
    print(json.dumps(img, ensure_ascii=False, indent=4))

    # reply = api_chat_completions()
    # print(reply)
