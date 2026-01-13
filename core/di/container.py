from typing import Any, Dict, Optional
from core.services.config_manager import ConfigManager
from core.services.translator import Translator


# Dependency Injection container following the Singleton pattern
# Manages service lifecycle and provides loose coupling between components
class DependencyContainer:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._initialize_services()

    def _initialize_services(self):
        self._services["config_manager"] = ConfigManager()

        translator = Translator()
        translator.set_config_manager(self._services["config_manager"])
        self._services["translator"] = translator

    def get(self, service_name: str) -> Any:
        """获取服务实例"""
        return self._services.get(service_name)

    def register(self, service_name: str, service_instance: Any) -> None:
        """注册服务实例"""
        self._services[service_name] = service_instance

    def has(self, service_name: str) -> bool:
        """检查服务是否存在"""
        return service_name in self._services


container = DependencyContainer()
