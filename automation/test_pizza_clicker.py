import sys
import os
import json
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from automation.scraper import GameScraper
from automation.ai_optimizer import AIOptimizer
from automation.template_generator import TemplateGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_single_url(url):
    scraper = GameScraper()
    logging.info(f"Manually scraping target: {url}")
    game_data = scraper.scrape_game_page(url)
    
    if not game_data:
        logging.error("Failed to scrape target.")
        return
        
    optimizer = AIOptimizer()
    generator = TemplateGenerator(base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    optimized_tdk = optimizer.optimize_tdk(game_data)
    faqs_data = optimizer.generate_faqs(game_data)
    
    generator.generate_page(game_data, optimized_tdk, faqs_data)
    logging.info(f"Done processing {url}")

if __name__ == "__main__":
    test_single_url("https://cookie-clicker2.com/pizza-clicker")
