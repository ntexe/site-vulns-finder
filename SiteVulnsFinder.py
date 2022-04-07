from requests import get
from os import system
from user_agent import generate_user_agent

system("")

# sorry for my English, I'm from Ukraine •___•

f = open("links.txt") # Opening links file (read-only)
site = input("Enter Site (example: google.com): ").replace("http://", "").replace("https://", "").split("/")[0]
scanCont = input("Scan content for string \"404\"? (default is \"n\", but if you getting fake pages, type \"y\"): ").replace(" ", "").lower() == "y"

links = f.read().splitlines()

history = {i.split()[0]:i.split()[1] for i in open("scanHistory", "r+").read().splitlines()} # openning with w+ for creating a file, if it doesn't exits

if site in history:
	if input(f"Continue previous scan of {site}? (y/n): ").replace(" ", "").lower() == "y":
		del links[:int(history[site])]

linkNum = 0

print("Available links: ")
for line in links:
	reqLink = f"http://{site}/{line}"
	try:
		resp = get(reqLink, headers = {'User-Agent': generate_user_agent()}, stream = True) # Getting page
		if resp.status_code == 404 or (None if not scanCont else ('404' in resp.raw.read(16777216).decode('utf8'))):
			print(f"\033[;91mNot Found\033[;90m {reqLink}\033[0m")

		elif resp.status_code == 200:
			print(f"\033[;92mValid\033[0m {reqLink}")
			with open("Valid.txt", "a") as fl: # Opening Valid.txt file, writing link and closing
				fl.write(f"{reqLink}\n")
				fl.close()

		elif resp.status_code == 429:
			print(f"\033[;91mToo many requests error\033[0m {reqLink}")

		elif resp.status_code == 403:
			print(f"\033[;91mForbidden\033[0m {reqLink}")

		else:
			print(f"\033[;33mUnknown response code: \033[0m{reqLink} => \033[;33m{resp.status_code}\033[0m")
			with open("Unknown.txt", "a") as fl: # Opening Unknown.txt file, writing link and closing
				fl.write(f"{reqLink} => {resp.status_code}\n")
				fl.close()

		linkNum += 1

		if linkNum % 16 == 0:
			open("scanHistory", "w").write(f"{site} {linkNum}")
	except Exception as e:
		print(e)

input("Scan end")
