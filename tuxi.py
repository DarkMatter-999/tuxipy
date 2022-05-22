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
    "basic",           # Basic Answers ( eg: christmas day )
    "feat",            # Featured Snippets ( eg: who is garfield )
    "quotes",          # Quotes ( eg: mahatma gandhi quotes )
    "trans",           # Translate ( eg: Vais para cascais? em ingles )
    "sport_fixture",   # Shows last or next fixture of a sports team ( eg. Chelsea next game )
    "lyrics_us",       # Lyrics for US users, above does not work for US
    "kno_right",       # Knowledge Graph - right ( eg: the office )
]

parser = argparse.ArgumentParser(prog='tuxipy')

parser.add_argument('q', nargs='?', help='Search query')
parser.add_argument('--query', nargs='?', help='Search query')

args = parser.parse_args()

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
        print("## Error:", e)
        return None

if args.q == None and args.query == None:
    print("Hi, I'm TuxiPy. Ask me anything!\n")
else:
    q, query = args.q, args.query
    if q != None:
        res = make_req(q)
        # print(res.prettify())
        if not quiet:
            print("Did you mean ", end="")
            print("".join([ a.text for a in res.find_all("a", class_ = "gL9Hy")]))

            # print(globals()["parser"])
    else:
        make_req(query)