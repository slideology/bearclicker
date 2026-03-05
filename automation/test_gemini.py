import google.generativeai as genai
import os
from PIL import Image

r_key = os.environ.get("GEMINI_API_KEY")
if not r_key:
    from dotenv import load_dotenv
    load_dotenv()
    r_key = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=r_key)
model = genai.GenerativeModel("gemini-1.5-flash")

print("Checking cookie_site_img.png")
img1 = Image.open("../tmp/cookie_site_img.png")
resp1 = model.generate_content(["Describe this image simply in 15 words. Identify if it shows a cookie or among us characters.", img1])
print("cookie_site_img.png:", resp1.text.strip())

print("\nChecking gamemonetize_img.jpg")
img2 = Image.open("../tmp/gamemonetize_img.jpg")
resp2 = model.generate_content(["Describe this image simply in 15 words. Identify if it shows a cookie or among us characters.", img2])
print("gamemonetize_img.jpg:", resp2.text.strip())
