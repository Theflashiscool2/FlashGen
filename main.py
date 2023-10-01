import json

import time

from utils.ui import Log
from utils.utils import Utils
import tls_client
import httpx

import os
import onest_captcha

if not os.path.exists("info"):
    os.mkdir("info")

config = json.load(open("info/config.json", encoding="utf-8"))

if config['invite_code'] == "":
    invite = input(Log.Info("Enter Invite Code"))
else:
    invite = config['invite_code']

threadcount = int(config['threads'])

genned = 0
errors = 0
solved = 0
StartTime = time.time()
server_name = \
    httpx.get(f"https://discord.com/api/v9/invites/{invite}?with_counts=true&with_expiration=true").json()["guild"][
        "name"]


class Console():
    global genned
    global errors
    global solved

    def __init__(self):
        self.title = f"{server_name} | Genned : {genned} | Errors: {errors} | Solved: {solved} | Elapsed: {round(time.time() - StartTime, 2)}s"


build_number = int(Utils.BuildNumber())
if build_number == "":
    Log.Error("Failed to parse build number, please try again later.")
    exit()
else:
    Utils.clear()
    Log.Info(f"Build number: {build_number}")

Console()


def main():
    date = Utils.GetBirthday()
    ua = Utils.PickUserAgent()
    # implement proxies. Proxy not working
    # proxy = Utils.RandomProxy()
    # formattedProxy = f"http://{proxy}"
    global genned, solved, \
        errors
    client = tls_client.Session(client_identifier='chrome_108')
    resp = client.get("https://discord.com/api/v9/experiments")
    fingerprint = resp.json()['fingerprint']
    time_solve = time.time()
    solv = onest_captcha.OneStCaptchaClient(config["captchakey"])
    capresp = solv.h_captcha_task_proxyless('https://discord.com/', site_key='4c672d35-0701-42b2-88c3-78380b0db560')
    key = capresp.get("token")
    time_solve = time.time() - time_solve
    Log.Info(f"Solved key in {round(time_solve, 2)}s")
    solved += 1
    Console()

    data = {
        'fingerprint': fingerprint,
        'email': str(Utils.RandomEmail()),
        'username': str(Utils.username()),
        'password': str(Utils.Password()),
        'invite': invite,
        'consent': True,
        'date_of_birth': date,
        "gift_code_sku_id": None,
        "captcha_key": key,
        "promotional_email_opt_in": True
    }

    headers = {
        'origin': 'https://discord.com',
        'referer': f'https://discord.gg/{invite}',
        'x-discord-locale': 'en-US',
        'x-debug-options': 'bugReporterEnabled',
        'user-agent': ua,
        'x-fingerprint': fingerprint,
        'x-super-properties': Utils.GetProperties(build_number),
        'Content-Type': 'application/json'
    }

    response = client.post('https://discord.com/api/v9/auth/register', json=data, headers=headers)
    if response.status_code == 201:
        token = response.json()['token']
        Log.Success(f"Generated {token[:40]}.......")
        genned += 1
        Console()
        with open(f"tokens.txt", "a", encoding="utf-8") as f:
            f.write(f"{token}\n")

    elif response.status_code == 429:
        Log.Error("Rate Limited.")
        errors += 1
        Console()

    elif 'captcha' in response.text:
        Log.Error("Captcha Data Invalid")
        errors += 1
        Console()

    else:
        Log.Error("Unknown Error")
        errors += 1
        Console()


