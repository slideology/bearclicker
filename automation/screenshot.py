import sys
import time
from playwright.sync_api import sync_playwright
from PIL import Image
import os

def take_screenshot(url, out_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Setup viewport to a standard 4:3 ratio for games
        context = browser.new_context(viewport={"width": 1024, "height": 768})
        page = context.new_page()
        print(f"Navigating to {url}")
        try:
            # wait_until="networkidle" can be too strict, use load or domcontentloaded
            page.goto(url, wait_until="load", timeout=30000)
            print("Page loaded. Waiting 5s for game engine to render...")
            time.sleep(5) # wait for preloader to finish sometimes
            
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            page.screenshot(path=out_path)
            print(f"Screenshot saved to {out_path}")
            
            # Now Generate a cropped 4:3 version and a 1:1 version
            img = Image.open(out_path)
            w, h = img.size
            # 1. 4:3 crop (Thumbnail) - usually it's already 1024x768 (4:3)
            # Resize to 512x384
            thumb = img.resize((512, 384), Image.Resampling.LANCZOS)
            thumb_path = out_path.replace(".png", "_thumb.jpg").replace(".jpg", "_thumb.jpg")
            thumb.convert("RGB").save(thumb_path, "JPEG", quality=85)
            print(f"Thumbnail saved to {thumb_path}")
            
            # 2. 1:1 crop (Favicon)
            # Crop the center square
            min_dim = min(w, h)
            left = (w - min_dim) / 2
            top = (h - min_dim) / 2
            right = (w + min_dim) / 2
            bottom = (h + min_dim) / 2
            icon = img.crop((left, top, right, bottom))
            icon = icon.resize((180, 180), Image.Resampling.LANCZOS)
            icon_path = out_path.replace(".png", "_icon.png").replace(".jpg", "_icon.png")
            icon.save(icon_path, "PNG")
            print(f"Favicon saved to {icon_path}")
            
        except Exception as e:
            print(f"Failed to screenshot: {e}")
            return False
        finally:
            browser.close()
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 4:
        # url, slug, images_dir, favicon_dir
        url = sys.argv[1]
        slug = sys.argv[2]
        images_dir = sys.argv[3]
        favicon_dir = sys.argv[4]
        
        out_path = f"/tmp/{slug}_temp.png"
        take_screenshot(url, out_path)
        
        # move files
        import shutil
        import os
        
        thumb_path = out_path.replace(".png", "_thumb.jpg").replace(".jpg", "_thumb.jpg")
        icon_path = out_path.replace(".png", "_icon.png").replace(".jpg", "_icon.png")
        
        if os.path.exists(thumb_path):
            shutil.move(thumb_path, os.path.join(images_dir, f"{slug}.jpg"))
        if os.path.exists(icon_path):
            shutil.move(icon_path, os.path.join(favicon_dir, f"{slug}-favicon.png"))
            shutil.copy(os.path.join(favicon_dir, f"{slug}-favicon.png"), os.path.join(favicon_dir, f"{slug}-apple-touch-icon.png"))
    else:
        print("Usage: python3 screenshot.py <url> <slug> <images_dir> <favicon_dir>")
