import os
import json
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TemplateGenerator:
    def __init__(self, base_dir="."):
        self.base_dir = base_dir
        self.templates_dir = os.path.join(base_dir, "templates")
        self.images_dir = os.path.join(base_dir, "static", "images", "games")
        self.favicon_dir = os.path.join(base_dir, "static", "images", "favicon")
        self.data_dir = os.path.join(base_dir, "static", "data")
        self.app_py_path = os.path.join(base_dir, "app.py")
        
        # Ensure all necessary output directories exist
        for d in [self.templates_dir, self.images_dir, self.favicon_dir, self.data_dir]:
            os.makedirs(d, exist_ok=True)

        
        # Load image mapping
        self.image_map = {}
        map_path = os.path.join(self.data_dir, "game_images_map.json")
        try:
            if os.path.exists(map_path):
                with open(map_path, "r", encoding="utf-8") as f:
                    self.image_map = json.load(f)
        except Exception as e:
            logging.error(f"Could not load game_images_map.json: {e}")

    def _process_image_assets(self, source_url, slug):
        if not source_url:
            return False
            
        import tempfile
        from PIL import Image
        
        # Download to temp
        temp_img = os.path.join(tempfile.gettempdir(), f"{slug}_dl.img")
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(source_url, headers=headers, stream=True, timeout=10)
            response.raise_for_status()
            with open(temp_img, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                    
            img = Image.open(temp_img)
            img = img.convert("RGBA")
            bg = Image.new("RGBA", img.size, (255,255,255,255))
            img = Image.alpha_composite(bg, img).convert("RGB")
            
            w, h = img.size
            
            # 1. 512x384 (4:3) Thumbnail
            # Crop to 4:3 first
            target_w, target_h = w, int(w * 0.75)
            if target_h > h:
                target_h = h
                target_w = int(h * 1.3333333333333333)
            left = (w - target_w) / 2
            top = (h - target_h) / 2
            right = (w + target_w) / 2
            bottom = (h + target_h) / 2
            
            thumb = img.crop((left, top, right, bottom))
            thumb = thumb.resize((512, 384), Image.Resampling.LANCZOS)
            thumb.save(os.path.join(self.images_dir, f"{slug}.jpg"), "JPEG", quality=85)
            
            # 2. 180x180 (1:1) icon
            min_dim = min(w, h)
            left = (w - min_dim) / 2
            top = (h - min_dim) / 2
            right = (w + min_dim) / 2
            bottom = (h + min_dim) / 2
            
            icon = img.crop((left, top, right, bottom))
            icon = icon.resize((180, 180), Image.Resampling.LANCZOS)
            icon_path = os.path.join(self.favicon_dir, f"{slug}-favicon.png")
            icon.save(icon_path, "PNG")
            
            import shutil
            shutil.copy(icon_path, os.path.join(self.favicon_dir, f"{slug}-apple-touch-icon.png"))
            
            logging.info(f"Successfully downloaded and cropped images for {slug} based on library source")
            return True
        except Exception as e:
            logging.error(f"Failed to process image assets for {slug}: {e}")
            return False
        finally:
            if os.path.exists(temp_img):
                os.remove(temp_img)

    def generate_page(self, game_data, optimized_tdk, faqs_data):
        slug = game_data['slug']
        logging.info(f"Starting deployment generation for {slug}")
        
        display_title = slug.replace('-', ' ').title()
        
        # Determine raw image source preferring the site scraped image map
        img_source = self.image_map.get(slug)
        if not img_source:
             img_source = game_data.get('image_url')
             
        # Generate thumbnail and favicons
        self._process_image_assets(img_source, slug)
        
        # 2. Update FAQs JSON
        faqs_path = os.path.join(self.data_dir, "faqs.json")
        try:
            with open(faqs_path, 'r', encoding='utf-8') as f:
                all_faqs = json.load(f)
        except Exception:
            all_faqs = {}
            
        all_faqs[slug] = faqs_data
        
        with open(faqs_path, 'w', encoding='utf-8') as f:
            json.dump(all_faqs, f, indent=2, ensure_ascii=False)
            logging.info(f"Updated faqs.json with data for {slug}")

        # 3. Generate HTML Template
        html_content = self._create_html_content(slug, optimized_tdk)
        html_path = os.path.join(self.templates_dir, f"{slug}.html")
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"Generated template at {html_path}")

        # 4. Modify app.py to add route
        self._add_route_to_app(slug)

        # 5. Update games.json
        games_json = os.path.join(self.base_dir, "static", "game-config", "games.json")
        self._update_games_json(games_json, slug, display_title, game_data.get('iframe_src'))
        
        # 6. Update trending_games.html
        trending_html = os.path.join(self.base_dir, "templates", "components", "trending_games.html")
        self._update_trending_games(trending_html, slug, display_title)
        
        # 7. Update sitemap.xml
        sitemap_path = os.path.join(self.base_dir, "static", "sitemap.xml")
        self._update_sitemap(sitemap_path, slug)
        
        return True

    def _create_html_content(self, slug, tdk):
        title = tdk.get('title', '').replace('"', '&quot;')
        desc = tdk.get('description', '').replace('"', '&quot;')
        
        # We try to infer a good title component for the hero layout
        display_title = slug.replace('-', ' ').title()
        
        template = f"""{{% extends "base.html" %}}

{{% block title %}}{title}{{% endblock %}}

{{% block meta_description %}}
<meta name="description" content="{desc}">
{{% endblock %}}

{{% block og_title %}}{title}{{% endblock %}}
{{% block og_description %}}{desc}{{% endblock %}}

{{% block og_image %}}https://bearclicker.net/static/images/games/{slug}.jpg{{% endblock %}}

{{% block favicon %}}
<link rel="icon" type="image/png" href="{{{{ url_for('static', filename='images/favicon/{slug}-favicon.png') }}}}">
<link rel="apple-touch-icon" sizes="180x180" href="{{{{ url_for('static', filename='images/favicon/{slug}-apple-touch-icon.png') }}}}">
{{% endblock %}}

{{% block content %}}
<div class="relative overflow-hidden">
    {{% with 
        gradient_colors="from-pink-400 via-purple-500 to-indigo-600",
        blob_gradient_1="from-pink-500 to-purple-500",
        blob_gradient_2="from-purple-500 to-indigo-500",
        title_gradient="from-pink-500 via-purple-500 to-indigo-500",
        game_url="/game/{slug}",
        title="{display_title}",
        description="{desc}",
        open_in_new_tab=False
    %}}
        {{% include 'components/hero.html' %}}
    {{% endwith %}}


    <!-- Trending Games Section -->
    {{% with current_page='{slug}' %}}
    {{% include 'components/trending_games.html' %}}
    {{% endwith %}}
    
    <!-- FAQ Section -->
    {{% include 'components/faq_section.html' %}}
</div>
{{% endblock %}}
"""
        return template

    def _add_route_to_app(self, slug):
        # Create a safe python function name
        function_name = slug.replace('-', '_').replace('.', '_')
        if function_name[0].isdigit():
            function_name = f"game_{function_name}"
            
        # Check if route already exists
        with open(self.app_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if f"def {function_name}()" in content or f"/{slug}'" in content or f'/{slug}"' in content:
                logging.info(f"Route for {slug} seems to already exist in app.py. Skipping injection.")
                return

        # Prepare snippet
        route_snippet = f"""
@app.route('/{slug}')
def {function_name}():
    faq_data = get_faqs_for_page('{slug}')
    return render_template('{slug}.html',
                         page_title='{slug.replace('-', ' ').title()}',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())
"""
        # Append to the end of app.py to avoid complex parsing problems, ensuring it's above any if __name__ == '__main__': if needed.
        # This is a basic injection hook. In real-world projects we might look for a specific marker.
        logging.info(f"Injecting route {function_name} into {self.app_py_path}")
        
        lines = content.split('\n')
        # find where to insert: preferably right before if __name__ == "__main__": or at the end
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.strip().startswith("if __name__ =="):
                insert_idx = i
                break
                
        lines.insert(insert_idx, route_snippet)
        
        with open(self.app_py_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

    def _update_games_json(self, path, slug, title, url):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # check if exists
            if any(g.get('id') == slug for g in data.get('games', [])):
                return
            
            new_game = {
                "id": slug,
                "title": title,
                "url": url if url else f"/{slug}.embed"
            }
            # Add to the beginning so it shows up first
            data.setdefault('games', []).insert(0, new_game)
            
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logging.info(f"Added {slug} to games.json")
        except Exception as e:
            logging.error(f"Failed to update games.json: {e}")

    def _update_trending_games(self, path, slug, title):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            content = "".join(lines)
            if f"/{slug}" in content:
                return # Already exists
                
            components = f"""            <!-- {title} Card -->
            <a href="https://bearclicker.net/{slug}" class="group relative rounded-lg overflow-hidden shadow-lg transition-transform duration-300 hover:transform hover:scale-105 flex flex-col">
                <div class="relative">
                    <img src="{{{{ url_for('static', filename='images/games/{slug}.jpg') }}}}" 
                         alt="{title} img" loading="lazy" class="w-full aspect-[4/3] object-cover">
                    <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                </div>
                <div class="p-2 bg-gray-100 dark:bg-gray-800">
                    <p class="text-xs sm:text-sm font-medium text-gray-800 dark:text-gray-200 truncate text-center">
                        {{{{ translations.get('trending', {{}}).get('{slug.replace('-', '_')}', '{title}') }}}}
                    </p>
                </div>
            </a>
"""
            # Insert right after the grid container div to be the absolute first item
            insert_idx = -1
            for i, line in enumerate(lines):
                if 'class="grid' in line and 'grid-cols-2' in line:
                    insert_idx = i
                    break
                    
            if insert_idx != -1:
                lines.insert(insert_idx + 1, components)
                with open(path, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                logging.info(f"Added {slug} to trending_games.html")
        except Exception as e:
            logging.error(f"Failed to update trending_games.html: {e}")

    def _update_sitemap(self, path, slug):
        """将新游戏的 URL 追加到 sitemap.xml 中（如尚未存在）"""
        try:
            from datetime import date
            today = date.today().isoformat()
            new_url = f"https://bearclicker.net/{slug}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Skip if already in sitemap
            if new_url in content:
                logging.info(f"{slug} already exists in sitemap.xml, skipping.")
                return
                
            # Build new url block
            new_entry = f"""    <url>
        <loc>{new_url}</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
"""
            # Insert before closing </urlset> tag
            updated = content.replace("</urlset>", new_entry + "</urlset>")
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(updated)
                
            logging.info(f"Added {slug} to sitemap.xml with date {today}")
            
            # Ping Google to notify of sitemap update
            try:
                ping_url = "https://www.google.com/ping?sitemap=https://bearclicker.net/sitemap.xml"
                requests.get(ping_url, timeout=5)
                logging.info("Pinged Google to re-crawl sitemap.xml")
            except Exception:
                pass  # Non-fatal, don't raise
        except Exception as e:
            logging.error(f"Failed to update sitemap.xml: {e}")
