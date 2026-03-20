import requests
from bs4 import BeautifulSoup
import json
import os
import urllib.parse
import time

def build_image_map():
    base_url = "https://cookie-clicker2.com"
    ajax_url = "https://cookie-clicker2.com/paging.ajax"
    headers = {
        "User-Agent": "curl/7.81.0"
    }
    
    game_map = {}
    page = 1
    
    while True:
        print(f"Scraping page {page} via AJAX...")
        payload = {"page": str(page)}
        
        try:
            resp = requests.post(ajax_url, data=payload, headers=headers, timeout=15)
            # The server actually returns a JSON-encoded string containing HTML (e.g. `" <div class=\"... "`)
            try:
                html_content = json.loads(resp.text)
                if isinstance(html_content, dict):
                    html_content = html_content.get("content", html_content.get("html", html_content.get("data", "")))
            except:
                html_content = resp.text
            
            soup = BeautifulSoup(html_content, "html.parser")
            games = soup.find_all("a", href=True)
            
            if not games:
                print(f"No more games found on page {page}, ending.")
                break
                
            items_found_on_page = 0
            for a in games:
                href = a.get("href", "")
                if href.startswith("/") and len(href) > 2 and not "games/" in href and href not in ["/all-games", "/new-games", "/hot-games"]:
                    slug = href.strip("/")
                    img = a.find("img")
                    if img and img.get("src"):
                        src = img.get("src")
                        # 跳过极小缩略图（24x24），保留所有其他有效图片
                        if "m24x24" in src:
                            continue
                        # 补全相对路径
                        if not src.startswith("http"):
                            src = urllib.parse.urljoin(base_url, src)
                        # 优先选较大的 m250x195 图，或保留第一个找到的
                        if slug not in game_map or "m250x195" in src:
                            game_map[slug] = src
                            items_found_on_page += 1
            
            if items_found_on_page == 0:
                print(f"No valid games found on page {page}, possibly end of list.")
                break
                
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
            
        page += 1
        time.sleep(0.5)
        
    out_dir = "../static/data"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "game_images_map.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(game_map, f, indent=2)
    print(f"Successfully saved {len(game_map)} game image mappings to {out_path}.")
    
    print("among-us-clicker == ", game_map.get("among-us-clicker"))

if __name__ == "__main__":
    build_image_map()

