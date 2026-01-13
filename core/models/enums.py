from enum import Enum


# Enums for type safety and to avoid magic strings throughout the codebase
class MenuAction(Enum):
    """菜单动作枚举"""

    EXIT = 0
    RESET_MACHINE_ID = 1
    REGISTER_GOOGLE = 2
    REGISTER_GITHUB = 3
    REGISTER_MANUAL = 4
    QUIT_CURSOR = 5
    TOTALLY_RESET = 6
    BYPASS_TOKEN_LIMIT = 7
    RESTORE_MACHINE_ID = 8
    DELETE_GOOGLE_ACCOUNT = 9
    BYPASS_VERSION = 10
    DISABLE_AUTO_UPDATE = 11
    CHECK_USER_AUTHORIZED = 12
    OAUTH_AUTH = 13
    MANUAL_CUSTOM_AUTH = 14
    CURSOR_AUTH = 15
    GET_USER_TOKEN = 16
    CURSOR_REGISTER_MANUAL = 17
    CURSOR_ACC_INFO = 18
    ACCOUNT_MANAGER = 19
    NEW_SIGNUP = 20
    BUILD = 21
    FILL_MISSING_TRANSLATIONS = 22
    QUIT_CURSOR_APP = 23


class Language(Enum):
    """语言枚举"""

    EN = "en"
    ZH_CN = "zh_cn"


class OperationStatus(Enum):
    """操作状态枚举"""

    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ConfigSection(Enum):
    """配置段枚举"""

    LANGUAGE = "Language"
    CHROME = "Chrome"
    TURNSITLE = "Turnstile"
    OS_PATHS = "OSPaths"
    TIMING = "Timing"
    UTILS = "Utils"
    TEMP_MAIL_PLUS = "TempMailPlus"
    WINDOWS_PATHS = "WindowsPaths"
    BROWSER = "Browser"
    OAUTH = "OAuth"
