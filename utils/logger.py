from datetime import datetime
from colorama import Fore, Style, init

# تفعيل الألوان في الـ Terminal
init(autoreset=True)

class Logger:
    @staticmethod
    def get_time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def add(message: str):
        print(f'{Fore.CYAN}[{Logger.get_time()}]{Style.RESET_ALL} {Fore.GREEN}[+]{Style.RESET_ALL} {message}')

    @staticmethod
    def delete(message: str):
        print(f'{Fore.CYAN}[{Logger.get_time()}]{Style.RESET_ALL} {Fore.RED}[-]{Style.RESET_ALL} {message}')

    @staticmethod
    def warning(message: str):
        print(f'{Fore.CYAN}[{Logger.get_time()}]{Style.RESET_ALL} {Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}')

    @staticmethod
    def error(message: str):
        print(f'{Fore.CYAN}[{Logger.get_time()}]{Style.RESET_ALL} {Fore.RED}[ERROR]{Style.RESET_ALL} {message}')
        
    @staticmethod
    def info(message: str):
         print(f'{Fore.CYAN}[{Logger.get_time()}]{Style.RESET_ALL} {Fore.BLUE}[i]{Style.RESET_ALL} {message}')