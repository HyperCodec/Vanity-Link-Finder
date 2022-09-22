import json, requests, itertools, time, settings
from requests import RequestException

existinglinks = []
chars = "abcdefghigjklmnopqrstuvwxyz!$&-_=+,1234567890"

proxycycle = itertools.cycle(settings.proxies)

for length in range(1, 17):
    for link in itertools.product(chars, repeat=length):
        link = ''.join(link)
        proxy = next(proxycycle)

        try:
            response = requests.get(f"https://discordapp.com/api/invites/{link}", allow_redirects=True, proxies={"http": proxy, "https": proxy})

            print(f"Connected to https://discordapp.com/api/invites/{link} with status code {response.status_code} ({response.elapsed})")

            if response.status_code == 200:
                print(f"discord.gg/{link} is valid")

                existinglinks[link] = response.url

        except RequestException:
            print(f"Failed to connect to http://discord.gg/{link}")

        time.sleep(2)

print("Saving...")

try:
    with open("links.json", "r") as f:
        stuff = json.load(f)
except FileNotFoundError:
    with open("links.json", "w") as f:
        f.write("")
        json.dump(existinglinks, f, indent=4)
else:
    with open("links.json", "w") as f:
        for link in existinglinks:
            stuff[link] = existinglinks[link]

        json.dump(stuff, f, indent=4)

print("Saved!")
