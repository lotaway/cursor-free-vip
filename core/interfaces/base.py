from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IService(ABC):
    """服务接口基类"""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """执行服务方法"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取服务名称"""
        pass


class IMenuItem(ABC):
    """菜单项接口"""

    @abstractmethod
    def get_id(self) -> int:
        """获取菜单项ID"""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """获取菜单项名称"""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """获取菜单项描述"""
        pass

    @abstractmethod
    def execute(self) -> None:
        """执行菜单项"""
        pass


class ITranslator(ABC):
    """翻译器接口"""

    @abstractmethod
    def get(self, key: str, **kwargs) -> str:
        """获取翻译文本"""
        pass

    @abstractmethod
    def set_language(self, language: str) -> None:
        """设置当前语言"""
        pass

    @abstractmethod
    def get_available_languages(self) -> list:
        """获取可用语言列表"""
        pass


class IConfigManager(ABC):
    """配置管理器接口"""

    @abstractmethod
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """获取配置值"""
        pass

    @abstractmethod
    def set(self, section: str, key: str, value: Any) -> None:
        """设置配置值"""
        pass

    @abstractmethod
    def save(self) -> None:
        """保存配置"""
        pass


class ILogger(ABC):
    """日志器接口"""

    @abstractmethod
    def info(self, message: str) -> None:
        """记录信息日志"""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """记录错误日志"""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """记录警告日志"""
        pass
