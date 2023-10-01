import random
import re
import string
from json import dumps, loads
from base64 import b64encode
import os

import httpx
import requests

from utils.ui import Log

config = loads(open("info/config.json", "r").read())


class Utils(object):
    @staticmethod
    def GetBirthday():
        year = str(random.randrange(1997, 2001))
        month = str(random.randrange(1, 12))
        day = str(random.randrange(1, 28))
        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day

        return f"{year}-{month}-{day}"

    @staticmethod
    def RandomEmail():
        return ''.join(random.choice(string.ascii_letters) for i in range(10)) + '@gmail.com'

    @staticmethod
    def Password():
        if config["password"] == "random":
            return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(10))
        else:
            return config["password"]
    @staticmethod
    def PickUserAgent():
        return open("info/useragents.txt", encoding="utf-8").read().splitlines()[
            random.randint(0, len(open("info/useragents.txt", encoding="utf-8").read().splitlines()) - 1)]
    @staticmethod
    def username():
        return open("info/usernames.txt", encoding="utf-8").read().splitlines()[
            random.randint(0, len(open("info/usernames.txt", encoding="utf-8").read().splitlines()) - 1)] + \
            open("info/usernames.txt", encoding="utf-8").read().splitlines()[
                random.randint(0, len(open("info/usernames.txt", encoding="utf-8").read().splitlines()) - 1)] + \
            open("info/usernames.txt", encoding="utf-8").read().splitlines()[
                random.randint(0, len(open("info/usernames.txt", encoding="utf-8").read().splitlines()) - 1)]

    @staticmethod
    def GetProperties(buildNum: int):
        return b64encode(dumps({"os": "Windows", "browser": "Chrome", "device": "", "system_locale": "pl-PL",
                                "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                                "browser_version": "108.0.0.0", "os_version": "10", "referrer": "",
                                "referring_domain": "", "referrer_current": "", "referring_domain_current": "",
                                "release_channel": "stable", "client_build_number": buildNum,
                                "client_event_source": None, "design_id": 0}).encode()).decode()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def RandomProxy():
        proxysources = [
            ["http://spys.me/proxy.txt", "%ip%:%port% "],
            ["http://www.httptunnel.ge/ProxyListForFree.aspx", " target=\"_new\">%ip%:%port%</a>"],
            ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json",
             "\"ip\":\"%ip%\",\"port\":\"%port%\","],
            ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list",
             '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
            ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt",
             '%ip%:%port% (.*?){2}-.-S \\+'],
            ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
             '%ip%", "type": "http", "port": %port%'],
            ["https://www.us-proxy.org/",
             "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
            ["https://free-proxy-list.net/",
             "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
            ["https://www.sslproxies.org/",
             "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
            ["https://www.proxy-list.download/api/v0/get?l=en&t=https", '"IP": "%ip%", "PORT": "%port%",'],
            [
                "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all",
                "%ip%:%port%"],
            ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
            ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
            ["https://proxylist.icu/", "<td>%ip%:%port%</td><td>http<"],
            ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
            ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
            ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
            ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
            ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
            ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
            ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json",
             '"ip": "%ip%",\n.*?"port": "%port%",']
        ]
        random.shuffle(proxysources)

        for proxy in proxysources:
            url = proxy[0]
            custom_regex = proxy[1]
            proxylist = requests.get(url, timeout=5).text
            proxylist = proxylist.replace('null', '"N/A"')
            custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
            custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')

            matching_proxies = re.findall(re.compile(custom_regex), proxylist)

            random.shuffle(matching_proxies)

            for proxy in matching_proxies:
                return proxy[0] + ":" + proxy[1]
    @staticmethod
    def get_js() -> str:
        try:
            resp = httpx.get("https://discord.com/app")
            resp.raise_for_status()
        except httpx.HTTPError as e:
            Log.Error(f"HTTP error occurred while fetching latest JS version: {e}")
            return ""

        try:
            js_version = resp.text.split('"></script><script src="/assets/')[2].split('" integrity')[0]
            return js_version
        except IndexError:
            Log.Error("Failed to parse JS version from response.")
            return ""
    @staticmethod
    def BuildNumber():
        js_version = Utils.get_js()
        url = f"https://discord.com/assets/{js_version}"

        resp = requests.get(url)
        body = resp.content.decode()

        regex_pattern = r'"buildNumber",null!==\(t="(\d+)"\)\?t:""\)'

        regex = re.compile(regex_pattern)
        match = regex.search(body)

        if match:
            build_number = match.group(1)
            return build_number
        else:
            Log.Error("Build number not found in the body text.")
            return ""
