import requests

data = {
    "host": "www.pokemongammaemeraldgame.com",
    "key": "1097d5a190b24fcb941eacf89b4911b0",
    "keyLocation": "https://pokemongammaemeraldgame.com/1097d5a190b24fcb941eacf89b4911b0.txt",
    "urlList": [
        "https://pokemongammaemeraldgame.com/merge-fellas",
"https://pokemongammaemeraldgame.com/privacy-policy",
"https://pokemongammaemeraldgame.com/italian-brainrot-playground",
"https://pokemongammaemeraldgame.com/tung-sahur-clicker",
"https://pokemongammaemeraldgame.com/poor-bunny",
"https://pokemongammaemeraldgame.com/wacky-flip",
"https://pokemongammaemeraldgame.com/multi-theme-clicker-game",
"https://pokemongammaemeraldgame.com/drive-beyond-horizons",
"https://pokemongammaemeraldgame.com/contact",
"https://pokemongammaemeraldgame.com/speed-stars",
"https://pokemongammaemeraldgame.com/about",
"https://pokemongammaemeraldgame.com/faq",
"https://pokemongammaemeraldgame.com/italian-brainrot-2048",
"https://pokemongammaemeraldgame.com/terms-of-service",
"https://pokemongammaemeraldgame.com/merge-fellas-brainrot",
"https://pokemongammaemeraldgame.com/dreamy-room",
"https://pokemongammaemeraldgame.com/crazy-mouse-battle",
"https://pokemongammaemeraldgame.com/",
"https://pokemongammaemeraldgame.com/italian-brainrot-clicker-2",
"https://pokemongammaemeraldgame.com/lemon-clicker",
"https://pokemongammaemeraldgame.com/game"
    ]
}

response = requests.post(
    "https://api.indexnow.org/IndexNow",
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)

print("状态码：", response.status_code)
print("返回内容：", response.text)