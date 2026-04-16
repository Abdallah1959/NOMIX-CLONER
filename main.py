import os
import time
import sys
import shutil
import asyncio
import aiohttp
import discord
import json
import requests
import threading
import hashlib
import traceback
from datetime import datetime
from colorama import Fore, Style, init
from keyauth import api

from utils.logger import Logger
from utils.config import Config
from core.cloner import CloneEngine 

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
init(autoreset=True)

# === Fix Working Directory for EXE Builds ===
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
# ============================================

# === [ إجبار التيرمنال على دعم اللغة العربية (UTF-8) - تعديل المهندس ] ===
if os.name == "nt":
    os.system("chcp 65001 > nul")
    sys.stdout.reconfigure(encoding="utf-8")
# ========================================================================

os.system(f'title NOMIX CLONER {Config.VERSION}')

USER_TOKEN = None

# === إعداد مسار حفظ آمن للبيانات في الويندوز ===
APPDATA_DIR = os.path.join(os.getenv('APPDATA') or os.getcwd(), 'NOMIX')
os.makedirs(APPDATA_DIR, exist_ok=True)
LICENSE_PATH = os.path.join(APPDATA_DIR, 'nomix_license.txt')
# ================================================

# === نظام تسجيل الأخطاء الدقيق (Crash Logger) ===
def log_error(error):
    """تسجيل الأخطاء في ملف error.log داخل مسار آمن"""
    try:
        log_file_path = os.path.join(APPDATA_DIR, "error.log")
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Error: {str(error)}\n\n")
            f.write(traceback.format_exc())
    except Exception:
        pass
# ================================================

# =========================================================
# KeyAuth Security System
# =========================================================
def getchecksum():
    md5_hash = hashlib.md5()
    try:
        # التعديل السحري المتوافق مع Nuitka
        if "__compiled__" in globals() or getattr(sys, 'frozen', False):
            file_path = os.path.abspath(sys.argv[0])  # بيقرأ ملف الـ EXE نفسه
        else:
            file_path = os.path.abspath(__file__)

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5_hash.update(chunk)

        return md5_hash.hexdigest()
    except Exception as e:
        print(f"Checksum Error: {e}")
        return "checksum_error"

