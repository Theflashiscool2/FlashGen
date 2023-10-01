from datetime import datetime
from colorama import Fore
import threading

lock = threading.Lock()


class Log:
    def Success(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock.acquire()
        print(
            Fore.LIGHTGREEN_EX + "[" + Fore.LIGHTBLACK_EX + current_time + Fore.LIGHTGREEN_EX + "] [\] " + Fore.WHITE + text + Fore.RESET)
        lock.release()

    def Info(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock.acquire()
        print(
            Fore.LIGHTYELLOW_EX + "[" + Fore.LIGHTBLACK_EX + current_time + Fore.LIGHTYELLOW_EX + "] [!] " + Fore.WHITE + text + Fore.RESET)
        lock.release()

    def Error(text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        lock.acquire()
        print(Fore.RED + "[" + Fore.LIGHTBLACK_EX + current_time + Fore.LIGHTRED_EX + "] [-] " + Fore.WHITE + text + Fore.RESET)
        lock.release()
