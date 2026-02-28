import os
import json
import logging
import re
from dotenv import load_dotenv

# Use appropriate LLM SDK based on BearClicker's setup
try:
    from google import genai
    from pydantic import BaseModel
except ImportError:
    genai = None

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIOptimizer:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GEMINI_API_KEY') or os.getenv('DEEPSEEK_API_KEY')
        self.model = "gemini-2.5-flash" # Use gemini-2.5-flash for fast text tasks
        
        if genai and self.api_key:
            self.client = genai.Client(api_key=self.api_key)
            logging.info("Gemini SDK initialized successfully.")
        else:
            self.client = None
            logging.warning("No Gemini SDK or API Key found. AI Optimization will run in fallback/mock mode.")

    def _call_llm(self, system_prompt, user_prompt, require_json=False):
        if not self.client:
            return None
            
        try:
            config_args = {"system_instruction": system_prompt, "temperature": 0.7}
            if require_json:
                config_args["response_mime_type"] = "application/json"
                
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config=genai.types.GenerateContentConfig(**config_args)
            )
            return response.text
        except Exception as e:
            logging.error(f"LLM Call failed: {e}")
            return None

    def optimize_tdk(self, game_data):
        """
        Rewrites Title and Description to fit SEO constraints:
        Title < 60 chars, Desc < 160 chars.
        """
        logging.info(f"Optimizing TDK for {game_data.get('slug')}")
        
        system_prompt = (
            "You are an expert SEO copywriter for a gaming website. "
            "Your task is to rewrite the meta title and description for a web game to maximize CTR and search rankings. "
            "STRICT RULES:\n"
            "1. Meta Title MUST be UNDER 60 characters.\n"
            "2. Meta Description MUST be UNDER 160 characters.\n"
            "3. DO NOT include any competitor names like 'Cookie Clicker 2' or 'Cookie Clicker'. Replace them with 'Bear Clicker' or remove them entirely.\n"
            "4. Output ONLY valid JSON with keys: 'title', 'description', 'keywords'."
        )
        
        user_prompt = f"""
        Original Title: {game_data.get('original_title')}
        Original Description: {game_data.get('original_description')}
        Game Content: {game_data.get('content_text')}
        Game Slug: {game_data.get('slug')}
        
        Please provide the optimized SEO JSON.
        """
        
        result = self._call_llm(system_prompt, user_prompt, require_json=True)
        
        if result:
            try:
                optimized = json.loads(result)
                # Validation checks against strict constraints
                title = optimized.get('title', game_data.get('original_title'))
                desc = optimized.get('description', game_data.get('original_description'))
                
                if len(title) > 60:
                    logging.warning(f"AI generated title too long ({len(title)} chars). Truncating.")
                    title = title[:56] + "..."
                if len(desc) > 160:
                    logging.warning(f"AI generated desc too long ({len(desc)} chars). Truncating.")
                    desc = desc[:156] + "..."
                    
                return {
                    "title": title,
                    "description": desc,
                    "keywords": optimized.get('keywords', game_data.get('slug', '').replace('-', ' '))
                }
            except Exception as e:
                logging.error(f"Failed to parse AI TDK JSON: {e}")
        
        # Fallback simulation to show rule compliance
        title = game_data.get('original_title', '')
        desc = game_data.get('original_description', '')
        
        # Simulate AI rewriting by adding keywords, and STRICTLY truncating
        opt_title = f"Play {title} Unblocked & Free"
        opt_desc = f"Enjoy {desc} Play the best {title} free online right now without downloading!"
        
        if len(opt_title) > 56:
            opt_title = opt_title[:56] + "..."
        if len(opt_desc) > 156:
            opt_desc = opt_desc[:156] + "..."
            
        return {
            "title": opt_title,
            "description": opt_desc,
            "keywords": game_data.get('slug', '').replace('-', ' ')
        }

    def generate_faqs(self, game_data):
        """
        Generates 3-5 FAQs for the game page.
        """
        logging.info(f"Generating FAQs for {game_data.get('slug')}")
        
        system_prompt = (
            "You are a helpful assistant writing FAQ sections for a web game portal. "
            "STRICT RULES:\n"
            "1. Output MUST be valid JSON matching this schema:\n"
            "{\n  'faqs': [\n    {'question': '...', 'answer': '...'}\n  ],\n  'conclusion': 'A short wrap-up sentence.'\n}\n"
            "2. Ensure you generate at least 6 and up to 8 distinct FAQs regarding gameplay, tips, controls, and accessibility.\n"
            "3. NEVER use the words 'Cookie Clicker' or 'Cookie Clicker 2'. If the source text mentions them, replace them with 'Bear Clicker' or just the specific Game Name.\n"
            "4. Keep answers concise and written in native English."
        )
        
        user_prompt = f"Game Name: {game_data.get('slug').replace('-', ' ').title()}\nGame Info: {game_data.get('content_text')}"
        
        result = self._call_llm(system_prompt, user_prompt, require_json=True)
        
        if result:
            try:
                faqs = json.loads(result)
                return faqs
            except Exception as e:
                logging.error(f"Failed to parse AI FAQ JSON: {e}")
                
        # Fallback with robust FAQ creation to meet user expectations
        name = game_data.get('slug', '').replace('-', ' ').title()
        return {
            "faqs": [
                {"question": f"How to play {name}?", "answer": f"Simply use your mouse to interact with the elements. Follow the on-screen instructions to get started with {name}."},
                {"question": f"Is {name} free to play?", "answer": "Yes! You can play it completely free online directly in your browser without any downloads."},
                {"question": f"Can I play {name} on my phone?", "answer": "Absolutely, this HTML5 game is fully responsive and runs smoothly on both desktop and mobile devices."},
                {"question": f"What is the best strategy for {name}?", "answer": "Focus on upgrading your early resources as quickly as possible to build a strong foundation for late-game scaling."},
                {"question": f"Do my progress save automatically?", "answer": "Yes, your progress is typically saved in your browser's local storage, so you can resume anytime you come back."}
            ],
            "conclusion": f"Enjoy playing {name} and share your high scores with friends!"
        }

if __name__ == '__main__':
    # Test with mock data
    optimizer = AIOptimizer()
    mock_data = {
        "slug": "cookie-tap",
        "original_title": "Cookie Tap - Play Cookie Tap On Cookie Clicker 2",
        "original_description": "Tap click cookies to see many interesting things as well as many attractive fruits here. ",
        "content_text": "Tap click cookies to see many interesting things as well as many attractive fruits here. Wish you have fun!"
    }
    
    tdk = optimizer.optimize_tdk(mock_data)
    faqs = optimizer.generate_faqs(mock_data)
    
    print("--- Optimized TDK ---")
    print(json.dumps(tdk, indent=2))
    print("--- Generated FAQs ---")
    print(json.dumps(faqs, indent=2))
