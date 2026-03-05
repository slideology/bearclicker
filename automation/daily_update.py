import os
import sys
import json
import requests
import random
from bs4 import BeautifulSoup
from scraper import GameScraper
from ai_optimizer import AIOptimizer
from template_generator import TemplateGenerator
import logging

# Set up logging to output both to file and standard out
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_latest_games_from_source():
    """从源站获取新游戏列表的 Slug"""
    url = "https://cookie-clicker2.com/new-games"
    new_slugs = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        games = soup.find_all("a", href=True)
        
        for a in games:
            href = a.get("href", "")
            if href.startswith("/") and len(href) > 2 and "games/" not in href and href not in ["/all-games", "/new-games", "/hot-games"]:
                slug = href.strip("/")
                if slug not in new_slugs:
                    new_slugs.append(slug)
    except Exception as e:
        logging.error(f"Failed to fetch new games from source: {e}")
        
    # Exclude typical non-game pages that might appear in new games list
    exclude_list = ['cookie-clicker-game', 'about-us', 'contact-us', 'privacy-policy', 'term-of-use', 'copyright-infringement-notice-procedure']
    return [s for s in new_slugs if s not in exclude_list]

def load_processed_games():
    """读取已生成发布的游戏"""
    games_json_path = os.path.join(".", "static", "game-config", "games.json")
    try:
        with open(games_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [g.get("id") for g in data.get("games", [])]
    except Exception:
        return []

def get_targets_for_today(target_count=3):
    """
    1. 获取新游并比对本地库存，取出"独有新游"
    2. 如果新游不够，从 pending_games_list 取出足够的数量凑齐 3 篇
    """
    processed_slugs = set(load_processed_games())
    source_new_slugs = get_latest_games_from_source()
    
    # 过滤出我们没有的源站新游戏
    truly_new_slugs = [s for s in source_new_slugs if s not in processed_slugs]
    
    selected_targets = []
    
    # 首先加入新游戏
    for slug in truly_new_slugs:
        if len(selected_targets) < target_count:
            selected_targets.append(slug)
            
    logging.info(f"Found {len(selected_targets)} strictly new games.")
            
    # 如果不够 3 个，从 pending 库里面找旧游戏补充
    if len(selected_targets) < target_count:
        needed = target_count - len(selected_targets)
        logging.info(f"Need {needed} more games from pending list to reach target {target_count}.")
        
        pending_path = "pending_games_list.txt"
        if os.path.exists(pending_path):
            with open(pending_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
                
            # 我们通过寻找不重复的有效链接来补位
            # 我们之前验证过它有极多重复数据，并且有闲杂分类页
            added = 0
            remaining_lines = []
            
            for line in lines:
                slug = line.split("/")[-1]
                if slug in ["all-games", "new-games", "hot-games"] or "-games" in slug or slug == "idle":
                    continue # Skip category pages
                    
                if added < needed and slug not in processed_slugs and slug not in selected_targets:
                    selected_targets.append(slug)
                    added += 1
                else:
                    remaining_lines.append(line)
                    
            # 可选：如果取了游戏可以重写回 pending 去掉它
            with open(pending_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(remaining_lines))
                
    return selected_targets

def run_daily_update():
    logging.info("Starting Daily Update Pipeline...")
    
    targets = get_targets_for_today(3)
    
    if not targets:
        logging.info("No more targets available today.")
        return
        
    logging.info(f"Today's confirmed target slugs: {targets}")
    
    scraper = GameScraper()
    optimizer = AIOptimizer()
    generator = TemplateGenerator(base_dir=".")
    
    success_records = []
    failed_records = []
    
    for slug in targets:
        url = f"https://cookie-clicker2.com/{slug}"
        try:
            logging.info(f"--- Processing {url} ---")
            raw_data = scraper.scrape_game_page(url)
            if not raw_data:
                failed_records.append(f"{slug} (Scraping failed)")
                continue
                
            tdk_data = optimizer.optimize_tdk(raw_data)
            faq_data = optimizer.generate_faqs(raw_data)
            
            optimized_data = {}
            optimized_data.update(raw_data)
            optimized_data.update(tdk_data)
            optimized_data["faqs"] = faq_data.get("faqs", [])
            optimized_data["conclusion"] = faq_data.get("conclusion", "")
            
            # Make sure bugged '.com' ending slugs are fixed
            if optimized_data.get("slug", "").endswith(".com"):
                optimized_data["slug"] = optimized_data["slug"][:-4]
            slug_clean = optimized_data["slug"]
            
            success = generator.generate_page(optimized_data, tdk_data, faq_data)
            if success:
                success_records.append({
                    "title": tdk_data.get("title", slug_clean),
                    "slug": slug_clean,
                    "url": f"https://bearclicker.net/{slug_clean}"
                })
                logging.info(f"Successfully generated {slug_clean}")
            else:
                failed_records.append(f"{slug_clean} (Template generation failed)")
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")
            failed_records.append(f"{slug} (Exception: {str(e)})")

    # Final wrap up
    # 1. Push to indexnow
    indexnow_success = False
    if success_records:
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        try:
            import indexnow
            urls_to_submit = [rec["url"] for rec in success_records]
            logging.info(f"Submitting {len(urls_to_submit)} URLs to IndexNow...")
            indexnow_success = indexnow.submit_urls(urls_to_submit)
        except Exception as e:
            logging.error(f"Could not hook into indexnow: {e}")
            
    # 2. Inform Feishu Webhook
    summary = {
        "success_games": success_records,
        "failed_games": failed_records,
        "indexnow_status": indexnow_success
    }
    
    # Use WebhookSender
    try:
        import webhook_sender
        sender = webhook_sender.create_webhook_sender()
        if sender:
            logging.info("Dispatching Feishu Summary Card...")
            sender.send_daily_report("🐻 BearClicker 每日自动更新战报", summary)
        else:
            logging.info("Feishu webhook not configured.")
    except Exception as e:
        logging.error(f"Could not hook into Feishu sender: {e}")

if __name__ == "__main__":
    run_daily_update()
