from __future__ import annotations

import os.path

import g4f
from ..providers.types import BaseProvider, ProviderType
from ..providers.retry_provider import RetryProvider, IterListProvider
from ..providers.base_provider import AsyncProvider, AsyncGeneratorProvider
from ..providers.create_images import CreateImagesProvider

from .deprecated import *
from .selenium import *
from .needs_auth import *

from .gigachat import *
from .nexra import *

from .Ai4Chat import Ai4Chat
from .AI365VIP import AI365VIP
from .AIChatFree import AIChatFree
from .AIUncensored import AIUncensored
from .Allyfy import Allyfy
from .AmigoChat import AmigoChat
from .AiChatOnline import AiChatOnline
from .AiChats import AiChats
from .AiMathGPT import AiMathGPT
from .Airforce import Airforce
from .Aura import Aura
from .Bing import Bing
from .BingCreateImages import BingCreateImages
from .Blackbox import Blackbox
from .ChatGot import ChatGot
from .ChatGpt import ChatGpt
from .Chatgpt4Online import Chatgpt4Online
from .Chatgpt4o import Chatgpt4o
from .ChatGptEs import ChatGptEs
from .ChatgptFree import ChatgptFree
from .ChatHub import ChatHub
from .ChatifyAI import ChatifyAI
from .Cloudflare import Cloudflare
from .DarkAI import DarkAI
from .DDG import DDG
from .DeepInfra import DeepInfra
from .DeepInfraChat import DeepInfraChat
from .DeepInfraImage import DeepInfraImage
from .Editee import Editee
from .FlowGpt import FlowGpt
from .Free2GPT import Free2GPT
from .FreeChatgpt import FreeChatgpt
from .FreeGpt import FreeGpt
from .FreeNetfly import FreeNetfly
from .GeminiPro import GeminiPro
from .GizAI import GizAI
from .GPROChat import GPROChat
from .HuggingChat import HuggingChat
from .HuggingFace import HuggingFace
from .Koala import Koala
from .Liaobots import Liaobots
from .Local import Local
from .MagickPen import MagickPen
from .MetaAI import MetaAI
# from .MetaAIAccount   import MetaAIAccount
from .Ollama import Ollama
from .PerplexityLabs import PerplexityLabs
from .Pi import Pi
from .Pizzagpt import Pizzagpt
from .Prodia import Prodia
from .Reka import Reka
from .Replicate import Replicate
from .ReplicateHome import ReplicateHome
from .RubiksAI import RubiksAI
from .TeachAnything import TeachAnything
from .Upstage import Upstage
from .WhiteRabbitNeo import WhiteRabbitNeo
from .You import You
from .TogBlackbox import TogBlackbox

import sys

_current_dir = os.path.abspath(os.path.dirname(__file__))
g4f.debug.is_use_api = os.path.isfile(os.path.join(_current_dir, "is_use_api"))
print(f'g4f.debug.is_use_api = {g4f.debug.is_use_api}')

__modules__: list = [
    getattr(sys.modules[__name__], provider) for provider in dir()
    if not provider.startswith("__")
]

__providers__: list[ProviderType] = [
    provider for provider in __modules__
    if isinstance(provider, type)
       and issubclass(provider, BaseProvider) and (
               not g4f.debug.is_use_api or g4f.debug.is_use_api and provider.__name__.startswith("Tog"))
]

# print("Available providers:")
# for provider in __providers__:
#     print(provider.__name__)

__all__: list[str] = [
    provider.__name__ for provider in __providers__
]

__map__: dict[str, ProviderType] = dict([
    (provider.__name__, provider) for provider in __providers__
])


class ProviderUtils:
    convert: dict[str, ProviderType] = __map__
