import json
import os
from typing import Any, Dict, Optional, List
from core.interfaces.base import ITranslator
from utils import get_user_documents_path


class Translator(ITranslator):
    """翻译器实现"""

    def __init__(self):
        self.translations: Dict[str, Dict] = {}
        self.current_language = "en"
        self.config_manager = None
        self.language_cache_dir = os.path.join(
            get_user_documents_path(), ".cursor-free-vip", "languages"
        )
        os.makedirs(self.language_cache_dir, exist_ok=True)
        self._load_translations()

    def set_config_manager(self, config_manager):
        self.config_manager = config_manager
        self._load_config()

    def _load_config(self):
        if self.config_manager:
            saved_language = self.config_manager.get("Language", "current_language")
            if saved_language and saved_language.strip():
                self.set_language(saved_language)
            else:
                self.current_language = self.detect_system_language()
                if self.config_manager:
                    self.config_manager.set(
                        "Language", "current_language", self.current_language
                    )
                    self.config_manager.save()

    def _load_translations(self):
        try:
            # Load translations from the locales directory
            locales_dir = os.path.join(os.path.dirname(__file__), "..", "..", "locales")
            if os.path.exists(locales_dir):
                for file_name in os.listdir(locales_dir):
                    if file_name.endswith(".json"):
                        lang_code = file_name[:-5]
                        try:
                            with open(
                                os.path.join(locales_dir, file_name),
                                "r",
                                encoding="utf-8",
                            ) as f:
                                self.translations[lang_code] = json.load(f)
                        except Exception:
                            continue
        except Exception:
            pass

    def detect_system_language(self) -> str:
        try:
            import locale
            import platform

            if platform.system() == "Windows":
                return self._detect_windows_language()
            else:
                return self._detect_unix_language()
        except Exception:
            return "en"

    def _detect_windows_language(self) -> str:
        try:
            import ctypes

            if not hasattr(ctypes, "windll"):
                return "en"

            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            threadid = user32.GetWindowThreadProcessId(hwnd, 0)
            layout_id = user32.GetKeyboardLayout(threadid) & 0xFFFF

            match layout_id:
                case 0x0804:
                    return "zh_cn"
                case _:
                    return "en"
        except:
            return self._detect_unix_language()

    def _detect_unix_language(self) -> str:
        try:
            import locale

            locale.setlocale(locale.LC_ALL, "")
            system_locale = locale.getlocale()[0]
            if not system_locale:
                return "en"

            system_locale = system_locale.lower()

            match system_locale:
                case s if s.startswith("zh_cn"):
                    return "zh_cn"
                case s if s.startswith("en"):
                    return "en"
                case _:
                    env_lang = os.getenv("LANG", "").lower()
                    match env_lang:
                        case s if "cn" in s:
                            return "zh_cn"
                        case s if "en" in s:
                            return "en"
                        case _:
                            return "en"
        except Exception:
            return "en"

            system_locale = system_locale.lower()

            match system_locale:
                case s if s.startswith("zh_cn"):
                    return "zh_cn"
                case s if s.startswith("en"):
                    return "en"
                case _:
                    env_lang = os.getenv("LANG", "").lower()
                    match env_lang:
                        case s if "cn" in s:
                            return "zh_cn"
                        case s if "en" in s:
                            return "en"
                        case _:
                            return "en"
        except:
            return "en"

    def get(self, key: str, **kwargs) -> str:
        try:
            keys = key.split(".")
            value = self.translations.get(self.current_language, {})

            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k, {})
                else:
                    break

            if isinstance(value, dict):
                if self.current_language != "en":
                    fallback_value = self.translations.get("en", {})
                    for k in keys:
                        if isinstance(fallback_value, dict):
                            fallback_value = fallback_value.get(k, {})
                        else:
                            break
                    if not isinstance(fallback_value, dict):
                        value = fallback_value
                else:
                    value = key

            if isinstance(value, str) and kwargs:
                try:
                    return value.format(**kwargs)
                except (KeyError, ValueError):
                    pass

            return str(value) if value else key
        except Exception:
            return key

    def set_language(self, language: str) -> None:
        if language in self.translations:
            self.current_language = language
            if self.config_manager:
                self.config_manager.set("Language", "current_language", language)
                self.config_manager.save()

    def get_available_languages(self) -> List[str]:
        """获取可用语言列表"""
        return list(self.translations.keys())
