import unittest
from unittest.mock import Mock, patch
from core.services.config_manager import ConfigManager
from core.services.translator import Translator


class TestConfigManager(unittest.TestCase):
    """配置管理器测试"""

    def setUp(self):
        self.config_manager = ConfigManager()

    def test_get_set_value(self):
        """测试获取和设置配置值"""
        self.config_manager.set("Test", "key", "value")
        self.assertEqual(self.config_manager.get("Test", "key"), "value")

    def test_get_boolean(self):
        """测试获取布尔值"""
        self.config_manager.set("Test", "bool_key", "True")
        self.assertTrue(self.config_manager.get_boolean("Test", "bool_key"))

        self.config_manager.set("Test", "bool_key", "False")
        self.assertFalse(self.config_manager.get_boolean("Test", "bool_key"))


class TestTranslator(unittest.TestCase):
    """翻译器测试"""

    def setUp(self):
        self.translator = Translator()

    def test_get_translation(self):
        result = self.translator.get("menu.title")
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_set_language(self):
        """测试设置语言"""
        self.translator.set_language("zh_cn")
        self.assertEqual(self.translator.current_language, "zh_cn")

    def test_get_available_languages(self):
        """测试获取可用语言"""
        languages = self.translator.get_available_languages()
        self.assertIsInstance(languages, list)
        self.assertIn("en", languages)
        self.assertIn("zh_cn", languages)


if __name__ == "__main__":
    unittest.main()
