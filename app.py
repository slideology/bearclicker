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

@app.route('/dadish')
def dadish():
    faq_data = get_faqs_for_page('dadish')
    return render_template('dadish.html',
                         page_title='Dadish',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/flying-kong')
def flying_kong():
    faq_data = get_faqs_for_page('flying-kong')
    return render_template('flying-kong.html',
                         page_title='Flying Kong',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())

@app.route('/block-blast-3d')
def block_blast_3d():
    faq_data = get_faqs_for_page('block-blast-3d')
    return render_template('block-blast-3d.html',
                         page_title='Block Blast 3D',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/ssspicy')
def ssspicy():
    faq_data = get_faqs_for_page('ssspicy')
    return render_template('ssspicy.html',
                         page_title='Ssspicy',
                         dynamic_faqs=faq_data['faqs'],
                         conclusion=faq_data['conclusion'],
                         translations=get_translations())
@app.route('/god-simulator')
def god_simulator():
    faq_data = get_faqs_for_page('god-simulator')
    return render_template('god-simulator.html',
                         page_title='God Simulator',
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

@app.route('/stonecraft')
def stonecraft():
    faq_data = get_faqs_for_page('stonecraft')
    return render_template('stonecraft.html',
                         page_title='Stonecraft',
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


@app.route('/pizza-clicker')
def pizza_clicker():
    faq_data = get_faqs_for_page('pizza-clicker')
    return render_template('pizza-clicker.html',
                         page_title='Pizza Clicker',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cookie-clicker2.com')
def cookie_clicker2_com():
    faq_data = get_faqs_for_page('cookie-clicker2.com')
    return render_template('cookie-clicker2.com.html',
                         page_title='Cookie Clicker2.Com',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cookie-clicker-2')
def cookie_clicker_2():
    faq_data = get_faqs_for_page('cookie-clicker-2')
    return render_template('cookie-clicker-2.html',
                         page_title='Cookie Clicker 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/among-us-clicker')
def among_us_clicker():
    faq_data = get_faqs_for_page('among-us-clicker')
    return render_template('among-us-clicker.html',
                         page_title='Among Us Clicker',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cookie-tap')
def cookie_tap():
    faq_data = get_faqs_for_page('cookie-tap')
    return render_template('cookie-tap.html',
                         page_title='Cookie Tap',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/sudoku')
def sudoku():
    faq_data = get_faqs_for_page('sudoku')
    return render_template('sudoku.html',
                         page_title='Sudoku',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/2048')
def game_2048():
    faq_data = get_faqs_for_page('2048')
    return render_template('2048.html',
                         page_title='2048',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cookie-clicker2')
def cookie_clicker2():
    faq_data = get_faqs_for_page('cookie-clicker2')
    return render_template('cookie-clicker2.html',
                         page_title='Cookie Clicker2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/orbit-kick')
def orbit_kick():
    faq_data = get_faqs_for_page('orbit-kick')
    return render_template('orbit-kick.html',
                         page_title='Orbit Kick',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/steal-a-brainrot')
def steal_a_brainrot():
    faq_data = get_faqs_for_page('steal-a-brainrot')
    return render_template('steal-a-brainrot.html',
                         page_title='Steal A Brainrot',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/flying-gorilla')
def flying_gorilla():
    faq_data = get_faqs_for_page('flying-gorilla')
    return render_template('flying-gorilla.html',
                         page_title='Flying Gorilla',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/animal-rampage-3d')
def animal_rampage_3d():
    faq_data = get_faqs_for_page('animal-rampage-3d')
    return render_template('animal-rampage-3d.html',
                         page_title='Animal Rampage 3D',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/sprunki')
def sprunki():
    faq_data = get_faqs_for_page('sprunki')
    return render_template('sprunki.html',
                         page_title='Sprunki',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/wave-road')
def wave_road():
    faq_data = get_faqs_for_page('wave-road')
    return render_template('wave-road.html',
                         page_title='Wave Road',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/supermarket-master')
def supermarket_master():
    faq_data = get_faqs_for_page('supermarket-master')
    return render_template('supermarket-master.html',
                         page_title='Supermarket Master',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/mineclicker')
def mineclicker():
    faq_data = get_faqs_for_page('mineclicker')
    return render_template('mineclicker.html',
                         page_title='Mineclicker',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/color-rush')
def color_rush():
    faq_data = get_faqs_for_page('color-rush')
    return render_template('color-rush.html',
                         page_title='Color Rush',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/traffic-road')
def traffic_road():
    faq_data = get_faqs_for_page('traffic-road')
    return render_template('traffic-road.html',
                         page_title='Traffic Road',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/kaizo-cookie-clicker')
def kaizo_cookie_clicker():
    faq_data = get_faqs_for_page('kaizo-cookie-clicker')
    return render_template('kaizo-cookie-clicker.html',
                         page_title='Kaizo Cookie Clicker',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/10x10-farming')
def game_10x10_farming():
    faq_data = get_faqs_for_page('10x10-farming')
    return render_template('10x10-farming.html',
                         page_title='10X10 Farming',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/crazy-monsters-memory')
def crazy_monsters_memory():
    faq_data = get_faqs_for_page('crazy-monsters-memory')
    return render_template('crazy-monsters-memory.html',
                         page_title='Crazy Monsters Memory',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/alphabet-memory-game')
def alphabet_memory_game():
    faq_data = get_faqs_for_page('alphabet-memory-game')
    return render_template('alphabet-memory-game.html',
                         page_title='Alphabet Memory Game',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/vegetables-collection')
def vegetables_collection():
    faq_data = get_faqs_for_page('vegetables-collection')
    return render_template('vegetables-collection.html',
                         page_title='Vegetables Collection',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/reversi')
def reversi():
    faq_data = get_faqs_for_page('reversi')
    return render_template('reversi.html',
                         page_title='Reversi',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/happy-halloween')
def happy_halloween():
    faq_data = get_faqs_for_page('happy-halloween')
    return render_template('happy-halloween.html',
                         page_title='Happy Halloween',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/hero-rescue')
def hero_rescue():
    faq_data = get_faqs_for_page('hero-rescue')
    return render_template('hero-rescue.html',
                         page_title='Hero Rescue',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/word-wood')
def word_wood():
    faq_data = get_faqs_for_page('word-wood')
    return render_template('word-wood.html',
                         page_title='Word Wood',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/basketball-stars')
def basketball_stars():
    faq_data = get_faqs_for_page('basketball-stars')
    return render_template('basketball-stars.html',
                         page_title='Basketball Stars',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/gold-miner-bros')
def gold_miner_bros():
    faq_data = get_faqs_for_page('gold-miner-bros')
    return render_template('gold-miner-bros.html',
                         page_title='Gold Miner Bros',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/plants-vs-zombies-2')
def plants_vs_zombies_2():
    faq_data = get_faqs_for_page('plants-vs-zombies-2')
    return render_template('plants-vs-zombies-2.html',
                         page_title='Plants Vs Zombies 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/sugar-heroes')
def sugar_heroes():
    faq_data = get_faqs_for_page('sugar-heroes')
    return render_template('sugar-heroes.html',
                         page_title='Sugar Heroes',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/pop-the-eggs')
def pop_the_eggs():
    faq_data = get_faqs_for_page('pop-the-eggs')
    return render_template('pop-the-eggs.html',
                         page_title='Pop The Eggs',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/hex-a-mong')
def hex_a_mong():
    faq_data = get_faqs_for_page('hex-a-mong')
    return render_template('hex-a-mong.html',
                         page_title='Hex A Mong',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/geometry-dash')
def geometry_dash():
    faq_data = get_faqs_for_page('geometry-dash')
    return render_template('geometry-dash.html',
                         page_title='Geometry Dash',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/deep-io')
def deep_io():
    faq_data = get_faqs_for_page('deep-io')
    return render_template('deep-io.html',
                         page_title='Deep Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/crazypartyio')
def crazypartyio():
    faq_data = get_faqs_for_page('crazypartyio')
    return render_template('crazypartyio.html',
                         page_title='Crazypartyio',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/fallerzio')
def fallerzio():
    faq_data = get_faqs_for_page('fallerzio')
    return render_template('fallerzio.html',
                         page_title='Fallerzio',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/super-mario-bros')
def super_mario_bros():
    faq_data = get_faqs_for_page('super-mario-bros')
    return render_template('super-mario-bros.html',
                         page_title='Super Mario Bros',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/goo-goo-gaga-clicker')
def goo_goo_gaga_clicker():
    faq_data = get_faqs_for_page('goo-goo-gaga-clicker')
    return render_template('goo-goo-gaga-clicker.html',
                         page_title='Goo Goo Gaga Clicker',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/checkers')
def checkers():
    faq_data = get_faqs_for_page('checkers')
    return render_template('checkers.html',
                         page_title='Checkers',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/words-finder')
def words_finder():
    faq_data = get_faqs_for_page('words-finder')
    return render_template('words-finder.html',
                         page_title='Words Finder',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/ultimate-tic-tac-toe')
def ultimate_tic_tac_toe():
    faq_data = get_faqs_for_page('ultimate-tic-tac-toe')
    return render_template('ultimate-tic-tac-toe.html',
                         page_title='Ultimate Tic Tac Toe',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/fruit-slice')
def fruit_slice():
    faq_data = get_faqs_for_page('fruit-slice')
    return render_template('fruit-slice.html',
                         page_title='Fruit Slice',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/pull-pin')
def pull_pin():
    faq_data = get_faqs_for_page('pull-pin')
    return render_template('pull-pin.html',
                         page_title='Pull Pin',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/jelly-crush')
def jelly_crush():
    faq_data = get_faqs_for_page('jelly-crush')
    return render_template('jelly-crush.html',
                         page_title='Jelly Crush',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/temple-runner')
def temple_runner():
    faq_data = get_faqs_for_page('temple-runner')
    return render_template('temple-runner.html',
                         page_title='Temple Runner',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/doodle-jump')
def doodle_jump():
    faq_data = get_faqs_for_page('doodle-jump')
    return render_template('doodle-jump.html',
                         page_title='Doodle Jump',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/duck-shooter')
def duck_shooter():
    faq_data = get_faqs_for_page('duck-shooter')
    return render_template('duck-shooter.html',
                         page_title='Duck Shooter',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/super-pineapple-pen')
def super_pineapple_pen():
    faq_data = get_faqs_for_page('super-pineapple-pen')
    return render_template('super-pineapple-pen.html',
                         page_title='Super Pineapple Pen',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/g-switch-3')
def g_switch_3():
    faq_data = get_faqs_for_page('g-switch-3')
    return render_template('g-switch-3.html',
                         page_title='G Switch 3',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/zumba-mania')
def zumba_mania():
    faq_data = get_faqs_for_page('zumba-mania')
    return render_template('zumba-mania.html',
                         page_title='Zumba Mania',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/paperio-2')
def paperio_2():
    faq_data = get_faqs_for_page('paperio-2')
    return render_template('paperio-2.html',
                         page_title='Paperio 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/crowd-city')
def crowd_city():
    faq_data = get_faqs_for_page('crowd-city')
    return render_template('crowd-city.html',
                         page_title='Crowd City',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/master-chess')
def master_chess():
    faq_data = get_faqs_for_page('master-chess')
    return render_template('master-chess.html',
                         page_title='Master Chess',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/run-3')
def run_3():
    faq_data = get_faqs_for_page('run-3')
    return render_template('run-3.html',
                         page_title='Run 3',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/slither-dragon-io')
def slither_dragon_io():
    faq_data = get_faqs_for_page('slither-dragon-io')
    return render_template('slither-dragon-io.html',
                         page_title='Slither Dragon Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/catch-dots')
def catch_dots():
    faq_data = get_faqs_for_page('catch-dots')
    return render_template('catch-dots.html',
                         page_title='Catch Dots',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/flammy')
def flammy():
    faq_data = get_faqs_for_page('flammy')
    return render_template('flammy.html',
                         page_title='Flammy',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/jump-color')
def jump_color():
    faq_data = get_faqs_for_page('jump-color')
    return render_template('jump-color.html',
                         page_title='Jump Color',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cookie-blast')
def cookie_blast():
    faq_data = get_faqs_for_page('cookie-blast')
    return render_template('cookie-blast.html',
                         page_title='Cookie Blast',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/neon-360')
def neon_360():
    faq_data = get_faqs_for_page('neon-360')
    return render_template('neon-360.html',
                         page_title='Neon 360',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/extreme-thumb-war')
def extreme_thumb_war():
    faq_data = get_faqs_for_page('extreme-thumb-war')
    return render_template('extreme-thumb-war.html',
                         page_title='Extreme Thumb War',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/space-blaze')
def space_blaze():
    faq_data = get_faqs_for_page('space-blaze')
    return render_template('space-blaze.html',
                         page_title='Space Blaze',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/stickman-hook')
def stickman_hook():
    faq_data = get_faqs_for_page('stickman-hook')
    return render_template('stickman-hook.html',
                         page_title='Stickman Hook',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/stickman-vector')
def stickman_vector():
    faq_data = get_faqs_for_page('stickman-vector')
    return render_template('stickman-vector.html',
                         page_title='Stickman Vector',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/8-ball-pool')
def game_8_ball_pool():
    faq_data = get_faqs_for_page('8-ball-pool')
    return render_template('8-ball-pool.html',
                         page_title='8 Ball Pool',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/moto-maniac-2')
def moto_maniac_2():
    faq_data = get_faqs_for_page('moto-maniac-2')
    return render_template('moto-maniac-2.html',
                         page_title='Moto Maniac 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/space-hunting')
def space_hunting():
    faq_data = get_faqs_for_page('space-hunting')
    return render_template('space-hunting.html',
                         page_title='Space Hunting',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/stickman-shooter-2')
def stickman_shooter_2():
    faq_data = get_faqs_for_page('stickman-shooter-2')
    return render_template('stickman-shooter-2.html',
                         page_title='Stickman Shooter 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/happy-glass-2')
def happy_glass_2():
    faq_data = get_faqs_for_page('happy-glass-2')
    return render_template('happy-glass-2.html',
                         page_title='Happy Glass 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/neon-invaders')
def neon_invaders():
    faq_data = get_faqs_for_page('neon-invaders')
    return render_template('neon-invaders.html',
                         page_title='Neon Invaders',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/inca-adventure')
def inca_adventure():
    faq_data = get_faqs_for_page('inca-adventure')
    return render_template('inca-adventure.html',
                         page_title='Inca Adventure',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/shortcut-pro')
def shortcut_pro():
    faq_data = get_faqs_for_page('shortcut-pro')
    return render_template('shortcut-pro.html',
                         page_title='Shortcut Pro',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/fireboy-and-watergirl')
def fireboy_and_watergirl():
    faq_data = get_faqs_for_page('fireboy-and-watergirl')
    return render_template('fireboy-and-watergirl.html',
                         page_title='Fireboy And Watergirl',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/pull-mermaid-out')
def pull_mermaid_out():
    faq_data = get_faqs_for_page('pull-mermaid-out')
    return render_template('pull-mermaid-out.html',
                         page_title='Pull Mermaid Out',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/among-us-io')
def among_us_io():
    faq_data = get_faqs_for_page('among-us-io')
    return render_template('among-us-io.html',
                         page_title='Among Us Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/color-spin-2')
def color_spin_2():
    faq_data = get_faqs_for_page('color-spin-2')
    return render_template('color-spin-2.html',
                         page_title='Color Spin 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/wormo-io')
def wormo_io():
    faq_data = get_faqs_for_page('wormo-io')
    return render_template('wormo-io.html',
                         page_title='Wormo Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/cut-the-rope-2')
def cut_the_rope_2():
    faq_data = get_faqs_for_page('cut-the-rope-2')
    return render_template('cut-the-rope-2.html',
                         page_title='Cut The Rope 2',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/colored-drawing')
def colored_drawing():
    faq_data = get_faqs_for_page('colored-drawing')
    return render_template('colored-drawing.html',
                         page_title='Colored Drawing',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/risky-rescue')
def risky_rescue():
    faq_data = get_faqs_for_page('risky-rescue')
    return render_template('risky-rescue.html',
                         page_title='Risky Rescue',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/sweet-candy-mania')
def sweet_candy_mania():
    faq_data = get_faqs_for_page('sweet-candy-mania')
    return render_template('sweet-candy-mania.html',
                         page_title='Sweet Candy Mania',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/whack-a-mole')
def whack_a_mole():
    faq_data = get_faqs_for_page('whack-a-mole')
    return render_template('whack-a-mole.html',
                         page_title='Whack A Mole',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/mahjong')
def mahjong():
    faq_data = get_faqs_for_page('mahjong')
    return render_template('mahjong.html',
                         page_title='Mahjong',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/knife-hit')
def knife_hit():
    faq_data = get_faqs_for_page('knife-hit')
    return render_template('knife-hit.html',
                         page_title='Knife Hit',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/yohoho-io')
def yohoho_io():
    faq_data = get_faqs_for_page('yohoho-io')
    return render_template('yohoho-io.html',
                         page_title='Yohoho Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/aquapark-io')
def aquapark_io():
    faq_data = get_faqs_for_page('aquapark-io')
    return render_template('aquapark-io.html',
                         page_title='Aquapark Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/super-rocket-buddy')
def super_rocket_buddy():
    faq_data = get_faqs_for_page('super-rocket-buddy')
    return render_template('super-rocket-buddy.html',
                         page_title='Super Rocket Buddy',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/stack-colors')
def stack_colors():
    faq_data = get_faqs_for_page('stack-colors')
    return render_template('stack-colors.html',
                         page_title='Stack Colors',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/idle-zoo')
def idle_zoo():
    faq_data = get_faqs_for_page('idle-zoo')
    return render_template('idle-zoo.html',
                         page_title='Idle Zoo',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/alphabet-kitchen')
def alphabet_kitchen():
    faq_data = get_faqs_for_page('alphabet-kitchen')
    return render_template('alphabet-kitchen.html',
                         page_title='Alphabet Kitchen',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/zombie-tsunami-online')
def zombie_tsunami_online():
    faq_data = get_faqs_for_page('zombie-tsunami-online')
    return render_template('zombie-tsunami-online.html',
                         page_title='Zombie Tsunami Online',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/spin-wheel')
def spin_wheel():
    faq_data = get_faqs_for_page('spin-wheel')
    return render_template('spin-wheel.html',
                         page_title='Spin Wheel',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/rolly-vortex')
def rolly_vortex():
    faq_data = get_faqs_for_page('rolly-vortex')
    return render_template('rolly-vortex.html',
                         page_title='Rolly Vortex',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/fire-balls-3d')
def fire_balls_3d():
    faq_data = get_faqs_for_page('fire-balls-3d')
    return render_template('fire-balls-3d.html',
                         page_title='Fire Balls 3D',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/pop-it')
def pop_it():
    faq_data = get_faqs_for_page('pop-it')
    return render_template('pop-it.html',
                         page_title='Pop It',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/flyufo-io')
def flyufo_io():
    faq_data = get_faqs_for_page('flyufo-io')
    return render_template('flyufo-io.html',
                         page_title='Flyufo Io',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/hex-pipes')
def hex_pipes():
    faq_data = get_faqs_for_page('hex-pipes')
    return render_template('hex-pipes.html',
                         page_title='Hex Pipes',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())


@app.route('/pop-us')
def pop_us():
    faq_data = get_faqs_for_page('pop-us')
    return render_template('pop-us.html',
                         page_title='Pop Us',
                         dynamic_faqs=faq_data.get('faqs', []),
                         conclusion=faq_data.get('conclusion', ''),
                         translations=get_translations())

if __name__ == '__main__':
    app.run(debug=True, port=5002)
