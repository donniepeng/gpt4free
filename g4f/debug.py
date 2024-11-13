from .providers.types import ProviderType

logging: bool = False
version_check: bool = True
last_provider: ProviderType = None
last_model: str = None
version: str = None
is_use_api: bool = False