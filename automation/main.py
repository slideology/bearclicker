import os
import sys
import logging

# Add parent directory to path to allow absolute imports if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automation.scraper import GameScraper
from automation.ai_optimizer import AIOptimizer
from automation.template_generator import TemplateGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_automation():
    logging.info("Starting Automation Run...")
    
    # 1. Scrape for new games
    scraper = GameScraper()
    new_games = scraper.get_new_games(limit=2) # Fetch up to 2 games per run to manage load
    
    if not new_games:
        logging.info("No new games found to process. Exiting.")
        return

    # 2. Initialize Optimizer and Generator
    optimizer = AIOptimizer()
    generator = TemplateGenerator(base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 3. Process each new game
    for game_data in new_games:
        slug = game_data['slug']
        logging.info(f"Processing new game: {slug}")
        
        # A. AI Optimization
        # Enforces Title < 60 chars, Desc < 160 chars
        optimized_tdk = optimizer.optimize_tdk(game_data)
        faqs_data = optimizer.generate_faqs(game_data)
        
        # B. Generate Template and Assets
        generator.generate_page(game_data, optimized_tdk, faqs_data)
        
        # C. Mark as processed
        scraper.mark_as_processed(slug)
        logging.info(f"Successfully deployed: {slug}")

if __name__ == '__main__':
    run_automation()
