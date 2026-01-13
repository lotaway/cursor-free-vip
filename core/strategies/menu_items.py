from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from core.interfaces.base import IMenuItem
from core.models.enums import MenuAction


# Strategy pattern implementation for menu items
# Each menu action is encapsulated in its own class following the Strategy pattern
class BaseMenuItem(IMenuItem):
    def __init__(self, action: MenuAction, translator: Any):
        self.action = action
        self.translator = translator

    @abstractmethod
    def execute(self) -> None:
        """执行菜单项的具体逻辑"""
        pass

    def get_id(self) -> int:
        """获取菜单项ID"""
        return self.action.value

    def get_name(self) -> str:
        """获取菜单项名称"""
        return self.translator.get(
            f"menu.{self.action.name.lower()}", fallback=self.action.name
        )

    def get_description(self) -> str:
        """获取菜单项描述"""
        return self.translator.get(
            f"menu.{self.action.name.lower()}_desc",
            fallback=f"Execute {self.action.name}",
        )


class ExitMenuItem(BaseMenuItem):
    """退出菜单项"""

    def execute(self) -> None:
        from colorama import Fore, Style

        print(
            f"\n{Fore.YELLOW}ℹ️  {self.translator.get('menu.exit')}...{Style.RESET_ALL}"
        )
        print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
        exit(0)


class ResetMachineIdMenuItem(BaseMenuItem):
    """重置机器ID菜单项"""

    def execute(self) -> None:
        import reset_machine_manual

        reset_machine_manual.run(self.translator)


class RegisterManualMenuItem(BaseMenuItem):
    """手动注册菜单项"""

    def execute(self) -> None:
        import cursor_register_manual

        cursor_register_manual.main(self.translator)


class QuitCursorMenuItem(BaseMenuItem):
    """退出Cursor菜单项"""

    def execute(self) -> None:
        import quit_cursor

        quit_cursor.quit_cursor(self.translator)


class LanguageMenuItem(BaseMenuItem):
    """语言选择菜单项"""

    def execute(self) -> None:
        pass


class OAuthGoogleMenuItem(BaseMenuItem):
    """Google OAuth菜单项"""

    def execute(self) -> None:
        from oauth_auth import main as oauth_main

        oauth_main("google", self.translator)


class OAuthGitHubMenuItem(BaseMenuItem):
    """GitHub OAuth菜单项"""

    def execute(self) -> None:
        from oauth_auth import main as oauth_main

        oauth_main("github", self.translator)


class DisableAutoUpdateMenuItem(BaseMenuItem):
    """禁用自动更新菜单项"""

    def execute(self) -> None:
        import disable_auto_update

        disable_auto_update.run(self.translator)


class TotallyResetMenuItem(BaseMenuItem):
    """完全重置菜单项"""

    def execute(self) -> None:
        import totally_reset_cursor

        totally_reset_cursor.run(self.translator)


class ShowContributorsMenuItem(BaseMenuItem):
    """显示贡献者菜单项"""

    def execute(self) -> None:
        import logo

        print(logo.CURSOR_CONTRIBUTORS)


class ShowConfigMenuItem(BaseMenuItem):
    """显示配置菜单项"""

    def execute(self) -> None:
        from config import print_config, get_config

        print_config(get_config(), self.translator)


class BypassVersionMenuItem(BaseMenuItem):
    """绕过版本检查菜单项"""

    def execute(self) -> None:
        import bypass_version

        bypass_version.main(self.translator)


class CheckAuthorizedMenuItem(BaseMenuItem):
    """检查授权菜单项"""

    def execute(self) -> None:
        import check_user_authorized

        check_user_authorized.main(self.translator)


class BypassTokenLimitMenuItem(BaseMenuItem):
    """绕过Token限制菜单项"""

    def execute(self) -> None:
        import bypass_token_limit

        bypass_token_limit.run(self.translator)


class RestoreMachineIdMenuItem(BaseMenuItem):
    """恢复机器ID菜单项"""

    def execute(self) -> None:
        import restore_machine_id

        restore_machine_id.run(self.translator)


class DeleteGoogleAccountMenuItem(BaseMenuItem):
    """删除Google账户菜单项"""

    def execute(self) -> None:
        import delete_cursor_google

        delete_cursor_google.main(self.translator)


class OAuthProfileMenuItem(BaseMenuItem):
    """OAuth配置文件菜单项"""

    def execute(self) -> None:
        from oauth_auth import OAuthHandler

        oauth = OAuthHandler(self.translator)
        oauth._select_profile()


class ManualCustomAuthMenuItem(BaseMenuItem):
    """手动自定义认证菜单项"""

    def execute(self) -> None:
        import manual_custom_auth

        manual_custom_auth.main(self.translator)
