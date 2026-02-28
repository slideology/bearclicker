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

    def _download_image(self, url, dest_path):
        if not url:
            return False
            
        try:
            response = requests.get(url, stream=True, timeout=10)
            response.raise_for_status()
            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logging.info(f"Downloaded image to {dest_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to download image from {url}: {e}")
            return False

    def generate_page(self, game_data, optimized_tdk, faqs_data):
        slug = game_data['slug']
        logging.info(f"Starting deployment generation for {slug}")
        
        # 1. Download Images
        img_url = game_data.get('image_url')
        favicon_url = game_data.get('favicon_url', img_url)
        
        display_title = slug.replace('-', ' ').title()
        
        if img_url:
            self._download_image(img_url, os.path.join(self.images_dir, f"{slug}.jpg"))
        if favicon_url:
            self._download_image(favicon_url, os.path.join(self.favicon_dir, f"{slug}-favicon.png"))
            self._download_image(favicon_url, os.path.join(self.favicon_dir, f"{slug}-apple-touch-icon.png"))
        
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
        
        if not os.path.exists(html_path):
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"Created template at {html_path}")
        else:
            logging.info(f"Template {html_path} already exists. Skipping HTML generation.")

        # 4. Modify app.py to add route
        self._add_route_to_app(slug)

        # 5. Update games.json
        games_json = os.path.join(self.base_dir, "static", "game-config", "games.json")
        self._update_games_json(games_json, slug, display_title, game_data.get('iframe_src'))
        
        # 6. Update trending_games.html
        trending_html = os.path.join(self.base_dir, "templates", "components", "trending_games.html")
        self._update_trending_games(trending_html, slug, display_title)

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

    <!-- Recommended Videos (using placeholders) -->
    {{% with videos=[
        {{'video_id': 'IYVD4uNfQc4'}},
        {{'video_id': 'HoYN60Cj2BY'}},
        {{'video_id': 'ewRR3ZrcLAA'}},
        {{'video_id': 'MOU2XjPPW90'}}
    ] %}}
    {{% include 'components/trending_videos.html' %}}
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
