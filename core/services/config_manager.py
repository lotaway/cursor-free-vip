import configparser
import os
from typing import Any, Optional
from core.interfaces.base import IConfigManager
from core.models.enums import ConfigSection
from utils import get_user_documents_path


class ConfigManager(IConfigManager):
    """配置管理器实现"""

    def __init__(self, config_path: Optional[str] = None):
        self.config = configparser.ConfigParser()
        self.config_path = config_path or self._get_default_config_path()
        self._load_config()

    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        return os.path.join(get_user_documents_path(), ".cursor-free-vip", "config.ini")

    def _load_config(self) -> None:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            self.config.read(self.config_path, encoding="utf-8")

    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """获取配置值"""
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def set(self, section: str, key: str, value: Any) -> None:
        """设置配置值"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def save(self) -> None:
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            self.config.write(f)

    def get_boolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """获取布尔值配置"""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback


config_manager = ConfigManager()
