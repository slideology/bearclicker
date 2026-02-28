import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import urllib.parse
import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GameScraper:
    def __init__(self, sitemap_url="https://cookie-clicker2.com/sitemap.xml", processed_log="automation/processed_games.json"):
        self.sitemap_url = sitemap_url
        self.processed_log = processed_log
        self.processed_games = self._load_processed_games()

    def _load_processed_games(self):
        if os.path.exists(self.processed_log):
            try:
                with open(self.processed_log, 'r', encoding='utf-8') as f:
                    return set(json.load(f))
            except json.JSONDecodeError:
                return set()
        return set()

    def _save_processed_game(self, slug):
        self.processed_games.add(slug)
        # Ensure dir exists
        os.makedirs(os.path.dirname(self.processed_log), exist_ok=True)
        with open(self.processed_log, 'w', encoding='utf-8') as f:
            json.dump(list(self.processed_games), f, indent=2)

    def fetch_sitemap_urls(self):
        """Fetch all URLs from the sitemap"""
        logging.info(f"Fetching sitemap from {self.sitemap_url}")
        try:
            response = requests.get(self.sitemap_url, timeout=10)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            # Handle XML namespace
            namespace = ""
            if "}" in root.tag:
                namespace = root.tag.split("}")[0] + "}"
            
            urls = []
            for url_elem in root.findall(f"{namespace}url"):
                loc = url_elem.find(f"{namespace}loc")
                if loc is not None and loc.text:
                    urls.append(loc.text.strip())
            
            logging.info(f"Found {len(urls)} URLs in sitemap")
            return urls
        except Exception as e:
            logging.error(f"Failed to fetch or parse sitemap: {e}")
            return []

    def scrape_game_page(self, url):
        """Extract metadata, iframe, and images from a single game page."""
        logging.info(f"Scraping {url}...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {}
            data['url'] = url
            
            # TDK
            data['original_title'] = soup.title.string if soup.title else ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            data['original_description'] = meta_desc['content'] if meta_desc else ""
            
            # Canonical URL / Slug
            canonical = soup.find('link', rel='canonical')
            data['canonical'] = canonical['href'] if canonical else url
            data['slug'] = data['canonical'].rstrip('/').split('/')[-1]
            
            # Iframe URL (Game Source)
            iframe = soup.find('iframe')
            base_iframe_src = iframe['src'] if iframe and iframe.has_attr('src') else ""
            
            # Make iframe src absolute if it's relative
            if base_iframe_src.startswith('/'):
                parsed_url = urllib.parse.urlparse(url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                data['iframe_src'] = urllib.parse.urljoin(base_url, base_iframe_src)
            else:
                data['iframe_src'] = base_iframe_src
            
            # OG Image
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image['content']:
                img_url = og_image['content']
                if not img_url.startswith('http'):
                    parsed_url = urllib.parse.urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    img_url = urllib.parse.urljoin(base_url, img_url)
                data['image_url'] = img_url
            else:
                data['image_url'] = ""

            # Favicon
            favicon = soup.find('link', rel=lambda x: x and 'icon' in x)
            if favicon and favicon['href']:
                fav_url = favicon['href']
                if not fav_url.startswith('http'):
                    parsed_url = urllib.parse.urlparse(url)
                    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                    fav_url = urllib.parse.urljoin(base_url, fav_url)
                data['favicon_url'] = fav_url
            else:
                data['favicon_url'] = data['image_url'] # fallback to og:image if no icon
                
            # Content Text for AI
            description_div = soup.find('div', id='description')
            if description_div:
                data['content_text'] = description_div.get_text(separator=' ', strip=True)
            else:
                paras = soup.find_all('p')
                data['content_text'] = ' '.join([p.get_text(strip=True) for p in paras[:5]])
                
            logging.info(f"Successfully scraped metadata for {data['slug']}")
            return data
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {e}")
            return None

    def get_new_games(self, limit=1):
        """Finds games from sitemap that haven't been processed yet."""
        urls = self.fetch_sitemap_urls()
        
        new_games_data = []
        for url in urls:
            # Skip root domain or weird routes
            if url.count('/') <= 3 and (url.endswith('com') or url.endswith('com/')):
                continue
            
            slug = url.rstrip('/').split('/')[-1]
            if slug not in self.processed_games:
                # Basic filter to ensure we aren't hitting categories
                if any(x in url for x in ['category', 'tag', 'about-us', 'contact-us', 'privacy-policy', '-policy']):
                    continue
                if '.' in slug: # To prevent pulling domain names or broken routes
                    continue
                    
                game_data = self.scrape_game_page(url)
                if game_data and game_data['iframe_src']: # Ensure it's actually a playable game
                    new_games_data.append(game_data)
                    logging.info(f"Found new valid game: {slug}")
                    
                    if len(new_games_data) >= limit:
                        break
        
        return new_games_data

    def mark_as_processed(self, slug):
        self._save_processed_game(slug)

if __name__ == '__main__':
    scraper = GameScraper()
    new_games = scraper.get_new_games(limit=1)
    if new_games:
        print(json.dumps(new_games[0], indent=2, ensure_ascii=False))
    else:
        print("No new games found.")
