#!/usr/bin/env python3
"""
Cursor Free VIP - Main Application
遵循代码规范进行重构，使用依赖注入和策略模式
"""

import os
import sys
import platform
from colorama import Fore, Style, init

from core.di.container import container
from ui.menu.menu_manager import MenuManager
from logo import print_logo


def is_frozen() -> bool:
    """检查是否为冻结的可执行文件"""
    return getattr(sys, "frozen", False)


def is_admin() -> bool:
    """检查是否具有管理员权限（仅Windows）"""
    if platform.system() != "Windows":
        return True

    try:
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def run_as_admin() -> bool:
    """以管理员权限重新运行（仅Windows）"""
    try:
        import ctypes

        args = [sys.executable] + sys.argv

        EMOJI = {"ADMIN": "🔐"}
        print(f"{Fore.YELLOW}{EMOJI['ADMIN']} 请求管理员权限...{Style.RESET_ALL}")

        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", args[0], " ".join(f'"{arg}"' for arg in args[1:]), None, 1
        )
        return True
    except Exception as e:
        EMOJI = {"ERROR": "❌"}
        print(f"{Fore.RED}{EMOJI['ERROR']} 请求管理员权限失败: {e}{Style.RESET_ALL}")
        return False


def check_latest_version():
    """检查最新版本（简化版本）"""
    translator = container.get("translator")
    print(f"{Fore.CYAN}ℹ️ {translator.get('updater.checking_version')}{Style.RESET_ALL}")

    try:
        import requests
        from logo import version

        response = requests.get(
            "https://api.github.com/repos/lotaway/cursor-free-vip/releases/latest",
            timeout=10,
        )

        if response.status_code == 404:
            print(
                f"{Fore.YELLOW}⚠️ {translator.get('updater.no_releases', fallback='No releases found in repository')}{Style.RESET_ALL}"
            )
            return

        response.raise_for_status()

        latest_release = response.json()
        if "tag_name" not in latest_release:
            print(
                f"{Fore.YELLOW}⚠️ {translator.get('updater.invalid_release', fallback='Invalid release data')}{Style.RESET_ALL}"
            )
            return

        latest_version = latest_release["tag_name"].lstrip("v")
        current_version = version.lstrip("v")

        print(
            f"{Fore.GREEN}✅ {translator.get('updater.version_info', current=current_version, latest=latest_version)}{Style.RESET_ALL}"
        )

    except requests.exceptions.RequestException as e:
        print(
            f"{Fore.RED}❌ {translator.get('updater.network_error', error=str(e))}{Style.RESET_ALL}"
        )
    except Exception as e:
        print(
            f"{Fore.RED}❌ {translator.get('updater.check_failed', error=str(e))}{Style.RESET_ALL}"
        )


def print_menu(menu_manager):
    """打印菜单"""
    translator = container.get("translator")

    print(f"\n{Fore.CYAN}{translator.get('menu.title')}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 50}{Style.RESET_ALL}")

    for choice in menu_manager.get_available_choices():
        menu_item = menu_manager.get_menu_item(choice)
        if menu_item:
            print(f"{Fore.GREEN}{choice}{Style.RESET_ALL}. {menu_item.get_name()}")


def handle_language_selection():
    """处理语言选择"""
    translator = container.get("translator")
    config_manager = container.get("config_manager")

    print(f"\n{Fore.CYAN}🌐 {translator.get('menu.select_language')}:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'─' * 40}{Style.RESET_ALL}")

    languages = translator.get_available_languages()
    for i, lang in enumerate(languages):
        lang_name = translator.get(f"languages.{lang}", fallback=lang)
        print(f"{Fore.GREEN}{i}{Style.RESET_ALL}. {lang_name}")

    try:
        choice = input(
            f"\n➜ {Fore.CYAN}{translator.get('menu.input_choice', choices=f'0-{len(languages) - 1}')}: {Style.RESET_ALL}"
        )
        choice = choice.strip()

        if choice.isdigit() and 0 <= int(choice) < len(languages):
            selected_language = languages[int(choice)]
            translator.set_language(selected_language)
            print(
                f"{Fore.GREEN}✅ {translator.get('menu.language_config_saved')}{Style.RESET_ALL}"
            )
            return True
        else:
            print(
                f"{Fore.RED}❌ {translator.get('menu.invalid_choice')}{Style.RESET_ALL}"
            )
            return False

    except KeyboardInterrupt:
        return False
    except Exception as e:
        print(
            f"{Fore.RED}❌ {translator.get('menu.error_occurred', error=str(e))}{Style.RESET_ALL}"
        )
        return False


def main():
    init()

    if platform.system() == "Windows" and is_frozen() and not is_admin():
        translator = container.get("translator")
        print(
            f"{Fore.YELLOW}🔐 {translator.get('menu.admin_required')}{Style.RESET_ALL}"
        )
        if run_as_admin():
            sys.exit(0)
        else:
            print(
                f"{Fore.YELLOW}ℹ️ {translator.get('menu.admin_required_continue')}{Style.RESET_ALL}"
            )

    print_logo()

    translator = container.get("translator")
    config_manager = container.get("config_manager")

    try:
        from config import get_config, force_update_config

        config = get_config(translator)
        if not config:
            print(
                f"{Fore.RED}❌ {translator.get('menu.config_init_failed')}{Style.RESET_ALL}"
            )
            return
        force_update_config(translator)
    except Exception as e:
        print(
            f"{Fore.RED}❌ {translator.get('menu.config_init_failed', error=str(e))}{Style.RESET_ALL}"
        )
        return

    if config_manager.get_boolean("Utils", "check_update"):
        check_latest_version()

    menu_manager = MenuManager(translator)
    while True:
        try:
            print_menu(menu_manager)

            choice = input(
                f"\n➜ {Fore.CYAN}{translator.get('menu.input_choice', choices=f'0-{len(menu_manager.get_available_choices()) - 1}')}: {Style.RESET_ALL}"
            )
            choice = choice.strip()

            if choice == "0":
                print(
                    f"\n{Fore.YELLOW}ℹ️ {translator.get('menu.exit')}...{Style.RESET_ALL}"
                )
                print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
                break

            elif choice == "4":
                if handle_language_selection():
                    continue

            elif menu_manager.execute_choice(choice):
                continue

            else:
                print(
                    f"{Fore.RED}❌ {translator.get('menu.invalid_choice')}{Style.RESET_ALL}"
                )

        except KeyboardInterrupt:
            print(
                f"\n{Fore.YELLOW}ℹ️ {translator.get('menu.program_terminated')}{Style.RESET_ALL}"
            )
            print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
            break

        except Exception as e:
            print(
                f"{Fore.RED}❌ {translator.get('menu.error_occurred', error=str(e))}{Style.RESET_ALL}"
            )


if __name__ == "__main__":
    main()
