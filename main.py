import requests, time, random, string

TOKEN = "MTI0OTU5NDgyMzM5MzAyMTk3Nw.G8wr5m.9M_HeHMlnN6AdUaCkdFBpsHHGbVbw-NgAeNbwY"
CHANNEL_ID = "1543105367561474052"

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}
url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"

last_msg = ""
while True:
    while True:
        text = "".join(random.choice(string.ascii_lowercase) for _ in range(random.randint(8, 15)))
        if text != last_msg: break
    
    res = requests.post(url, headers=headers, json={"content": text})
    if res.status_code == 200:
        print(f"[+] Da gui: {text}")
        last_msg = text
    else:
        print(f"[-] Loi: {res.status_code}")
    
    time.sleep(10)
