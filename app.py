from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, session, g
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'bearclicker-secret-key-2024')

# 导入日志配置
from config.logging_config import setup_logging

# 设置日志系统
setup_logging(app)

def get_translations():
    """Get translations dictionary."""
    try:
        translations_path = os.path.join(app.static_folder, 'data', 'translations.json')
        with open(translations_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
            return translations.get('en', {})
    except Exception as e:
        app.logger.error(f"Error getting translations: {e}")
        return {
            'nav': {
                'home': 'Home',
                'guide': 'Game Guide',
                'faq': 'FAQ',
                'play': 'Play',
                'about': 'About',
                'contact': 'Contact',
                'games': 'Games'
            },
            "hero": {
                "title_highlight": "Create Music",
                "title_regular": "Like Never Before",
                "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
            },
            "game": {
                "title": "Bear Clicker",
                "subtitle": "The Ultimate Bear Clicker Game",
                "description": "Unleash haunting melodies with our special glitch music system. Stack sounds, witness their digital distortion transformation. Embrace Horror Aesthetics."
            },
            "trending": {
                "title": "Trending Games",
                "bear_lily": "Bear - Lily",
                "bear_megalovania": "Bear - Megalovania",
                "bear_spruted": "Bear - Spruted"
            }
        }

def load_faqs():
    """
    从JSON文件加载FAQ数据
    
    Returns:
        dict: FAQ数据字典
    """
    try:
        faqs_path = os.path.join(app.static_folder, 'data', 'faqs.json')
        
        with open(faqs_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading FAQs: {e}")
        # 返回空字典作为默认值
        return {}

def get_faqs_for_page(page_name):
    """
    获取特定页面的FAQ数据
    
    Args:
        page_name (str): 页面名称
        
    Returns:
        dict: 包含FAQ问答和结论的字典
    """
    faqs_data = load_faqs()
    
    # 如果找不到对应页面的FAQ，返回默认值
    if page_name not in faqs_data:
        return {
            'faqs': [],
            'conclusion': ''
        }
    
    return faqs_data[page_name]

@app.route('/')
def home():
    translations_data = get_translations()
    faq_data = get_faqs_for_page('index')  
    return render_template('index.html',
                         page_title='Bear Clicker',
                         title='Bear Clicker - Interactive Music Experience',
                         description='Create amazing music with Bear Clicker! Mix beats, compose tunes, and share your musical creations.',
                         translations=translations_data,
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'])

@app.route('/about')
def about():
    try:
        trans = get_translations()
        return render_template('about.html', 
                         title='About Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in about route: {e}")
        return render_template('about.html',
                         title='About Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/game')
def game():
    try:
        trans = get_translations()
        return render_template('game.html',
                         title='Play Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in game route: {e}")
        return render_template('game.html',
                         title='Play Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/introduction')
def introduction():
    try:
        trans = get_translations()
        return render_template('introduction.html',
                         title='Game Guide - Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in introduction route: {e}")
        return render_template('introduction.html',
                         title='Game Guide - Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        trans = get_translations()
        if request.method == 'POST':
            return send_message()
        return render_template('contact.html',
                         title='Contact Bear Clicker',
                         translations=trans)
    except Exception as e:
        app.logger.error(f"Error in contact route: {e}")
        return render_template('contact.html',
                         title='Contact Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         })

@app.route('/faq')
def faq():
    try:
        trans = get_translations()
        faq_data = get_faqs_for_page('index')  # 使用index页面的FAQ数据
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         page_title='Bear Clicker',
                         translations=trans,
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'])
    except Exception as e:
        app.logger.error(f"Error in faq route: {e}")
        return render_template('faq.html',
                         title='FAQ - Bear Clicker',
                         page_title='Bear Clicker',
                         translations={
                             "nav": {"home": "Home", "faq": "FAQ"},
                             "hero": {
                                 "title_highlight": "Create Music",
                                 "title_regular": "Like Never Before",
                                 "description": "Transform your musical ideas into reality with Bear Clicker. Mix beats, create melodies, and share your music with the world."
                             }
                         },
                         dynamic_faqs=[],
                         conclusion="No FAQ data available at this time.")

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')
@app.route('/79b10f40ab4848b5a84b4d154927ed13.txt')
def indexnow():
    return send_from_directory('static', '79b10f40ab4848b5a84b4d154927ed13.txt')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt')

@app.route('/capybara-clicker')
def capybara_clicker():
    faq_data = get_faqs_for_page('capybara-clicker')
    return render_template('capybara-clicker.html',
                         page_title='Capybara Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/stimulation-clicker')
def stimulation_clicker():
    faq_data = get_faqs_for_page('stimulation-clicker')
    return render_template('stimulation-clicker.html',
                         page_title='Stimulation Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 
@app.route('/unchill-guy-clicker')
def unchill_guy_clicker():
    faq_data = get_faqs_for_page('unchill-guy-clicker')
    return render_template('unchill-guy-clicker.html',
                         page_title='Unchill Guy Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 
@app.route('/the-ultimate-clicker-squad')
def the_ultimate_clicker_squad():
    faq_data = get_faqs_for_page('the-ultimate-clicker-squad')
    return render_template('the-ultimate-clicker-squad.html',
                         page_title='The Ultimate Clicker Squad',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 

@app.route('/chill-girl-clicker')
def chill_girl_clicker():
    faq_data = get_faqs_for_page('chill-girl-clicker')
    return render_template('chill-girl-clicker.html',
                         page_title='Chill Girl Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations()) 

@app.route('/bitcoin-clicker')
def bitcoin_clicker():
    faq_data = get_faqs_for_page('bitcoin-clicker')
    return render_template('bitcoin-clicker.html',
                         page_title='Bitcoin Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/business-clicker')
def business_clicker():
    faq_data = get_faqs_for_page('business-clicker')
    return render_template('business-clicker.html',
                         page_title='Business Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/bombardino-crocodilo-clicker')
def bombardino_crocodilo_clicker():
    faq_data = get_faqs_for_page('bombardino-crocodilo-clicker')
    return render_template('bombardino-crocodilo-clicker.html',
                         page_title='Bombardino Crocodilo Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/golf-hit')
def golf_hit():
    faq_data = get_faqs_for_page('golf-hit')
    return render_template('golf-hit.html',
                         page_title='Golf Hit',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/capybara-clicker-2')
def capybara_clicker_2():
    faq_data = get_faqs_for_page('capybara-clicker-2')
    return render_template('capybara-clicker-2.html',
                         page_title='Capybara Clicker 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/terradome')
def terradome():
    faq_data = get_faqs_for_page('terradome')
    return render_template('terradome.html',
                         page_title='Terradome',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/white-horizon')
def white_horizon():
    faq_data = get_faqs_for_page('white-horizon')
    return render_template('white-horizon.html',
                         page_title='White Horizon',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/chill-guy-clicker-3d')
def chill_guy_clicker_3d():
    faq_data = get_faqs_for_page('chill-guy-clicker-3d')
    return render_template('chill-guy-clicker-3d.html',
                         page_title='Chill Guy Clicker 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/banana-clicker')
def banana_clicker():
    faq_data = get_faqs_for_page('banana-clicker')
    return render_template('banana-clicker.html',
                         page_title='Banana Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())  
@app.route('/red-rush')
def red_rush():
    faq_data = get_faqs_for_page('red-rush')
    return render_template('red-rush.html',
                         page_title='Red Rush',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/scrandle')
def scrandle():
    faq_data = get_faqs_for_page('scrandle')
    return render_template('scrandle.html',
                         page_title='Scrandle',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/poop-clicker-2')
def poop_clicker_2():
    faq_data = get_faqs_for_page('poop-clicker-2')
    return render_template('poop-clicker-2.html',
                         page_title='Poop Clicker 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/banana-clicker-unblocked')
def banana_clicker_unblocked():
    faq_data = get_faqs_for_page('banana-clicker-unblocked')
    return render_template('banana-clicker-unblocked.html',
                         page_title='Banana Clicker Unblocked',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/chill-clicker')
def chill_clicker():
    faq_data = get_faqs_for_page('chill-clicker')
    return render_template('chill-clicker.html',
                         page_title='Chill Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     

@app.route('/clock-clicker')
def clock_clicker():
    faq_data = get_faqs_for_page('clock-clicker')
    return render_template('clock-clicker.html',
                         page_title='Clock Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cat-clicker')
def cat_clicker():
    faq_data = get_faqs_for_page('cat-clicker')
    return render_template('cat-clicker.html',
                         page_title='Cat Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/muscle-clicker-2')
def muscle_clicker_2():
    faq_data = get_faqs_for_page('muscle-clicker-2')
    return render_template('muscle-clicker-2.html',
                         page_title='Muscle Clicker 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/big-dig-treasure-clickers')
def big_dig_treasure_clickers():
    faq_data = get_faqs_for_page('big-dig-treasure-clickers')
    return render_template('big-dig-treasure-clickers.html',
                         page_title='Big Dig Treasure Clickers',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/ice-cream-clicker')
def ice_cream_clicker():
    faq_data = get_faqs_for_page('ice-cream-clicker')
    return render_template('ice-cream-clicker.html',
                         page_title='Ice Cream Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/whopper-clicker')
def whopper_clicker():
    faq_data = get_faqs_for_page('whopper-clicker')
    return render_template('whopper-clicker.html',
                         page_title='Whopper Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/chicken-jockey-clicker')
def chicken_jockey_clicker():
    faq_data = get_faqs_for_page('chicken-jockey-clicker')
    return render_template('chicken-jockey-clicker.html',
                         page_title='Chicken Jockey Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/duck-duck-clicker-3d')
def duck_duck_clicker_3d():
    faq_data = get_faqs_for_page('duck-duck-clicker-3d')
    return render_template('duck-duck-clicker-3d.html',
                         page_title='Duck Duck Clicker 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cat-clicker-mlg')
def cat_clicker_mlg():
    faq_data = get_faqs_for_page('cat-clicker-mlg')
    return render_template('cat-clicker-mlg.html',
                         page_title='Cat Clicker MLG',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-idle-clicker')
def sprunki_idle_clicker():
    faq_data = get_faqs_for_page('sprunki-idle-clicker')
    return render_template('sprunki-idle-clicker.html',
                         page_title='Sprunki Idle Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())


@app.route('/loot-heroes-clicker')
def loot_heroes_clicker():
    faq_data = get_faqs_for_page('loot-heroes-clicker')
    return render_template('loot-heroes-clicker.html',
                         page_title='Loot Heroes Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/my-cupcake-clicker')
def my_cupcake_clicker():
    faq_data = get_faqs_for_page('my-cupcake-clicker')
    return render_template('my-cupcake-clicker.html',
                         page_title='My Cupcake Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/noob-basketball-clicker')
def noob_basketball_clicker():
    faq_data = get_faqs_for_page('noob-basketball-clicker')
    return render_template('noob-basketball-clicker.html',
                         page_title='Noob Basketball Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-4')
def cookie_clicker_4():
    faq_data = get_faqs_for_page('cookie-clicker-4')
    return render_template('cookie-clicker-4.html',
                         page_title='Cookie Clicker 4',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-5')
def cookie_clicker_5():
    faq_data = get_faqs_for_page('cookie-clicker-5')
    return render_template('cookie-clicker-5.html',
                         page_title='Cookie Clicker 5',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-3')
def cookie_clicker_3():
    faq_data = get_faqs_for_page('cookie-clicker-3')
    return render_template('cookie-clicker-3.html',
                         page_title='Cookie Clicker 3',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cheese-chompers-3d')
def cheese_chompers_3d():
    faq_data = get_faqs_for_page('cheese-chompers-3d')
    return render_template('cheese-chompers-3d.html',
                         page_title='Cheese Chompers 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/crazy-cattle-3d')
def crazy_cattle_3d():
    faq_data = get_faqs_for_page('crazy-cattle-3d')
    return render_template('crazy-cattle-3d.html',
                         page_title='Crazy Cattle 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/crazy-kitty-3d')
def crazy_kitty_3d():
    faq_data = get_faqs_for_page('crazy-kitty-3d')
    return render_template('crazy-kitty-3d.html',
                         page_title='Crazy Kitty 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/tung-tung-sahur-gta-miami')
def tung_tung_sahur_gta_miami():
    faq_data = get_faqs_for_page('tung-tung-sahur-gta-miami')
    return render_template('tung-tung-sahur-gta-miami.html',
                         page_title='Tung Tung Sahur: GTA Miami',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/doge-miner')
def doge_miner():
    faq_data = get_faqs_for_page('doge-miner')
    return render_template('doge-miner.html',
                         page_title='Doge Miner',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/doge-miner-2')
def doge_miner_2():
    faq_data = get_faqs_for_page('doge-miner-2')
    return render_template('doge-miner-2.html',
                         page_title='Doge Miner 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-evolution')
def cookie_clicker_evolution():
    faq_data = get_faqs_for_page('cookie-clicker-evolution')
    return render_template('cookie-clicker-evolution.html',
                         page_title='Cookie Clicker Evolution',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-city')
def cookie_clicker_city():
    faq_data = get_faqs_for_page('cookie-clicker-city')
    return render_template('cookie-clicker-city.html',
                         page_title='Cookie Clicker City',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/doggo-clicker')
def doggo_clicker():
    faq_data = get_faqs_for_page('doggo-clicker')
    return render_template('doggo-clicker.html',
                         page_title='Doggo Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/monster-clicker')
def monster_clicker():
    faq_data = get_faqs_for_page('monster-clicker')
    return render_template('monster-clicker.html',
                         page_title='Monster Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/panda-clicker')
def panda_clicker():
    faq_data = get_faqs_for_page('panda-clicker')
    return render_template('panda-clicker.html',
                         page_title='Panda Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/capybara-evolution-clicker')
def capybara_evolution_clicker():
    faq_data = get_faqs_for_page('capybara-evolution-clicker')
    return render_template('capybara-evolution-clicker.html',
                         page_title='Capybara Evolution Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/particle-clicker')
def particle_clicker():
    faq_data = get_faqs_for_page('particle-clicker')
    return render_template('particle-clicker.html',
                         page_title='Particle Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/duck-duck-clicker')
def duck_duck_clicker():
    faq_data = get_faqs_for_page('duck-duck-clicker')
    return render_template('duck-duck-clicker.html',
                         page_title='Duck Duck Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/duck-clicker')
def duck_clicker():
    faq_data = get_faqs_for_page('duck-clicker')
    return render_template('duck-clicker.html',
                         page_title='Duck Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/capybara-clicker-pro')
def capybara_clicker_pro():
    faq_data = get_faqs_for_page('capybara-clicker-pro')
    return render_template('capybara-clicker-pro.html',
                         page_title='Capybara Clicker Pro',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/clicker-heroes')
def clicker_heroes():
    faq_data = get_faqs_for_page('clicker-heroes')
    return render_template('clicker-heroes.html',
                         page_title='Clicker Heroes',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/crusher-clicker')
def crusher_clicker():
    faq_data = get_faqs_for_page('crusher-clicker')
    return render_template('crusher-clicker.html',
                         page_title='Crusher Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/minetap-merge-clicker')
def minetap_merge_clicker():
    faq_data = get_faqs_for_page('minetap-merge-clicker')
    return render_template('minetap-merge-clicker.html',
                         page_title='MineTap Merge Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/little-farm-clicker')
def little_farm_clicker():
    faq_data = get_faqs_for_page('little-farm-clicker')
    return render_template('little-farm-clicker.html',
                         page_title='Little Farm Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/smash-car-clicker')
def smash_car_clicker():
    faq_data = get_faqs_for_page('smash-car-clicker')
    return render_template('smash-car-clicker.html',
                         page_title='Smash Car Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/omega-nuggets-clicker')
def omega_nuggets_clicker():
    faq_data = get_faqs_for_page('omega-nuggets-clicker')
    return render_template('omega-nuggets-clicker.html',
                         page_title='Omega Nugget Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/bear-clicker-girl')
def bear_clicker_girl():
    faq_data = get_faqs_for_page('bear-clicker-girl')
    return render_template('bear-clicker-girl.html',
                         page_title='Bear Clicker Girl',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/italian-brainrot-playground')
def italian_brainrot_playground():
    faq_data = get_faqs_for_page('italian-brainrot-playground')
    return render_template('italian-brainrot-playground.html',
                         page_title='Italian Brainrot Playground',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/merge-fellas-brainrot')
def merge_fellas_brainrot():
    faq_data = get_faqs_for_page('merge-fellas-brainrot')
    return render_template('merge-fellas-brainrot.html',
                         page_title='Merge Fellas Brainrot',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/crazy-mouse-battle')
def crazy_mouse_battle():
    faq_data = get_faqs_for_page('crazy-mouse-battle')
    return render_template('crazy-mouse-battle.html',
                         page_title='Crazy Mouse Battle',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/poor-bunny')
def poor_bunny():
    faq_data = get_faqs_for_page('poor-bunny')
    return render_template('poor-bunny.html',
                         page_title='Poor Bunny',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/lemon-clicker')
def lemon_clicker():
    faq_data = get_faqs_for_page('lemon-clicker')
    return render_template('lemon-clicker.html',
                         page_title='Lemon Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/tung-sahur-clicker')
def tung_sahur_clicker():
    faq_data = get_faqs_for_page('tung-sahur-clicker')
    return render_template('tung-sahur-clicker.html',
                         page_title='Tung Sahur Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/tung-tung-sahur-obby-challenge')
def tung_tung_sahur_obby_challenge():
    faq_data = get_faqs_for_page('tung-tung-sahur-obby-challenge')
    return render_template('tung-tung-sahur-obby-challenge.html',
                         page_title='Tung Tung Sahur Obby Challenge',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/brainrot-clicker')
def brainrot_clicker():
    faq_data = get_faqs_for_page('brainrot-clicker')
    return render_template('brainrot-clicker.html',
                         page_title='Brainrot Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/bear-clicker-female')
def bear_clicker_female():
    faq_data = get_faqs_for_page('bear-clicker-female')
    return render_template('bear-clicker-female.html',
                         page_title='Bear Clicker Female',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/italian-brainrot-clicker-2')
def italian_brainrot_clicker_2():
    faq_data = get_faqs_for_page('italian-brainrot-clicker-2')
    return render_template('italian-brainrot-clicker-2.html',
                         page_title='Italian Brainrot Clicker 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/cat-paw-taba-clicker')
def cat_paw_taba_clicker():
    faq_data = get_faqs_for_page('cat-paw-taba-clicker')
    return render_template('cat-paw-taba-clicker.html',
                         page_title='Cat Paw Taba Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/speed-stars')
def speed_stars():
    faq_data = get_faqs_for_page('speed-stars')
    return render_template('speed-stars.html',
                         page_title='Speed Stars',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/italian-brainrot-2048')
def italian_brainrot_2048():
    faq_data = get_faqs_for_page('italian-brainrot-2048')
    return render_template('italian-brainrot-2048.html',
                         page_title='Italian Brainrot 2048',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/pokemon-gamma-emerald')
def pokemon_gamma_emerald():
    faq_data = get_faqs_for_page('pokemon-gamma-emerald')
    return render_template('pokemon-gamma-emerald.html',
                         page_title='Pokemon Gamma Emerald',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/multi-theme-clicker-game')
def multi_theme_clicker_game():
    faq_data = get_faqs_for_page('multi-theme-clicker-game')
    return render_template('multi-theme-clicker-game.html',
                         page_title='Multi Theme Clicker Game',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/dreamy-room')
def dreamy_room():
    faq_data = get_faqs_for_page('dreamy-room')
    return render_template('dreamy-room.html',
                         page_title='Dreamy Room',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/wacky-flip')
def wacky_flip():
    faq_data = get_faqs_for_page('wacky-flip')
    return render_template('wacky-flip.html',
                         page_title='Wacky Flip',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/merge-fellas')
def merge_fellas():
    faq_data = get_faqs_for_page('merge-fellas')
    return render_template('merge-fellas.html',
                         page_title='Merge Fellas',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/drive-beyond-horizons')
def drive_beyond_horizons():
    faq_data = get_faqs_for_page('drive-beyond-horizons')
    return render_template('drive-beyond-horizons.html',
                         page_title='Drive Beyond Horizons',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-1')
def cookie_clicker_1():
    faq_data = get_faqs_for_page('cookie-clicker-1')
    return render_template('cookie-clicker-1.html',
                         page_title='Cookie Clicker 1',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/wild-west-saga-idle-tycoon-clicker')
def wild_west_saga_idle_tycoon_clicker():
    faq_data = get_faqs_for_page('wild-west-saga-idle-tycoon-clicker')
    return render_template('wild-west-saga-idle-tycoon-clicker.html',
                         page_title='Wild West Saga: Idle Tycoon Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/twitchie-clicker')
def twitchie_clicker():
    faq_data = get_faqs_for_page('twitchie-clicker')
    return render_template('twitchie-clicker.html',
                         page_title='Twitchie Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/italian-brainrot-clicker')
def italian_brainrot_clicker():
    faq_data = get_faqs_for_page('italian-brainrot-clicker')
    return render_template('italian-brainrot-clicker.html',
                         page_title='Italian Brainrot Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/robux-clicker')
def robux_clicker():
    faq_data = get_faqs_for_page('robux-clicker')
    return render_template('robux-clicker.html',
                         page_title='Robux Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/military-capitalist-idle-clicker')
def military_capitalist_idle_clicker():
    faq_data = get_faqs_for_page('military-capitalist-idle-clicker')
    return render_template('military-capitalist-idle-clicker.html',
                         page_title='Military Capitalist Idle Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/race-clicker')
def race_clicker():
    faq_data = get_faqs_for_page('race-clicker')
    return render_template('race-clicker.html',
                         page_title='Race Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/internet-roadtrip')
def internet_roadtrip():
    faq_data = get_faqs_for_page('internet-roadtrip')
    return render_template('internet-roadtrip.html',
                         page_title='Internet Roadtrip',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/smash-car-clicker-2')
def smash_car_clicker_2():
    faq_data = get_faqs_for_page('smash-car-clicker-2')
    return render_template('smash-car-clicker-2.html',
                         page_title='Smash Car Clicker 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/poop-clicker')
def poop_clicker():
    faq_data = get_faqs_for_page('poop-clicker')
    return render_template('poop-clicker.html',
                         page_title='Poop Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/gift-clicker')
def gift_clicker():
    faq_data = get_faqs_for_page('gift-clicker')
    return render_template('gift-clicker.html',
                         page_title='Gift Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/crazy-chicken-3d')
def crazy_chicken_3d():
    faq_data = get_faqs_for_page('crazy-chicken-3d')
    return render_template('crazy-chicken-3d.html',
                         page_title='Crazy Chicken 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/crazy-animal-city')
def crazy_animal_city():
    faq_data = get_faqs_for_page('crazy-animal-city')
    return render_template('crazy-animal-city.html',
                         page_title='Crazy Animal City',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/css-clicker')
def css_clicker():
    faq_data = get_faqs_for_page('css-clicker')
    return render_template('css-clicker.html',
                         page_title='Css Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/clicker-sprunki-2')
def clicker_sprunki_2():
    faq_data = get_faqs_for_page('clicker-sprunki-2')
    return render_template('clicker-sprunki-2.html',
                         page_title='Clicker Sprunki 2',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker-save-the-world')
def cookie_clicker_save_the_world():
    faq_data = get_faqs_for_page('cookie-clicker-save-the-world')
    return render_template('cookie-clicker-save-the-world.html',
                         page_title='Cookie Clicker Save the World',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/click-click-clicker')
def click_click_clicker():
    faq_data = get_faqs_for_page('click-click-clicker')
    return render_template('click-click-clicker.html',
                         page_title='Click Click Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/babe-clicker')
def babe_clicker():
    faq_data = get_faqs_for_page('babe-clicker')
    return render_template('babe-clicker.html',
                         page_title='Babe Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/clicker-royale')
def clicker_royale():
    faq_data = get_faqs_for_page('clicker-royale')
    return render_template('clicker-royale.html',
                         page_title='Clicker Royale',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/chill-guy-clicker')
def chill_guy_clicker():
    faq_data = get_faqs_for_page('chill-guy-clicker')
    return render_template('chill-guy-clicker.html',
                         page_title='Chill Guy Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/planet-clicker')
def planet_clicker():
    faq_data = get_faqs_for_page('planet-clicker')
    return render_template('planet-clicker.html',
                         page_title='Planet Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/astro-robot-clicker')
def astro_robot_clicker():
    faq_data = get_faqs_for_page('astro-robot-clicker')
    return render_template('astro-robot-clicker.html',
                         page_title='Astro Robot Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/tube-clicker')
def tube_clicker():
    faq_data = get_faqs_for_page('tube-clicker')
    return render_template('tube-clicker.html',
                         page_title='Tube Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/titans-clicker')
def titans_clicker():
    faq_data = get_faqs_for_page('titans-clicker')
    return render_template('titans-clicker.html',
                         page_title='Titans Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                      

@app.route('/kiwi-clicker')
def kiwi_clicker():
    faq_data = get_faqs_for_page('kiwi-clicker')
    return render_template('kiwi-clicker.html',
                         page_title='Kiwi Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     

@app.route('/muscle-clicker')
def muscle_clicker():
    faq_data = get_faqs_for_page('muscle-clicker')
    return render_template('muscle-clicker.html',
                         page_title='Muscle Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/money-clicker')
def money_clicker():
    faq_data = get_faqs_for_page('money-clicker')
    return render_template('money-clicker.html',
                         page_title='Money Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/sprunki-clicker')
def sprunki_clicker():
    faq_data = get_faqs_for_page('sprunki-clicker')
    return render_template('sprunki-clicker.html',
                         page_title='Sprunki Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/cookie-clicker')
def cookie_clicker():
    faq_data = get_faqs_for_page('cookie-clicker')
    return render_template('cookie-clicker.html',
                         page_title='Cookie Clicker',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())                     
@app.route('/paper')
def paper():
    # 读取文档数据
    with open('static/data/paper.json', 'r', encoding='utf-8') as f:
        paper_data = json.load(f)
    return render_template('paper.html', paper=paper_data)

@app.route('/privacy-policy')
def privacy_policy():
    try:
        translations_data = get_translations()
        return render_template('privacy-policy.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in privacy policy route: {e}")
        return render_template('error.html', error="An error occurred loading the privacy policy page.")

@app.route('/terms-of-service')
def terms_of_service():
    try:
        translations_data = get_translations()
        return render_template('terms-of-service.html', translations=translations_data)
    except Exception as e:
        app.logger.error(f"Error in terms of service route: {e}")
        return render_template('error.html', error="An error occurred loading the terms of service page.")

def send_message():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, subject, message]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('contact'))
        
        try:
            email_user = os.getenv('EMAIL_USER')
            email_password = os.getenv('EMAIL_PASSWORD')
            
            if not email_user or not email_password:
                flash('Email configuration is not set up', 'error')
                return redirect(url_for('contact'))
            
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_user  # Send to yourself
            msg['Subject'] = f"Sprunkr: {subject} - from {name}"
            
            body = f"""
            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: {message}
            """
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
            server.quit()
            
            flash('Thank you for your message! We will get back to you soon.', 'success')
        except Exception as e:
            app.logger.error(f"Error sending message: {str(e)}")
            flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    except Exception as e:
        app.logger.error(f"Error in send_message: {e}")
        flash('Sorry, there was a problem sending your message. Please try again later.', 'error')
    
    return redirect(url_for('contact'))

# 添加全局错误处理器
@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Server Error: {error}')
    return render_template('error.html', 
                         error_code=500,
                         error_message="Internal Server Error",
                         translations=get_translations()), 500

@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {error}')
    return render_template('error.html', 
                         error_code=404,
                         error_message="Page Not Found",
                         translations=get_translations()), 404

# 导入游戏API处理函数
from api.game_api import game_api

# 添加游戏API路由
@app.route('/game/<path:game_id>', methods=['GET'])
def game_route(game_id):
    app.logger.info(f"处理游戏请求: /game/{game_id}")
    # 将game_id作为查询参数传递给game_api函数
    return game_api(game_id=game_id)

# 添加游戏API路由（用于处理直接的API请求）
@app.route('/api/game-api', methods=['GET'])
def game_api_route():
    app.logger.info(f"处理游戏API请求: {request.url}")
    # 从查询参数中获取game_id
    game_id = request.args.get('gameId')
    return game_api(game_id=game_id)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
