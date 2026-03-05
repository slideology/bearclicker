from scraper import GameScraper
from ai_optimizer import AIOptimizer
from template_generator import TemplateGenerator
import traceback
import logging
import sys

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reprocess_all():
    scraper = GameScraper()
    optimizer = AIOptimizer()
    generator = TemplateGenerator(base_dir=".")

    games_to_reprocess = [
        "https://cookie-clicker2.com/among-us-clicker",
    ]

    for url in games_to_reprocess:
        try:
            print(f"\n--- Processing {url} ---")
            raw_data = scraper.scrape_game_page(url)
            if not raw_data:
                continue
                
            tdk_data = optimizer.optimize_tdk(raw_data)
            faq_data = optimizer.generate_faqs(raw_data)
            
            optimized_data = {}
            optimized_data.update(raw_data)
            optimized_data.update(tdk_data)
            optimized_data["faqs"] = faq_data.get("faqs", [])
            optimized_data["conclusion"] = faq_data.get("conclusion", "")
            
            slug = optimized_data.get("slug")
            print(f"Generating Template for {slug}...")
            
            if slug.endswith(".com"):
                optimized_data["slug"] = slug[:-4]
            
            success = generator.generate_page(optimized_data, tdk_data, faq_data)
            if success:
                print(f"Successfully generated {optimized_data['slug']}")
            else:
                print(f"Failed to generate {optimized_data['slug']}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    reprocess_all()
