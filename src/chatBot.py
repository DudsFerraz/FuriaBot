from dotenv import load_dotenv
import os
import telebot
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import threading

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

my_service = Service("/usr/local/bin/chromedriver")

lineup_cs_names = []
lineup_cs = []
lineup_cs_html = ""
results_cs_html = ""
tournaments_cs_html = ""
matches_cs_html = ""
lineup_cs_text = ""
results_cs_text = ""
tournaments_cs_text = ""
matches_cs_text = ""

lineup_cs_names_fe =[]
lineup_cs_fe = []
lineup_cs_html_fe = ""
results_cs_html_fe = ""
tournaments_cs_html_fe = ""
matches_cs_html_fe = ""
lineup_cs_text_fe = ""
results_cs_text_fe = ""
tournaments_cs_text_fe = ""
matches_cs_text_fe = ""

matches_kl_html = ""
matches_kl_text = ""
table_kl_html = ""
table_kl_text = ""

def escape_markdown_v2(text: str) -> str:
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def format_date(unix):
    dt = datetime.datetime.fromtimestamp(unix / 1000)
    return dt.strftime('%d/%m/%Y')

def stealth_html_getter(url: str) -> BeautifulSoup:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-3d-apis")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/124.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    global my_service
    browser = webdriver.Chrome(service=my_service, options=chrome_options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        """
    })
    
    browser.get(url)
    time.sleep(3)

    try:
        allowCookies = browser.find_element("id", "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
        allowCookies.click()
        time.sleep(1)
    except:
        pass

    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.quit()
    return soup



def start_background_updates():
    print("\n\n[STARTUP] Iniciando atualizações iniciais...\n\n")
    update_results_cs(False)
    print("\n\n[STARTUP] results iniciado\n\n")
    time.sleep(5)
    update_matches_cs(False)
    print("\n\n[STARTUP] matches iniciado\n\n")
    time.sleep(5)
    update_lineup_cs(False)
    print("\n\n[STARTUP] lineup iniciado\n\n")
    time.sleep(5)
    update_tournaments_cs(False)
    print("\n\n[STARTUP] tournaments iniciado\n\n")
    update_results_cs(True)
    print("\n\n[STARTUP] results fe iniciado\n\n")
    time.sleep(5)
    update_matches_cs(True)
    print("\n\n[STARTUP] matches fe iniciado\n\n")
    time.sleep(5)
    update_lineup_cs(True)
    print("\n\n[STARTUP] lineup fe iniciado\n\n")
    time.sleep(5)
    update_tournaments_cs(True)
    print("\n\n[STARTUP] tournaments fe iniciado\n\n")
    time.sleep(5)
    update_matches_kl()
    print("\n\n[STARTUP] matches KL iniciado\n\n")
    time.sleep(5)
    update_table_kl()
    print("\n\n[STARTUP] table KL iniciado\n\n")
    print("\n\n[STARTUP] Atualizações automáticas iniciadas com sucesso\n\n")

def update_results_cs(fem: bool):
    global results_cs_html
    global results_cs_html_fe
    global results_cs_text
    global results_cs_text_fe

    if(fem):
        results_cs_html_fe = stealth_html_getter("https://www.hltv.org/results?team=10976")
        results_cs_text_fe = set_results_cs(results_cs_html_fe,True)
        threading.Timer(180, update_results_cs, args=(True,)).start()  # 3 minutos
    else:    
        results_cs_html = stealth_html_getter("https://www.hltv.org/results?team=8297")
        results_cs_text = set_results_cs(results_cs_html,False)
        threading.Timer(180, update_results_cs, args=(False,)).start()  # 3 minutos

def update_tournaments_cs(fem: bool):
    global tournaments_cs_html
    global tournaments_cs_html_fe
    global tournaments_cs_text
    global tournaments_cs_text_fe

    if(fem):
        tournaments_cs_html_fe = stealth_html_getter("https://www.hltv.org/team/10976/furia-fe#tab-eventsBox")
        tournaments_cs_text_fe = set_tournaments_cs(tournaments_cs_html_fe,True)
        threading.Timer(7620, update_tournaments_cs, args=(True,)).start()  # 2 horas e 7 minutos (7620s)
    else:    
        tournaments_cs_html = stealth_html_getter("https://www.hltv.org/team/8297/furia#tab-eventsBox")
        tournaments_cs_text = set_tournaments_cs(tournaments_cs_html,False)
        threading.Timer(7620, update_tournaments_cs, args=(False,)).start()  # 2 horas e 7 minutos (7620s)

def update_matches_cs(fem: bool):
    global matches_cs_html
    global matches_cs_html_fe
    global matches_cs_text
    global matches_cs_text_fe

    if(fem):
        matches_cs_html_fe = stealth_html_getter("https://www.hltv.org/team/10976/furia-fe#tab-matchesBox")
        matches_cs_text_fe = set_matches_cs(matches_cs_html_fe,True)
        threading.Timer(600, update_matches_cs, args=(True,)).start()  # 10 minutos
    else:    
        matches_cs_html = stealth_html_getter("https://www.hltv.org/team/8297/furia#tab-matchesBox")
        matches_cs_text = set_matches_cs(matches_cs_html,False)
        threading.Timer(600, update_matches_cs, args=(False,)).start()  # 10 minutos

def update_lineup_cs(fem: bool):
    global lineup_cs_html
    global lineup_cs_html_fe
    global lineup_cs
    global lineup_cs_fe
    global lineup_cs_names
    global lineup_cs_names_fe
    global lineup_cs_text
    global lineup_cs_text_fe

    if(fem):
        lineup_cs_html_fe = stealth_html_getter("https://www.hltv.org/team/10976/furia-fe#tab-rosterBox")
        set_lineup_cs(lineup_cs_html_fe,lineup_cs_names_fe,lineup_cs_fe)
        lineup_cs_text_fe = set_lineup_cs_text(lineup_cs_fe,True)
        threading.Timer(3720, update_lineup_cs, args=(True,)).start()  # 1 hora e 2 minutos (3720s)
    else:    
        lineup_cs_html = stealth_html_getter("https://www.hltv.org/team/8297/furia#tab-rosterBox")
        set_lineup_cs(lineup_cs_html,lineup_cs_names,lineup_cs)
        lineup_cs_text = set_lineup_cs_text(lineup_cs,False)
        threading.Timer(3720, update_lineup_cs, args=(False,)).start()  # 1 hora e 2 minutos (3720s)

def update_matches_kl():
    global matches_kl_html
    global matches_kl_text

    matches_kl_html = stealth_html_getter("https://kingsleague.pro/pt/times/50-furia-fc")
    matches_kl_text = set_matches_kl(matches_kl_html)
    threading.Timer(600,update_matches_kl).start()

def update_table_kl():
    global table_kl_html
    global table_kl_text

    table_kl_html = stealth_html_getter("https://kingsleague.pro/pt/brazil/classificacao")
    table_kl_text = set_table_kl(table_kl_html)
    threading.Timer(3720,update_table_kl).start()

@bot.message_handler(commands=["noticiasCS"])
def news_cs(message):
    url = "https://www.dust2.com.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,"html.parser")

    def is_furia_news(tag):
        if tag.name != 'a':
            return False
        classes = tag.get("class", [])
        class_str = " ".join(classes)
        if class_str not in [
            "a-block standard-box news-item",
            "a-block standard-box news-item big-article",
            "a-block standard-box news-item wide-article"
        ]:
            return False
        header = tag.find("div", class_="news-item-header")
        if not header:
            return False
        header_text = header.text.lower()
        if "furia" in header_text:
            return True
        return any(player in header_text for player in lineup_cs_names)

    headlines = soup.find_all(is_furia_news)[:5]

    if not headlines:
        bot.send_message(message.chat.id, "Nenhuma notícia encontrada sobre a FURIA ou seus jogadores.", parse_mode="MarkdownV2")
        return

    text = "*📰 Últimas Notícias da FURIA CS:*\n\n"
    news = []
    for h in headlines:
        title = escape_markdown_v2(h.find("div", class_="news-item-header").text.strip())
        link = escape_markdown_v2("https://www.dust2.com.br" + h["href"])
        img_tag = h.find("img")
        img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else None
        news.append((title,link,img_url))

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2")
    for title,link,img_url in news:
        caption = f"*💣  {title}  💣*\n\n 🔗{link}"
        bot.send_photo(message.chat.id, photo=img_url, caption=caption, parse_mode="MarkdownV2")

def set_results_cs(html: BeautifulSoup, fem: bool) -> str:
    if(fem):
        text = "*🐾🖤🎧   Últimos Resultados da FURIA CS fe:*\n\n"
    else:
        text = "*🐾🖤🎧   Últimos Resultados da FURIA CS:*\n\n"

    divs = html.find_all("div", class_="result-con")[:10]
    if not divs:
        return text + "Nenhum resultado recente encontrado\n"

    matches = []
    for d in divs:
        link = "https://www.hltv.org" + d.find("a")["href"]
        date = format_date(int(d["data-zonedgrouping-entry-unix"]))
        teams = d.find_all("td", class_="team-cell")[:2]
        names = [t.find("div", class_="team").text.strip() for t in teams]
        spans = d.find("td", class_="result-score").find_all("span")[:2]
        scores = [s.text.strip() for s in spans]
        event = d.find("td", class_="event").find("span").text.strip()
        matches.append((date, names, scores, event, link))

    for date, names, scores, event, link in matches:
        team1 = escape_markdown_v2(names[0])
        team2 = escape_markdown_v2(names[1])
        event = escape_markdown_v2(event)
        date = escape_markdown_v2(date)
        link = escape_markdown_v2(link)
        emote = "❌"
        if scores[0] > scores[1]:
            emote = "✅"

        text += f"🗓️ {date}\n"
        text += f"{emote} *{team1}* {scores[0]} x {scores[1]} *{team2}*\n"
        text += f"🏆 {event}\n"
        text += f"[🔗 Mais informações]({link})\n\n"

    return text

@bot.message_handler(commands=["resultadosCS"])
def results_cs(message):
    global results_cs_text
    text = results_cs_text

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

def set_tournaments_cs(html: BeautifulSoup, fem: bool) -> str:
    if(fem):
        text = "*🐾🖤🎧   Próximos torneios da FURIA CS fe:*\n\n"
    else:    
        text = "*🐾🖤🎧   Próximos torneios da FURIA CS:*\n\n"

    div = html.find("div", class_="upcoming-events-holder")
    if not div:
        return text + "Nenhum torneio encontrado na agenda\n\n"

    elements = div.find_all("a")[:10]
    if not elements:
        return text + "Nenhum torneio encontrado na agenda\n\n"
    
    events = []
    for e in elements:
        link = "https://www.hltv.org" + e["href"]
        name = e.find("div", class_="eventbox-eventname").text.strip()
        spans = e.find_all("span")
        dates = [s["data-unix"] for s in spans if "data-unix" in s.attrs]

        events.append((name, dates, link))

    for name, dates, link in events:
        name = escape_markdown_v2(name)
        begin_date = escape_markdown_v2(format_date(int(dates[0])))
        end_date = "TBD"
        if len(dates) > 1:
            end_date = escape_markdown_v2(format_date(int(dates[1])))
        link = escape_markdown_v2(link)

        text += f"🏆 {name}\n"
        text += f"🗓️  {begin_date} \\- {end_date}\n"
        text += f"[🔗 Mais informações]({link})\n\n"

    return text

def set_matches_cs(html: BeautifulSoup, fem: bool) -> str:
    if(fem):
        text = "*🐾🖤🎧   Próximas partidas da FURIA CS fe:*\n\n"
    else:
        text = "*🐾🖤🎧   Próximas partidas da FURIA CS:*\n\n"

    h2 = html.find("h2", class_="standard-headline", string=lambda s: s in ["Upcoming matches for FURIA", "Upcoming matches for FURIA fe"])
    if not h2:
        return text + "Nenhuma partida encontrada na agenda\n\n"

    table = h2.find_next_sibling()
    if table.name != "table":
        return text + "Nenhuma partida encontrada na agenda\n\n"
    
    matches = []
    tournaments = []
    for thead in table.find_all("thead")[1:]:
        tournaments.append(thead.find("a").text.strip())

    for tbody in table.find_all("tbody"):
        date_cell = tbody.find("td", class_="date-cell")
        date = date_cell.find("span")["data-unix"]
        furia = tbody.find("a", class_="team-name team-1").text.strip()
        enemy = tbody.find("a", class_="team-name team-2").text.strip()
        link = "https://www.hltv.org" + tbody.find("a", class_="matchpage-button")["href"]
        matches.append((date, furia, enemy, link))

    for tournament, (date, furia, enemy, link) in zip(tournaments, matches):
        date = escape_markdown_v2(format_date(int(date)))
        furia = escape_markdown_v2(furia)
        enemy = escape_markdown_v2(enemy)
        link = escape_markdown_v2(link)
        tournament = escape_markdown_v2(tournament)

        text += f"💥  {furia} x {enemy}\n"
        text += f"🗓️  {date}\n"
        text += f"🏆  {tournament}\n"
        text += f"[🔗 Mais informações]({link})\n\n"

    return text

@bot.message_handler(commands=["agendaCS"])
def schedule_cs(message):
    global tournaments_cs_text
    global matches_cs_text

    text = tournaments_cs_text + matches_cs_text

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

def set_lineup_cs(html: BeautifulSoup, names_list: list, lineup_list: list):
    coach_info = None

    coach_table = html.find("table", class_="table-container coach-table")
    if coach_table:
        a = coach_table.find("a")
        coach_link = "https://www.hltv.org" + a["href"]
        coach_name = a.find("div", class_="text-ellipsis").text.strip()
        names_list.append(coach_name.lower())
        coach_time_div = coach_table.find("div", class_="players-cell center-cell opacity-cell")
        coach_time = [
            t.replace("years", "anos")
             .replace("year", "ano")
             .replace("months", "meses")
             .replace("month", "mês")
             .replace("days", "dias")
             .replace("day", "dia")
            for t in coach_time_div.stripped_strings
        ]
        coach_service_time = " e ".join(coach_time)
        coach_info = (coach_name, coach_service_time, coach_link)

    players_tbody = html.find("table", class_="table-container players-table").find("tbody")
    starters = []
    benchers = []
    trs = players_tbody.find_all("tr")

    for idx, tr in enumerate(trs):
        a = tr.find("a")
        player_link = "https://www.hltv.org" + a["href"]
        player_name = tr.find("div", class_="text-ellipsis").text.strip()
        names_list.append(player_name.lower())
        time_div = tr.find("div", class_="players-cell center-cell opacity-cell")
        time = [
            t.replace("years", "anos")
             .replace("year", "ano")
             .replace("months", "meses")
             .replace("month", "mês")
             .replace("days", "dias")
             .replace("day", "dia")
            for t in time_div.stripped_strings
        ]
        service_time = " e ".join(time)

        if idx < 5:
            starters.append((player_name, service_time, player_link))
        else:
            benchers.append((player_name, service_time, player_link))

    lineup_list.clear()
    lineup_list.append((coach_info, starters, benchers))

def set_lineup_cs_text(lineup_list: list, fem: bool) -> str:
    coach_info, starters, benchers = lineup_list[0]

    if(fem):
        text = "*🐾🖤 Lineup atual da FURIA CS fe:*\n\n"
    else:    
        text = "*🐾🖤 Lineup atual da FURIA CS:*\n\n"

    if coach_info:
        coach_name, coach_time, coach_link = coach_info
        text += f"🎧 *Coach:*\n"
        text += f"🔹 {escape_markdown_v2(coach_name)}   🐾 {escape_markdown_v2(coach_time)} de FURIA 🖤   [perfil HLTV]({escape_markdown_v2(coach_link)})\n\n"

    text += "🔥 *Titulares:*\n"
    for player, time, link in starters:
        text += "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
        text += f"🟢 {escape_markdown_v2(player)}   🐾 {escape_markdown_v2(time)} de FURIA 🖤   [perfil HLTV]({escape_markdown_v2(link)})\n"
    text += "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"

    if benchers:
        text += "\n💺 *Banco:*\n"
        for player, time, link in benchers:
            text += "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            text += f"🔴 {escape_markdown_v2(player)}   🐾 {escape_markdown_v2(time)} de FURIA 🖤   [perfil HLTV]({escape_markdown_v2(link)})\n"
        text += "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"

    return text

@bot.message_handler(commands=["lineupCS"])
def lineup_cs_func(message):
    global lineup_cs_text
    text = lineup_cs_text

    bot.send_message(message.chat.id, text, parse_mode="MarkdownV2", disable_web_page_preview=True)

@bot.message_handler(["resultadosCSfe"])
def results_cs_fe(message):
    global results_cs_text_fe
    text = results_cs_text_fe

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

@bot.message_handler(commands=["agendaCSfe"])
def schedule_cs_fe(message):
    global tournaments_cs_text_fe
    global matches_cs_text_fe

    text = tournaments_cs_text_fe + matches_cs_text_fe

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

@bot.message_handler(commands=["lineupCSfe"])
def lineup_cs_func_fe(message):
    global lineup_cs_text_fe
    text = lineup_cs_text_fe

    bot.send_message(message.chat.id, text, parse_mode="MarkdownV2", disable_web_page_preview=True)

@bot.message_handler(commands=["redesKL"])
def redes_KL(message):
    text = "*🐾⚽  Fique por dentro de tudo que acontece com a FURIA FC\\!*\n\n"
    text += "📸 Instagram: [Clique aqui](https://www.instagram.com/furia.football/)\n\n"
    text += "🎥 YouTube: [Clique aqui](https://www.youtube.com/@FURIAF.C.)\n\n"
    text += "🎵 TikTok: [Clique aqui](https://www.tiktok.com/@furia.football)"

    bot.send_message(message.chat.id, text, parse_mode="MarkdownV2",disable_web_page_preview=True)

def set_matches_kl(html: BeautifulSoup) -> str:
    text = "*🐾🖤⚽   Jogos da FURIA FC:*\n\n"

    divs = html.find("div", id="matchesSlider").find_all("div", class_="turn-wrapper")

    matches = []
    for d in divs:
        date = d.find("p", class_="turn-date").text.strip()
        teams = d.find_all("div", class_="team-data-wrapper")[:2]
        home_team = teams[0].find("div", class_="team-short-name").text.strip()
        away_team = teams[1].find("div", class_="team-short-name").text.strip()
        home_team_result = d.find("div", class_="home-team-result-wrapper").find("div").text.strip()
        away_team_result = d.find("div", class_="away-team-result-wrapper").find("div").text.strip()
        link = "https://kingsleague.pro" + d.find("a", class_="match-data-wrapper")["href"]
        matches.append((date, home_team, away_team, home_team_result, away_team_result, link))

    def team_name_replacer(team: str) -> str:
        return (team.replace("FUR", "Furia FC")
                    .replace("DDL", "Dendele FC")
                    .replace("ELT", "FC Real Elite")
                    .replace("NYV", "Nyvelados FC")
                    .replace("LSC", "LOUD SC")
                    .replace("G3X", "G3X FC")
                    .replace("DMG", "Desimpedidos Goti")
                    .replace("CAP", "Capim FC")
                    .replace("FNK", "Funkbol Clube")
                    .replace("FLX", "Fluxo FC"))

    text = ""
    for date, home_team, away_team, home_team_result, away_team_result, link in matches:
        furia_home = home_team == "FUR"

        home_result_parts = home_team_result.split()
        away_result_parts = away_team_result.split()
        if len(home_result_parts) == 2:
            home_team_result = f"({home_result_parts[1]}) {home_result_parts[0]}"
            away_team_result = f"{away_result_parts[0]} ({away_result_parts[1]})"

        emote = "✅"
        if home_team_result == "-" and away_team_result == "-":
            emote = "🔮"
        elif len(home_result_parts) == 2:
            emote = "➖"
        elif furia_home:
            if home_team_result < away_team_result:
                emote = "❌"
        else:
            if away_team_result < home_team_result:
                emote = "❌"

        date = escape_markdown_v2(date)
        home_team = escape_markdown_v2(team_name_replacer(home_team))
        away_team = escape_markdown_v2(team_name_replacer(away_team))
        home_team_result = escape_markdown_v2(home_team_result)
        away_team_result = escape_markdown_v2(away_team_result)
        link = escape_markdown_v2(link)

        text += f"🗓️  {date}\n"
        text += f"{emote} *{home_team}* {home_team_result} x {away_team_result} *{away_team}*\n"
        text += f"[🔗 Mais informações]({link})\n\n"

    return text
        
@bot.message_handler(commands=["jogosKL"])
def matches_KL(message):
    global matches_kl_text
    text = matches_kl_text

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

def set_table_kl(html: BeautifulSoup) -> str:
    text = "***⚽🥇Tabela de Classificação da Kings League Brazil:***\n\n"

    divs = html.select_one("div.container-standing-rows").find_all("div", class_="standing-row relative min-w-max")

    teams = []
    for d in divs:
        pos = d.find("div", class_="standing-rank").text.strip()
        name = d.find("a").find("h2").text.strip()
        infos = d.find("div", class_="standing-row-data").find_all("span")
        pts = infos[0].text.strip()
        pj = infos[1].text.strip()
        v = infos[2].text.strip()
        sg = infos[8].text.strip()
        teams.append((pos, name, pts, pj, v, sg))

    text += "➖➖➖➖➖➖➖➖➖\n"
    for pos, name, pts, pj, v, sg in teams:
        name = escape_markdown_v2(name)
        pos = escape_markdown_v2(pos)
        pts = escape_markdown_v2(pts)
        pj = escape_markdown_v2(pj)
        v = escape_markdown_v2(v)
        sg = escape_markdown_v2(sg)

        emote = "🟢" if int(pos) == 1 else ("🟡" if int(pos) <= 7 else "🔴")
        estrela = " ⭐" if "Furia FC" in name else ""
        text += f"{emote} {pos}º \\- *{name}*{estrela}\n"
        text += f"Pts: {pts} \\| PJ: {pj} \\| V: {v} \\| SG: {sg}\n"
        text += "➖➖➖➖➖➖➖➖➖\n"

    text+="\n[🔗 Mais informações](https://kingsleague.pro/pt/brazil/classificacao)\n"

    return text

@bot.message_handler(commands=["tabelaKL"])
def table_KL(message):
    global table_kl_text
    text = table_kl_text

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

@bot.message_handler(commands=["ingressosKL"])
def ingressos_KL(message):
    text = "Garanta seu ingresso para a Kings League Brazil👇\n\n"
    text += "[Clique aqui](https://www.eventim.com.br/artist/kings-league-brazil)"

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

@bot.message_handler(commands=["redes"])
def social_media(message):
    text = "*🐾🖤  Fique por dentro de tudo que acontece com a FURIA\\!*\n\n"

    text+= "*** 🎥YouTube:***\n"
    text += "Esports: [Clique aqui](https://www.youtube.com/@FURIAgg)\n"
    text += "CS: [Clique aqui](https://www.youtube.com/@FURIAggCS)\n"
    text += "R6: [Clique aqui](https://www.youtube.com/@FURIAggR6)\n"
    text += "Valorant: [Clique aqui](https://www.youtube.com/@FURIAggVAL)\n"
    text += "LOL: [Clique aqui](https://www.youtube.com/@FURIAggLOL)\n"
    text += "FC: [Clique aqui](https://www.youtube.com/@FURIAF.C.)\n\n"

    text+= "***🎵 TikTok:***\n"
    text += "Esports: [Clique aqui](https://www.tiktok.com/@furia.football)\n"
    text += "Creators: [Clique aqui](https://www.tiktok.com/@furia.football)\n\n"

    text += "📸 Instagram: [Clique aqui](https://www.instagram.com/furiagg/)\n\n"

    text+= "🐦 Twitter/X: [Clique aqui](https://x.com/FURIA)\n\n"

    text+= "📺 Twitch: [Clique aqui](https://www.twitch.tv/team/furia)\n\n"

    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2",disable_web_page_preview=True)

@bot.message_handler(commands=["loja"])
def loja(message):
    text = "🔥🧥 Fique estiloso e furioso\n\n"
    text+= "[Loja oficial FURIA](https://www.furia.gg/)"
    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2")

def permit_all(message):
    return True

@bot.message_handler(func=permit_all)
def default(message):
    greeting = f"Eaí {message.from_user.first_name}, beleza? Eu estou aqui para fortalecer sua paixão pela FURIA\\!"
    text = f"""
    {greeting}

Para que possamos interagir, escolha uma das opções abaixo:

***Counter\\-Strike 2***
/noticiasCS \\- Últimas noticias
🔵
/resultadosCS \\- Últimos resultados
/agendaCS \\- Próximos compromissos
/lineupCS \\- Lineup furiosa
🟣
/resultadosCSfe \\- Últimos resultados FURIA fe
/agendaCSfe \\- Próximos compromissos FURIA fe
/lineupCSfe \\- Lineup furiosa feminina

***Kings League***
/jogosKL \\- Resultados e próximos jogos FURIA FC
/tabelaKL \\- Classificação da Kings League Brazil
/redesKL \\- Redes Sociais FURIA FC
/ingressosKL \\- Sua oportunidade de ver nossos craques de perto\\!
                    
***Conecte\\-se***
/redes \\- Redes sociais FURIA
/loja \\- Loja oficial FURIA
"""
    bot.send_message(message.chat.id,text,parse_mode="MarkdownV2")

start_background_updates()
bot.infinity_polling(skip_pending=True)