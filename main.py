from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import requests
from lxml.html import fromstring
from lxml import html


import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


class Queue:
    def __init__(self):
        self.a = []
        self.r = 0
        self.l = 0
    def size(self):
        return self.r - self.l
    def pop(self):
        self.l += 1
    def push(self, x):
        if (self.r == len(self.a)):
            self.a.append(x)
        else:
            self.a[self.r] = x
        self.r += 1
    def front(self):
        return self.a[self.l]
    def empty(self):
        return self.size() == 0

pref = ""

def getLinks(url):
    try:
        page = requests.get(url)
        s = page.text
        i = 0
        res = []
        while i + 5 < len(s):
            if s[i] + s[i + 1] + s[i + 2] + s[i + 3] + s[i + 4] + s[i + 5] == "a href":
                found = False
                b = 0
                t = ""
                while s[i] + s[i + 1] + s[i + 2] + s[i + 3] != "</a>":
                    if s[i] + s[i + 1] + s[i + 2] + s[i + 3] + s[i + 4] + s[i + 5] == "title=":
                        i += 7;
                        found = True
                        while s[i] != '"':
                            t += s[i]
                            i += 1
                    i += 1 
                if found:
                    if not (";" in t or ":" in t):
                        link = t.replace(' ', '_')
                        res.append([pref + link, t])
            i += 1
        return res
    except:
        return []

def get_page(url):
    try:
        r = requests.get(url)
        return r.text
    except:
        return "no page" 
def getTitle(url):
    try:
        r = requests.get(url)
        tree = fromstring(r.content)
        s = tree.findtext('.//title')
        return s[:-12]
    except:
        return "noname"

if __name__ == '__main__':
    start = input("Enter start url\n")
    tmp = start
    if tmp[len(tmp) - 1] == '/':
        tmp = tmp[:len(tmp) - 2]
    while tmp[len(tmp) - 1] != '/':
        tmp = tmp[:-1]
    pref = tmp
    end = input("Enter end url\n")
    end_t = getTitle(end)
    print("Going from " + '"' + getTitle(start) + '"' + " to " '"' + end_t + '"')
    q = Queue()

    end_word_vector = text_to_vector(get_page(end))
    
    q.push([start, getTitle(start)])
    d = {}
    d[getTitle(start)] = 0
    while not q.empty():
        v = q.front()[0]
        v_t = q.front()[1]
        if v == end:
            print("Done with " + str(d[v_t]) + " steps")
            exit(0)
        q.pop()
        links = getLinks(v)
        print(v_t)
        print("similarity to end page ", round(get_cosine(end_word_vector, text_to_vector(get_page(v))) * 10000))
        print("current deep = " + str(d[v_t]))
        for link, link_t in links:
            if link_t not in d:
                d[link_t] = d[v_t] + 1
                if link_t == end_t:
                    print("Done with " + str(d[link_t]) + " steps")
                    exit(0)
                q.push([link, link_t])
print("Can't get end link")
