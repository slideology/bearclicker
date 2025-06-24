import requests

data = {
    "host": "www.bearclicker.net/",
    "key": "79b10f40ab4848b5a84b4d154927ed13",
    "keyLocation": "https://bearclicker.net/79b10f40ab4848b5a84b4d154927ed13.txt",
    "urlList": [
       
        "https://bearclicker.net/god-simulator"
       
       
    ]
}

response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)