# تعريف تطبيق KeyAuth
keyauthapp = api(
    name="NOMIX CLONER",
    ownerid="MYqhYydMIF",
    version="1.0", # ⚠️ لازم تتأكد إن الرقم ده هو اللي موجود في الموقع بالظبط
    hash_to_check=getchecksum()
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_for_updates(auto_check=False):
    """دالة للتحقق من أحدث إصدار على جيت هاب"""
    current_version = Config.VERSION 
    repo_url = f"https://api.github.com/repos/{Config.GITHUB_REPO}/releases/latest"
    
    try:
        response = requests.get(repo_url, timeout=5)
        if response.status_code == 200:
            latest_version = response.json()['tag_name'] 
            
            clean_latest = latest_version.replace('v', '')
            clean_current = current_version.replace('v', '')
            
            if clean_latest != clean_current:
                if auto_check:
                    print_centered_text(f"\n{Fore.YELLOW}[!] NEW UPDATE AVAILABLE: v{clean_latest} !{Style.RESET_ALL}")
                    print_centered_text(f"{Fore.YELLOW}[!] Please select option [5] from the menu to update.{Style.RESET_ALL}")
                    time.sleep(3)
                return clean_latest
            else:
                if not auto_check:
                    print_centered_text(f"\n{Fore.GREEN}[✔] You are using the latest version (v{clean_current}).{Style.RESET_ALL}")
                    time.sleep(2)
                return False
    except Exception as e:
        if not auto_check:
            print_centered_text(f"\n{Fore.RED}[-] Failed to check for updates. Check your internet.{Style.RESET_ALL}")
            time.sleep(2)
        return False

def get_terminal_width():
    return shutil.get_terminal_size((100, 20)).columns

def draw_logo():
    term_width = get_terminal_width()
    logo_lines = [
        r"███╗   ██╗ ██████╗ ███╗   ███╗██╗██╗  ██╗     ██████╗ ██╗      ██████╗ ███╗   ██╗███████╗██████╗ ",
        r"████╗  ██║██╔═══██╗████╗ ████║██║╚██╗██╔╝    ██╔════╝ ██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗",
        r"██╔██╗ ██║██║   ██║██╔████╔██║██║ ╚███╔╝     ██║      ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝",
        r"██║╚██╗██║██║   ██║██║╚██╔╝██║██║ ██╔██╗     ██║      ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗",
        r"██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║██╔╝ ██╗    ╚██████╗ ███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║",
        r"╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═╝     ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝"
    ]
    logo_width = 95 
    logo_padding = max(0, (term_width - logo_width) // 2)
    
    print("\n")
    for line in logo_lines:
        print(" " * logo_padding + Fore.RED + line + Style.RESET_ALL)
        
    dev_text = f"Developed by: {Config.DEVELOPER}"
    dev_padding = max(0, (term_width - len(dev_text)) // 2)
    print(" " * dev_padding + Fore.MAGENTA + dev_text + Style.RESET_ALL)
    
    time_text = f"[ {Logger.get_time()} ]"
    time_padding = max(0, (term_width - len(time_text)) // 2)
    print(" " * time_padding + Fore.CYAN + time_text + Style.RESET_ALL)
    print("\n")

def draw_fixed_box(title, lines, box_width=75):
    term_width = get_terminal_width()
    box_padding = max(0, (term_width - box_width) // 2)
    pad_str = " " * box_padding
    title_text = f" {title} "
    left_dash = (box_width - len(title_text)) // 2
    right_dash = box_width - len(title_text) - left_dash
    
    print(pad_str + "╔" + "═" * left_dash + title_text + "═" * right_dash + "╗")
    print(pad_str + "║" + " " * box_width + "║")
    for line in lines:
        padding = box_width - len(line) - 4
        print(pad_str + "║    " + line + " " * max(0, padding) + "║")
    print(pad_str + "║" + " " * box_width + "║")
    print(pad_str + "╚" + "═" * box_width + "╝")

def print_centered_input_prompt(text):
    term_width = get_terminal_width()
    pad_str = " " * max(0, (term_width - 75) // 2)
    return input(f"{pad_str}{text}")

def print_centered_text(text):
    term_width = get_terminal_width()
    pad_str = " " * max(0, (term_width - 75) // 2)
    print(f"{pad_str}{text}")

# ==========================================
# Async API Helpers
# ==========================================
async def async_check_token(token):
    headers = {'Authorization': str(token)}
    async with aiohttp.ClientSession() as session:
        async with session.get('https://discord.com/api/v9/users/@me', headers=headers) as res:
            return res.status == 200

async def async_get_guild_info(token, guild_id):
    headers = {'Authorization': str(token)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://discord.com/api/v9/guilds/{guild_id}', headers=headers) as res:
            if res.status == 200:
                return await res.json()
            return None

async def async_get_guild_text_channels(token, guild_id):
    headers = {'Authorization': str(token)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://discord.com/api/v9/guilds/{guild_id}/channels', headers=headers) as res:
            if res.status == 200:
                data = await res.json()
                return [{"id": c["id"], "name": c["name"]} for c in data if c.get("type") == 0]
            return None

def run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

def show_token_guide():
    clear_screen()
    draw_logo()
    guide_lines = [
        "Step 1: Open Discord in your web browser and Login.",
        "Step 2: Press F12 to open Developer Tools.",
        "Step 3: Go to the 'Network' tab.",
        "Step 4: Press F5 to reload the page.",
        "Step 5: Type 'api' in the filter/search box.",
        "Step 6: Click on any request in the list below.",
        "Step 7: Scroll down to 'Request Headers' on the right.",
        "Step 8: Copy the value next to 'Authorization'."
    ]
    draw_fixed_box("HOW TO GET YOUR TOKEN", guide_lines)
    print("")

# --- [ الحارس المخفي ] ---
def background_security_patrol(interval=10):
    while True:
        time.sleep(interval)
        try:
            if keyauthapp.check() == False:
                raise SystemExit("BANNED")
        except BaseException as e:
            print(f"\n\n{Fore.RED}╔══════════════════════════════════════════════════════════════╗")
            print(f"║ [!] SECURITY ALERT: Your license was BANNED or EXPIRED!      ║")
            print(f"║ [!] Error Caught: {e}                                        ║")
            print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
            
            if os.path.exists(LICENSE_PATH):
                try:
                    os.remove(LICENSE_PATH)
                except:
                    pass
            
            time.sleep(3)
            os._exit(1)

def start_security_thread():
    thread = threading.Thread(
        target=background_security_patrol,
        daemon=True,
        name="SecurityPatrol"
    )
    thread.start()
# ---------------------------------------

def keyauth_login():
    key_file = LICENSE_PATH

    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            saved_key = f.read().strip()
        
        clear_screen()
        draw_logo()
        print_centered_text(f"{Fore.YELLOW}[*] Verifying saved license key...{Style.RESET_ALL}")
        
        try:
            keyauthapp.license(saved_key)
            Logger.add("Saved License Valid! Auto-Login successful.")
            time.sleep(1.5)
            start_security_thread() 
            return True
        except SystemExit:
            if os.path.exists(key_file): os.remove(key_file)
        except Exception:
            if os.path.exists(key_file): os.remove(key_file)

    while True:
        clear_screen()
        draw_logo()
        menu_lines = [
            "[1] > Enter License Key   (Login)",
            "[2] > Buy / Renew License (Purchase)",
            "[3] > Contact Support     (Help Desk)",
            "[0] > Exit App            (Close)"
        ]
        draw_fixed_box("WELCOME TO NOMIX CLONER", menu_lines)
        print("")
        
        choice = print_centered_input_prompt("[>] Choose Option : ").strip()
        
        if choice == '1':
            key = print_centered_input_prompt("\n[?] License Key > ").strip()
            Logger.info("Authenticating with KeyAuth Servers...")
            try:
                keyauthapp.license(key)
                Logger.add("License Authenticated Successfully! Welcome to NOMIX.")
                with open(key_file, "w") as f:
                    f.write(key)
                time.sleep(1.5)
                start_security_thread() 
                return True
            except SystemExit:
                Logger.error("Activation Failed: Invalid, Expired, or Banned Key.")
                time.sleep(3)
        elif choice == '2' or choice == '3':
            import webbrowser
            print_centered_text(f"\n{Fore.YELLOW}[*] Opening Discord Support in your browser...{Style.RESET_ALL}")
            time.sleep(1.5)
            webbrowser.open(Config.SUPPORT_LINK) 
        elif choice == '0':
            sys.exit()
        else:
            print_centered_text(f"{Fore.RED}[-] Invalid choice.{Style.RESET_ALL}")
            time.sleep(1)

def system_login():
    global USER_TOKEN
    while True:
        clear_screen()
        draw_logo()
        draw_fixed_box("SYSTEM LOGIN", ["Welcome to NOMIX CLONER.", "Please authenticate your session to continue."])
        print("")
        
        token = print_centered_input_prompt("[?] Enter Your Discord Token (Type 'help' for guide, '0' to exit) > ")
        
        if token == '0': sys.exit()
        elif token.lower() == 'help':
            show_token_guide()
            print_centered_input_prompt("Press Enter to continue...")
            continue
            
        print_centered_text("\n[*] Validating Token...")
        time.sleep(0.5)
        
        is_valid = run_async(async_check_token(token))
        if is_valid:
            Logger.add("Access Granted! Logging in...")
            check_for_updates(auto_check=True)
            time.sleep(1)
            USER_TOKEN = token
            main_menu()
            break
        else:
            Logger.error("Invalid Token! Please try again.")
            time.sleep(1.5)

def verify_security_status():
    if keyauthapp.check() == False:
        clear_screen()
        draw_logo()
        print_centered_text(f"{Fore.RED}[!] SECURITY ALERT: Your license has been banned or expired.{Style.RESET_ALL}")
        print_centered_text(f"{Fore.RED}[!] Force closing application...{Style.RESET_ALL}")
        
        if os.path.exists(LICENSE_PATH):
            os.remove(LICENSE_PATH)
            
        time.sleep(3)
        os._exit(1) 

def main_menu():
    clear_screen()
    draw_logo()
    menu_lines = [
        "[1] > Server Cloner             (Structure + Data)",
        "[2] > Server Wiper              (Selective Delete)",
        "[3] > Message Scraper           (Discord Backups) ",
        "[4] > Contact Developer         (Discord Support) ",
        "[5] > Check for Updates         (Version Checker) ",
        "[6] > Change Account            (Session Logout)  ",
        "[0] > Exit System               (Close App)       "
    ]
    draw_fixed_box("MAIN MENU", menu_lines)
    print("")
    
    while True:
        verify_security_status() 
        print_centered_text("[i] Type 'help' at any time for detailed instructions.")
        choice = print_centered_input_prompt("[>] Choose Tool : ").strip().lower()

        if choice == 'help':
            show_global_help()
            break
        elif choice == '1': cloner_mode(); break
        elif choice == '2': wiper_mode(); break
        elif choice == '3': scraper_mode(); break
        elif choice == '4':
            print_centered_text("\n[*] Opening Discord Support Server...")
            time.sleep(1)
            import webbrowser
            webbrowser.open(Config.SUPPORT_LINK)
            main_menu()
            break
        elif choice == '5':
            clear_screen()
            draw_logo()
            print_centered_text("[*] Checking GitHub for the latest version...")
            time.sleep(1)
            
            latest = check_for_updates(auto_check=False)
            if latest:
                print_centered_text(f"\n{Fore.GREEN}[!] Update v{latest} is available!{Style.RESET_ALL}")
                open_browser = print_centered_input_prompt("[?] Open download page in browser? (Y/N) > ").strip().lower()
                if open_browser == 'y':
                    import webbrowser
                    webbrowser.open(f"https://github.com/{Config.GITHUB_REPO}/releases/latest")
                    print_centered_text(f"{Fore.YELLOW}[*] Opening browser... Please download and install the new version.{Style.RESET_ALL}")
                    time.sleep(2)
            
            main_menu()
            break
        elif choice == '6':
            print_centered_text(f"\n{Fore.YELLOW}[*] Logging out...{Style.RESET_ALL}")
            time.sleep(1)
            system_login()
            break
        elif choice == '0': exit_system(); break
        else:
            print_centered_text(f"{Fore.RED}[-] Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1)
            clear_screen()
            draw_logo()
            draw_fixed_box("MAIN MENU", menu_lines)
            print("")

def show_global_help():
    clear_screen()
    draw_logo()
    help_lines = [
        "[1] Cloner  : Copies roles, channels, categories, emojis & stickers.",
        "[2] Wiper   : Deletes specific items or nukes a server completely.",
        "[3] Scraper : Backs up messages from specific channels to Discord HTML.",
        "[4] Support : Join our official Discord server for help & suggestions.",
        "[5] Update  : Check GitHub for the latest version of the tool.",
        "[6] Logout  : Sign out and enter a different token.",
        "[0] Exit    : Safely closes the application."
    ]
    draw_fixed_box("GLOBAL HELP", help_lines, box_width=85)
    print_centered_input_prompt("\nPress Enter to return to the menu...")
    main_menu()

def init_discord_client():
    try:
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
    except AttributeError:
        client = discord.Client()
    return client

def cloner_mode():
    while True: 
        clear_screen()
        draw_logo()
        draw_fixed_box("CLONING MODE", ["Welcome to the Server Cloner."])
        print("")
        
        while True:
            source_id = print_centered_input_prompt("[?] Source Server ID (To Copy From) or '0' to back > ")
            if source_id == '0': return main_menu()
            guild_from_info = run_async(async_get_guild_info(USER_TOKEN, source_id))
            if guild_from_info: break
            print_centered_text(f"{Fore.RED}[-] Invalid ID or No Permission. Try again.{Style.RESET_ALL}")

        while True:
            target_id = print_centered_input_prompt("[?] Target Server ID (To Paste To) or '0' to back > ")
            if target_id == '0': break 
            guild_to_info = run_async(async_get_guild_info(USER_TOKEN, target_id))
            if guild_to_info: break
            print_centered_text(f"{Fore.RED}[-] Invalid ID or No Permission. Try again.{Style.RESET_ALL}")

        if target_id == '0': continue 

        print_centered_text(f"\n{Fore.YELLOW}[*] INITIATING NOMIX CLONING PROTOCOL...{Style.RESET_ALL}")

        asyncio.set_event_loop(asyncio.new_event_loop())
        client = init_discord_client()

        @client.event
        async def on_ready():
            Logger.info(f"Logged in as: {client.user}")
            try:
                guild_from = client.get_guild(int(source_id))
                guild_to = client.get_guild(int(target_id))
                
                if not guild_from or not guild_to:
                    Logger.error("Cannot find servers. Check IDs.")
                    await client.close()
                    return
                
                Logger.info("Wiping target server...")
                await CloneEngine.roles_delete(guild_to)
                await CloneEngine.channels_delete(guild_to)
                await CloneEngine.emojis_delete(guild_to)
                await CloneEngine.stickers_delete(guild_to, USER_TOKEN) 
                
                Logger.info("Cloning Server Icon & Name...")
                await CloneEngine.guild_edit(guild_to, guild_from)
                Logger.info("Creating Roles...")
                await CloneEngine.roles_create(guild_to, guild_from)
                Logger.info("Creating Categories & Channels...")
                await CloneEngine.categories_create(guild_to, guild_from)
                await CloneEngine.channels_create(guild_to, guild_from)
                Logger.info("Cloning Emojis...")
                await CloneEngine.emojis_create(guild_to, guild_from)
                Logger.info("Cloning Stickers...")
                await CloneEngine.stickers_create(guild_to, guild_from, USER_TOKEN) 
                
                print_centered_text(f"\n{Fore.GREEN}[✔] SERVER FULLY CLONED SUCCESSFULLY!{Style.RESET_ALL}")
                
            except Exception as e:
                Logger.error(f"An error occurred: {e}")
            finally:
                await asyncio.sleep(2)
                await client.close() 

        client.run(USER_TOKEN, bot=False)

        again = print_centered_input_prompt(f"\n{Fore.YELLOW}[?] Do you want to Clone another server? (Y/N) > {Style.RESET_ALL}").strip().lower()
        if again != 'y':
            return main_menu()

def wiper_mode():
    while True: 
        clear_screen()
        draw_logo()
        draw_fixed_box("SERVER WIPER", [
            "Welcome to the Server Wiper.",
            "Warning: Proceed with extreme caution."
        ])
        print("")

        while True:
            target_id = print_centered_input_prompt("[?] Target Server ID (To Wipe) or '0' to back > ")
            if target_id == '0': return main_menu()
            guild_info = run_async(async_get_guild_info(USER_TOKEN, target_id))
            if guild_info: break
            print_centered_text(f"{Fore.RED}[-] Invalid ID or No Permission. Try again.{Style.RESET_ALL}")
            
        guild_name = guild_info.get('name', 'Unknown Server')

        while True: 
            clear_screen()
            draw_logo()
            print_centered_text(f"[*] Connected to: {Fore.CYAN}{guild_name}{Style.RESET_ALL}\n")
            
            wiper_menu = [
                "[1] > Delete ALL (Nuke)",
                "[2] > Delete Categories Only",
                "[3] > Delete Channels Only",
                "[4] > Delete Roles Only",
                "[5] > Delete Emojis Only",
                "[6] > Delete Stickers Only",
                "[0] > Change Server" 
            ]
            draw_fixed_box("WIPE OPTIONS", wiper_menu)
            print("")
            
            choice = print_centered_input_prompt("[>] Choose action : ").strip()
            
            if choice == '0': 
                break 
                
            if choice not in ['1', '2', '3', '4', '5', '6']:
                print_centered_text(f"{Fore.RED}[-] Invalid choice. Try again.{Style.RESET_ALL}")
                time.sleep(1)
                continue

            section_map = {'2': 'Categories', '3': 'Channels', '4': 'Roles', '5': 'Emojis', '6': 'Stickers'}

            if choice == '1':
                print_centered_text(f"\n{Fore.RED}[!] DANGER: You are about to wipe the ENTIRE server: '{guild_name}'{Style.RESET_ALL}")
                confirm = print_centered_input_prompt(f"{Fore.RED}[!] Type '{guild_name}' exactly to confirm (or '0' to cancel): {Style.RESET_ALL}")
                if confirm != guild_name:
                    print_centered_text(f"{Fore.YELLOW}[-] Cancelled.{Style.RESET_ALL}")
                    time.sleep(1)
                    continue 
            else:
                section_name = section_map[choice]
                confirm = print_centered_input_prompt(f"{Fore.YELLOW}[?] Are you sure you want to wipe ALL {section_name} from '{guild_name}'? (Y/N) : {Style.RESET_ALL}").lower()
                if confirm != 'y': 
                    continue 

            print_centered_text(f"\n{Fore.YELLOW}[*] EXECUTING WIPE PROTOCOL ON '{guild_name}'...{Style.RESET_ALL}")
            
            asyncio.set_event_loop(asyncio.new_event_loop())
            client = init_discord_client()

            @client.event
            async def on_ready():
                try:
                    guild_to = client.get_guild(int(target_id))
                    if choice == '1':
                        await CloneEngine.channels_delete(guild_to)
                        await CloneEngine.roles_delete(guild_to)
                        await CloneEngine.emojis_delete(guild_to)
                        await CloneEngine.stickers_delete(guild_to, USER_TOKEN)
                    elif choice == '2': await CloneEngine.categories_delete_only(guild_to)
                    elif choice == '3': await CloneEngine.channels_delete_only(guild_to)
                    elif choice == '4': await CloneEngine.roles_delete(guild_to)
                    elif choice == '5': await CloneEngine.emojis_delete(guild_to)
                    elif choice == '6': await CloneEngine.stickers_delete(guild_to, USER_TOKEN)

                    print_centered_text(f"\n{Fore.GREEN}[✔] WIPE TASK COMPLETED SUCCESSFULLY!{Style.RESET_ALL}")
                except Exception as e:
                    pass
                finally:
                    await asyncio.sleep(2)
                    await client.close()

            client.run(USER_TOKEN, bot=False)
            
            again = print_centered_input_prompt(f"\n{Fore.YELLOW}[?] Do you want to Wipe something else in THIS server? (Y/N) > {Style.RESET_ALL}").strip().lower()
            if again == 'y':
                continue 
            else:
                return main_menu() 

def scraper_mode():
    while True: 
        clear_screen()
        draw_logo()
        draw_fixed_box("MESSAGE SCRAPER", ["Backup your channels in Discord UI format."])
        print("")

        while True:
            server_id = print_centered_input_prompt("[?] Target Server ID or '0' to back > ")
            if server_id == '0': return main_menu()
            guild_info = run_async(async_get_guild_info(USER_TOKEN, server_id))
            if guild_info: break
            print_centered_text(f"{Fore.RED}[-] Invalid ID or No Permission. Try again.{Style.RESET_ALL}")
            
        server_name = guild_info.get('name', 'Unknown_Server')
        
        while True: 
            clear_screen()
            draw_logo()
            print_centered_text(f"[*] Connected to: {Fore.CYAN}{server_name}{Style.RESET_ALL}")
            channels_data = run_async(async_get_guild_text_channels(USER_TOKEN, server_id))
            
            if not channels_data:
                print_centered_text(f"{Fore.RED}[-] No text channels found or permission denied.{Style.RESET_ALL}")
                time.sleep(2)
                break 

            print_centered_text("\n[!] Available Text Channels:")
            for i, ch in enumerate(channels_data):
                print_centered_text(f"[{i+1}] #{ch['name']}")
                
            print_centered_text(f"\n{Fore.YELLOW}[i] Tip: Type numbers separated by commas (e.g., 1,2), 'all', or '0' to change server.{Style.RESET_ALL}")
            
            selected = print_centered_input_prompt("[>] Select Channels > ").strip().lower()
            
            if selected == '0': break 
            if not selected: continue

            proceed = True
            if selected == 'all':
                print_centered_text(f"\n{Fore.RED}╔══════════════════════════ DANGER ZONE ══════════════════════════╗")
                print_centered_text("║ [!] WARNING: Scraping an entire server can result in a BAN.     ║")
                print_centered_text("║  [Y] Proceed at own risk  |  [N] Cancel                         ║")
                print_centered_text(f"╚═════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
                confirm_all = print_centered_input_prompt("[>] Confirm : ").strip().lower()
                if confirm_all != 'y': proceed = False
                    
            if not proceed: continue 
                
            print_centered_text("\n[?] Choose Export Format:")
            print_centered_text("[1] HTML (Discord Replica - JS Engine) ")
            print_centered_text("[2] TXT  (Clean plain text with links) ")
            print_centered_text("[3] JSON (Raw data for Bots)           ")
            
            while True:
                fmt_choice = print_centered_input_prompt("[>] Format or '0' to back > ").strip()
                if fmt_choice in ['0', '1', '2', '3']: break
                print_centered_text(f"{Fore.RED}[-] Invalid choice.{Style.RESET_ALL}")
                
            if fmt_choice == '0': continue 
                
            format_type = {'1': 'html', '2': 'txt', '3': 'json'}[fmt_choice]
            
            while True:
                limit = print_centered_input_prompt("[>] How many messages per channel? (Max 100) or '0' to back > ").strip()
                if limit == '0': break
                if limit.isdigit():
                    limit_num = int(limit)
                    break
                print_centered_text(f"{Fore.RED}[-] Please enter a valid number.{Style.RESET_ALL}")
                
            if limit == '0': continue 
                
            channels_to_scrape = []
            if selected == 'all': channels_to_scrape = channels_data
            else:
                indices = [int(x.strip())-1 for x in selected.split(',') if x.strip().isdigit()]
                for idx in indices:
                    if 0 <= idx < len(channels_data): channels_to_scrape.append(channels_data[idx])
            
            print_centered_text("\n[*] Initializing Async Embed Scraper...")
            success_count = 0
            
            async def run_scraper():
                count = 0
                for ch in channels_to_scrape:
                    print_centered_text(f"[*] Fetching messages from #{ch['name']}...")
                    saved_path = await scrape_messages_async(USER_TOKEN, server_name, ch['id'], ch['name'], limit_num, format_type)
                    if saved_path:
                        Logger.add(f"Saved: {saved_path}")
                        count += 1
                        await asyncio.sleep(0.5)
                return count

            success_count = run_async(run_scraper())
            
            if success_count > 0:
                print_centered_text(f"\n{Fore.GREEN}[✔] Backup Completed! Saved {success_count} channels.{Style.RESET_ALL}")
            else:
                print_centered_text(f"\n{Fore.RED}[-] Backup Failed or Skipped due to permissions.{Style.RESET_ALL}")

            again = print_centered_input_prompt(f"\n{Fore.YELLOW}[?] Do you want to Scrape another channel in THIS server? (Y/N) > {Style.RESET_ALL}").strip().lower()
            if again == 'y': continue 
            else: return main_menu() 

def clean_carlbot_embed(embed):
    allowed_keys = {
        "title", "description", "url", "color",
        "fields", "author", "footer", "thumbnail",
        "image", "timestamp"
    }

    cleaned = {k: v for k, v in embed.items() if k in allowed_keys}

    if "fields" in cleaned:
        cleaned["fields"] = [
            {
                "name": field.get("name", ""),
                "value": field.get("value", ""),
                "inline": field.get("inline", False)
            }
            for field in cleaned["fields"]
        ]

    return cleaned

async def scrape_messages_async(token, server_name, channel_id, channel_name, limit, format_type):
    headers = {"Authorization": str(token)}
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://discord.com/api/v9/channels/{channel_id}/messages?limit={limit}", headers=headers) as res:
            if res.status == 200:
                messages = await res.json()
                
                if not messages:
                    Logger.warning(f"No messages found in #{channel_name}.")
                    return False
                    
                if format_type in ['txt', 'html']:
                    messages = messages[::-1] 
                    
                folder_path = os.path.join("Cloned_Messages", server_name)
                os.makedirs(folder_path, exist_ok=True)
                safe_name = "".join(x for x in channel_name if x.isalnum() or x in " -_")
                
                if format_type == 'json':
                    file_path = os.path.join(folder_path, f"{safe_name}.json")
                    
                    carlbot_messages = []
                    for msg in messages:
                        carl_msg = {}
                        if msg.get('content'): 
                            carl_msg['content'] = msg['content']
                        if msg.get('embeds') and len(msg['embeds']) > 0:
                            carl_msg['embed'] = clean_carlbot_embed(msg['embeds'][0])
                        if carl_msg: 
                            carlbot_messages.append(carl_msg)
                            
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(carlbot_messages, f, indent=4, ensure_ascii=False)
                        
                elif format_type == 'txt':
                    file_path = os.path.join(folder_path, f"{safe_name}.txt")
                    with open(file_path, "w", encoding="utf-8") as f:
                        for msg in messages:
                            author = msg.get('author', {}).get('username', 'Unknown')
                            date = str(msg.get('timestamp', ''))[:16].replace('T', ' ')
                            f.write(f"[{date}] {author}:\n")
                            
                            content = str(msg.get('content') or '')
                            if content: f.write(f"{content}\n")
                            
                            for embed in msg.get('embeds') or []:
                                f.write("--- [Embed] ---\n")
                                if embed.get('title'): f.write(f"Title: {embed['title']}\n")
                                if embed.get('description'): f.write(f"Desc: {embed['description']}\n")
                                for field in embed.get('fields') or []:
                                    f.write(f"Field: {field.get('name')} -> {field.get('value')}\n")
                                if embed.get('image'): f.write(f"Image Link: {embed['image'].get('url')}\n")
                                f.write("---------------\n")
                                
                            for att in msg.get('attachments') or []:
                                f.write(f"[Attachment Link]: {att.get('url', '')}\n")
                            f.write(f"{'='*50}\n")
                            
                elif format_type == 'html':
                    file_path = os.path.join(folder_path, f"{safe_name}.html")
                    json_data = json.dumps(messages, ensure_ascii=False) 
                    
                    html_content = f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="UTF-8">
    <title>#{safe_name} - Discord Export</title>
    <style>
        :root {{ --bg: #313338; --bg-embed: #2b2d31; --text: #dbdee1; --text-muted: #949ba4; --header: #f2f3f5; --blurple: #5865F2; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px 40px; margin: 0; }}
        .header {{ font-size: 24px; font-weight: bold; color: white; border-bottom: 1px solid #424549; padding-bottom: 15px; margin-bottom: 20px; }}
        .header::before {{ content: '#'; color: var(--text-muted); margin-right: 10px; font-size: 30px; font-weight: normal; }}
        
        .msg {{ display: flex; margin-bottom: 20px; }}
        .avatar {{ width: 40px; height: 40px; border-radius: 50%; margin-right: 15px; background: var(--blurple); object-fit: cover; flex-shrink: 0; }}
        .msg-content-container {{ max-width: 800px; width: 100%; }}
        .name-date {{ margin-bottom: 5px; }}
        .uname {{ color: var(--header); font-weight: 500; font-size: 16px; margin-right: 10px; }}
        .date {{ color: var(--text-muted); font-size: 12px; }}
        .content {{ white-space: pre-wrap; word-break: break-word; line-height: 1.4; }}
        .content a {{ color: #00a8fc; text-decoration: none; }} .content a:hover {{ text-decoration: underline; }}
        
        .embed {{ background: var(--bg-embed); border-left: 4px solid #202225; border-radius: 4px; padding: 12px 16px; margin-top: 8px; max-width: 520px; }}
        .embed-author {{ display: flex; align-items: center; margin-bottom: 8px; font-weight: 600; color: white; font-size: 14px; }}
        .embed-author img {{ width: 24px; height: 24px; border-radius: 50%; margin-right: 8px; object-fit: cover; }}
        .embed-title {{ color: #00a8fc; font-weight: 600; margin-bottom: 8px; text-decoration: none; display: block; font-size: 15px; word-break: break-word; }}
        .embed-desc {{ white-space: pre-wrap; font-size: 14px; margin-bottom: 8px; line-height: 1.375; }}
        .embed-fields {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 8px; }}
        .embed-field {{ flex: 1 1 100%; }}
        .embed-field.inline {{ flex: 1 1 calc(50% - 10px); }}
        .embed-field-name {{ font-weight: 600; color: white; font-size: 14px; margin-bottom: 2px; }}
        .embed-field-value {{ font-size: 14px; white-space: pre-wrap; }}
        .embed-image {{ max-width: 100%; max-height: 400px; border-radius: 4px; margin-top: 10px; object-fit: contain; }}
        .embed-thumb {{ max-width: 80px; max-height: 80px; border-radius: 4px; float: right; margin-left: 15px; object-fit: cover; }}
        .embed-footer {{ display: flex; align-items: center; font-size: 12px; color: var(--text-muted); margin-top: 8px; }}
        .embed-footer img {{ width: 20px; height: 20px; border-radius: 50%; margin-right: 8px; object-fit: cover; }}
        
        .attachment-img {{ max-width: 400px; max-height: 350px; border-radius: 8px; margin-top: 8px; display: block; object-fit: contain; }}
        .attachment-file {{ background: var(--bg-embed); padding: 10px 15px; border-radius: 4px; border: 1px solid #424549; display: inline-block; margin-top: 8px; }}
        .attachment-file a {{ color: #00a8fc; text-decoration: none; font-size: 14px; }}
        
        .btn-row {{ display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap; }}
        .btn {{ padding: 8px 16px; border-radius: 3px; color: white; font-size: 14px; font-weight: 500; cursor: default; display: flex; align-items: center; justify-content: center; }}
        .btn-1 {{ background: var(--blurple); }} .btn-2 {{ background: #4e5058; }} .btn-3 {{ background: #23a559; }} .btn-4 {{ background: #da373c; }} .btn-5 {{ background: #4e5058; color: #00a8fc; }}
    </style>
</head>
<body>
    <div class="header">{safe_name}</div>
    <div id="chat"></div>

    <script>
        const messages = {json_data};
        const chatDiv = document.getElementById('chat');

        function formatText(text) {{
            if (!text) return '';
            let html = text.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\\n/g, '<br>');
            html = html.replace(/(https?:\\/\\/[^\\s]+)/g, '<a href="$1" target="_blank">$1</a>');
            html = html.replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>'); 
            html = html.replace(/\\*(.*?)\\*/g, '<i>$1</i>'); 
            html = html.replace(/~~(.*?)~~/g, '<s>$1</s>'); 
            html = html.replace(/__(.*?)__/g, '<u>$1</u>'); 
            return html;
        }}

        messages.forEach(msg => {{
            const div = document.createElement('div');
            div.className = 'msg';
            
            const author = msg.author || {{}};
            const username = author.username || 'Unknown';
            const avHash = author.avatar;
            const avUrl = avHash ? `https://cdn.discordapp.com/avatars/${{author.id}}/${{avHash}}.png` : 'https://cdn.discordapp.com/embed/avatars/0.png';
            const date = msg.timestamp ? msg.timestamp.substring(0, 16).replace('T', ' ') : '';
            
            let html = `<img src="${{avUrl}}" class="avatar"><div class="msg-content-container"><div class="name-date"><span class="uname">${{username}}</span><span class="date">${{date}}</span></div>`;
            
            if (msg.content) {{
                html += `<div class="content">${{formatText(msg.content)}}</div>`;
            }}
            
            if (msg.embeds && msg.embeds.length > 0) {{
                msg.embeds.forEach(embed => {{
                    const color = embed.color ? `#${{embed.color.toString(16).padStart(6, '0')}}` : '#202225';
                    html += `<div class="embed" style="border-left-color: ${{color}};">`;
                    
                    if (embed.thumbnail && embed.thumbnail.url) {{
                        html += `<img src="${{embed.thumbnail.url}}" class="embed-thumb">`;
                    }}
                    
                    if (embed.author) {{
                        html += `<div class="embed-author">`;
                        if (embed.author.icon_url) html += `<img src="${{embed.author.icon_url}}">`;
                        html += `<span>${{formatText(embed.author.name)}}</span></div>`;
                    }}
                    
                    if (embed.title) {{
                        if (embed.url) html += `<a href="${{embed.url}}" target="_blank" class="embed-title">${{formatText(embed.title)}}</a>`;
                        else html += `<div class="embed-title">${{formatText(embed.title)}}</div>`;
                    }}
                    
                    if (embed.description) {{
                        html += `<div class="embed-desc">${{formatText(embed.description)}}</div>`;
                    }}
                    
                    if (embed.fields && embed.fields.length > 0) {{
                        html += `<div class="embed-fields">`;
                        embed.fields.forEach(f => {{
                            const inlineClass = f.inline ? 'inline' : '';
                            html += `<div class="embed-field ${{inlineClass}}"><div class="embed-field-name">${{formatText(f.name)}}</div><div class="embed-field-value">${{formatText(f.value)}}</div></div>`;
                        }});
                        html += `</div>`;
                    }}
                    
                    if (embed.image && embed.image.url) {{
                        html += `<img src="${{embed.image.url}}" class="embed-image">`;
                    }}
                    
                    if (embed.footer) {{
                        html += `<div class="embed-footer">`;
                        if (embed.footer.icon_url) html += `<img src="${{embed.footer.icon_url}}">`;
                        html += `<span>${{formatText(embed.footer.text)}}</span></div>`;
                    }}
                    
                    html += `</div>`;
                }});
            }}
            
            if (msg.components && msg.components.length > 0) {{
                msg.components.forEach(row => {{
                    if (row.type === 1) {{ 
                        html += `<div class="btn-row">`;
                        row.components.forEach(btn => {{
                            if (btn.type === 2) {{ 
                                const style = btn.style || 2;
                                let btnHtml = `<div class="btn btn-${{style}}">`;
                                if (btn.emoji) {{
                                    if (btn.emoji.id) {{
                                        const ext = btn.emoji.animated ? 'gif' : 'png';
                                        btnHtml += `<img src="https://cdn.discordapp.com/emojis/${{btn.emoji.id}}.${{ext}}" style="width:18px;height:18px;margin-right:6px;object-fit:contain;">`;
                                    }} else if (btn.emoji.name) {{
                                        btnHtml += `<span style="margin-right:6px;">${{btn.emoji.name}}</span>`;
                                    }}
                                }}
                                btnHtml += `${{btn.label || ''}}</div>`;
                                
                                if (style === 5 && btn.url) {{
                                    html += `<a href="${{btn.url}}" target="_blank" style="text-decoration:none;">${{btnHtml}}</a>`;
                                }} else {{
                                    html += btnHtml;
                                }}
                            }}
                        }});
                        html += `</div>`;
                    }}
                }});
            }}
            
            if (msg.attachments && msg.attachments.length > 0) {{
                msg.attachments.forEach(att => {{
                    if (att.url.match(/\.(jpeg|jpg|gif|png|webp)$/i)) {{
                        html += `<img src="${{att.url}}" class="attachment-img">`;
                    }} else {{
                        html += `<div class="attachment-file">📁 <a href="${{att.url}}" target="_blank">${{att.filename}}</a></div>`;
                    }}
                }});
            }}
            
            html += `</div></div>`;
            div.innerHTML = html;
            chatDiv.appendChild(div);
        }});
    </script>
</body>
</html>"""
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                        
                return os.path.abspath(file_path)
            else:
                Logger.error(f"Failed to fetch. Status Code: {res.status}")
            return False

def exit_system():
    clear_screen()
    draw_logo()
    exit_lines = [
        "[!] Are you sure you want to exit?",
        "[Y] Yes, exit now  | [N] No, return to menu"
    ]
    draw_fixed_box("SYSTEM EXIT", exit_lines)
    while True:
        confirm = print_centered_input_prompt("\n[>] Confirm : ").strip().lower()
        if confirm == 'y':
            print_centered_text("\n[*] Shutting down NOMIX OS...")
            time.sleep(1)
            sys.exit()
        elif confirm == 'n':
            main_menu()
            break
        else:
            print_centered_text(f"{Fore.RED}[-] Invalid input.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        if keyauth_login():
            system_login()
        else:
            sys.exit()
    except Exception as e:
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        print("\nAn unexpected error occurred.")
        print("Check 'error.log' for more details.")
        input("\nPress Enter to exit...")
