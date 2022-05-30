#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import argparse
import urllib

# options
raw=False
quiet=False
all=False
best_match=False
pick_search=False
debug=False
save_html=False
use_cache=False
pick_lang=False
no_pipe=False
plus_urls=False

priority=[
    "tracklist",       # Album track lists ( eg: noisia outer edges tracklist )
    "richcast",        # Rich Rich Answers ( eg: social network cast )
    "define",          # Define ( eg: define Aggrandize )
    "lists",           # Simple lists ( eg Need for Speed Heat cars list )
    "kno_val",         # Chem facts ( eg: density of silver, density of hydrogen, what is the triple point of oxygen )
    "pronounce",       # Learn to pronounce ( eg: pronounce linux )
    "lyrics_int",      # Lyrics ( eg: gecgecgec lyrics )
    "weather",         # Weather ( eg: weather new york )
    "math",            # Math ( eg: log_2(3) * pi^e )
    "unit",            # Units Conversion ( eg: 1m into 1 cm )
    "currency",        # Currency Conversion ( eg: 1 USD in rupee )
    "kno_top",         # Knowledge Graph - top ( list ) ( eg: the office cast )
    "moreans",         # Answers yet again ( eg: Is Linux better than Windows? )
    "basic",           # Basic Answers ( eg: christmas day )
    "feat",            # Featured Snippets ( eg: who is garfield )
    "quotes",          # Quotes ( eg: mahatma gandhi quotes )
    "trans",           # Translate ( eg: Vais para cascais? em ingles )
    "sport_fixture",   # Shows last or next fixture of a sports team ( eg. Chelsea next game )
    "lyrics_us",       # Lyrics for US users, above does not work for US
    "kno_right",       # Knowledge Graph - right ( eg: the office )
    "datetime",        # Time and Date results ( eg: Whats the time || what is the date today ) @DarkMatter-999
]

parser = argparse.ArgumentParser(prog='tuxipy')

parser.add_argument('q', nargs='?', help='Search query')
parser.add_argument('--query', nargs='?', help='Search query')

args = parser.parse_args()

# this div is google's top line answer, works for simple dates, values etc
# eg: density of silver, what is the triple point of oxygen, elevation of mount everest, christmas day
# "what is the " seems to be required for some things //credit @sudocanttype
def a_math():
    return "".join([ a.text for a in google_html.find_all("span", class_ = "qv3Wpe")])

# Math ( eg: log_2(3) * pi^e ) //credit @BeyondMagic
def a_kno_val():
    return "".join([ a.text for a in google_html.find_all("div", class_ = "Z0LcW")])

# Knowledge Graph - top (list) ( eg: the office cast ) //credit @Bugswriter
def a_kno_top():
    for a in google_html.find_all("div", class_ = "jhtnKe oJxN6"):
        x = zip([b.text for b in a.find_all("div", class_="JjtOHd")],[b.text for b in a.find_all("div", class_="ellip yF4Rkc AqEFvb")])
        return "\n".join("".join(i) for i in list(x))

# Quotes ( eg: mahatma gandhi quotes ) //credit @PoseidonCoder
def a_quotes():
    return "".join([ a.text for a in google_html.find_all("div", class_ = "Qynugf")])

# Basic Answers ( eg: summer solstice || easter ) // @Bugswriter
# this displays similar info to kno_val but uses a different div in the google results
def a_basic():
    return "".join([ a.text for a in google_html.find_all("div", class_ = "zCubwf")])

# Answers yet again ( eg: Is Linux better than Windows? ) // @DarkMatter-999
def a_moreans():
    return "".join([ a.text for a in google_html.find_all("span", class_ = "hgKElc")])
    

# # Rich Rich Answers ( eg: social network cast ) //credit @BeyondMagic
# def a_richcast():
#     for a in google_html.find_all("a", class_ = "ct5Ked"):
#         # x = zip([b.text for b in a.find_all("div", class_="JjtOHd")],[b.text for b in a.find_all("div", class_="ellip yF4Rkc AqEFvb")])
#         # return "\n".join("".join(i) for i in list(x))
#         return a.text

# Simple lists (eg: how to exit vim || how to update windows) //original snippet credit @BeyondMagic
def a_lists():
    return "\n".join([a.text for a in google_html.find_all("li", class_ = "TrT0Xe")])

# Featured Snippets ( eg: who is garfield ) //credit @Bugswriter
def a_feat():
    return "".join([ a.find("span").text for a in google_html.find_all("div", class_ = "PZPZlf hb8SAc")])

# Lyrics ( eg: gecgecgec lyrics ) //credit @d-shaun
def a_lyrics_int():
    return "\n".join([ a.text for a in google_html.find_all("span", jsname = "YS01Ge")])

# Weather ( eg: weather new york) //credit @jhagas + @Genghius + @BeyondMagic
def a_weather():
    data = [a.text for a in google_html.find_all("div", class_ = "UQt4rd")]
    if data:
        data = data[0]
        data = data.split("%")

        weather = data[0][:2] + "°C " + data[0][2:4] + "°F\nPrecipitation:" + data[0].split(":")[1] + "\n" + data[1] + "\n" + data[2].split("km/h")[0] + "km/h " + data[2].split("km/h")[1]
        return weather

# Units Conversion ( eg: 1m into 1 cm ) //credit @karthink
def a_unit():
    data = [a.find("input") for a in google_html.find_all("div", id = "NotFQb")]
    if data:
        return data[0]["value"]

# Currency Conversion ( eg: 1 USD in rupee ) //credit @karthink
def a_currency():
    return "".join([ a.text for a in google_html.find_all("span", class_ = "SwHCTb")])

# Translate ( eg: Vais para cascais? em ingles ) //credit @Genghius
def a_trans():
    return "".join([ a.text for a in google_html.find_all("pre", class_ = "XcVN5d")])

# Knowledge Graph - right ( eg: the office ) //credit @Bugswriter
def a_kno_right():
    data = google_html.find("div", class_ = "kno-rdesc")
    if data:
        return "".join([data.find("span").text])

# Learn to pronounce ( eg: pronounce linux ) //credit @sdushantha
def a_pronounce():
    return "".join([a.text for a in google_html.find_all("div", class_ = "TQ7enb")])

# Time and Date results ( eg: Whats the time || what is the date today ) @DarkMatter-999
def a_datetime():
    return "".join([a.text for a in google_html.find_all("div", class_ = "FzvWSb")])
    

def make_req(query):
    google_url = "https://www.google.com/search?"
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    headers = {
        'User-Agent': user_agent
    }
    google_url = google_url + urllib.parse.urlencode({"q" : query})
    # print(google_url)
    try:
        response = requests.get(google_url, headers=headers)
        # print(response.text)
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        return "## Error:", e
        return None

def get_answers(html):
    if not quiet:
            correction = "".join([ a.text for a in google_html.find_all("a", class_ = "gL9Hy")])
            if correction:
                print("Did you mean ", end="")
                print(correction)
            
            outputs = [globals()["a_"+k]() for k in priority if "a_"+k in globals()]
            outputs = [o for o in outputs if o != None and o !='']
            return outputs[0] if outputs else "Could not get results"
            #return outputs


if __name__ == '__main__':
    if args.q == None and args.query == None:
        print("Hi, I'm TuxiPy. Ask me anything!\n")
    else:
        q, query = args.q, args.query
        if q == None:
            q = query
        google_html = make_req(q)
        # print(google_html.prettify())
        print(get_answers(google_html))