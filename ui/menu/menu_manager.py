from typing import Dict, List
from core.interfaces.base import IMenuItem
from core.models.enums import MenuAction
from core.strategies.menu_items import (
    ExitMenuItem,
    ResetMachineIdMenuItem,
    RegisterManualMenuItem,
    QuitCursorMenuItem,
    LanguageMenuItem,
    OAuthGoogleMenuItem,
    OAuthGitHubMenuItem,
    DisableAutoUpdateMenuItem,
    TotallyResetMenuItem,
    ShowContributorsMenuItem,
    ShowConfigMenuItem,
    BypassVersionMenuItem,
    CheckAuthorizedMenuItem,
    BypassTokenLimitMenuItem,
    RestoreMachineIdMenuItem,
    DeleteGoogleAccountMenuItem,
    OAuthProfileMenuItem,
    ManualCustomAuthMenuItem,
)


class MenuManager:
    """菜单管理器"""

    def __init__(self, translator):
        self.translator = translator
        self.menu_items: Dict[str, IMenuItem] = {}
        self._initialize_menu_items()

    def _initialize_menu_items(self):
        """初始化菜单项"""
        menu_item_classes = {
            "0": (MenuAction.EXIT, ExitMenuItem),
            "1": (MenuAction.RESET_MACHINE_ID, ResetMachineIdMenuItem),
            "2": (MenuAction.REGISTER_MANUAL, RegisterManualMenuItem),
            "3": (MenuAction.QUIT_CURSOR, QuitCursorMenuItem),
            "4": (MenuAction.REGISTER_GOOGLE, OAuthGoogleMenuItem),
            "5": (MenuAction.REGISTER_GITHUB, OAuthGitHubMenuItem),
            "6": (MenuAction.DISABLE_AUTO_UPDATE, DisableAutoUpdateMenuItem),
            "7": (MenuAction.TOTALLY_RESET, TotallyResetMenuItem),
            "8": (MenuAction.BYPASS_TOKEN_LIMIT, BypassTokenLimitMenuItem),
            "9": (MenuAction.RESTORE_MACHINE_ID, RestoreMachineIdMenuItem),
            "10": (MenuAction.DELETE_GOOGLE_ACCOUNT, DeleteGoogleAccountMenuItem),
            "11": (MenuAction.OAUTH_AUTH, OAuthProfileMenuItem),
            "12": (MenuAction.MANUAL_CUSTOM_AUTH, ManualCustomAuthMenuItem),
            "13": (MenuAction.BYPASS_VERSION, BypassVersionMenuItem),
            "14": (MenuAction.CHECK_USER_AUTHORIZED, CheckAuthorizedMenuItem),
            "15": (MenuAction.CURSOR_AUTH, ShowConfigMenuItem),
            "16": (MenuAction.GET_USER_TOKEN, ShowContributorsMenuItem),
        }

        for choice, (action, item_class) in menu_item_classes.items():
            self.menu_items[choice] = item_class(action, self.translator)

    def get_menu_item(self, choice: str) -> IMenuItem:
        """获取菜单项"""
        return self.menu_items.get(choice)

    def get_available_choices(self) -> List[str]:
        """获取可用选择"""
        return list(self.menu_items.keys())

    def execute_choice(self, choice: str) -> bool:
        """执行选择"""
        menu_item = self.get_menu_item(choice)
        if menu_item:
            menu_item.execute()
            return True
        return False
