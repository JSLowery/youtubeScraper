from bottle import static_file,route, run, template, get, Bottle, request, hook, PasteServer
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing.dummy import Pool
@get("/youtube/<search>")
def youtube(search):
    ret = []
    div = []
    try:
        time1 = time.time()
        print("time to request: " + str(time.time()-time1))
        r = requests.Session()
        sauce = r.get('https://youtube.com/results?search_query='+search)
        time1 = time.time()
        strainer = SoupStrainer("div",attrs={'class':'yt-lockup-content'})
        soup = BeautifulSoup(sauce.text,'lxml', parse_only= strainer)
        aList = soup.find_all('a')
        for a in aList:
            a['href']="javascript:call_get('"+a['href']+"')"
        h3 = soup.find_all('h3')
        for h in h3:
          a = h.find('a')
          if a.has_attr('data-url'):
              if  'googleads' in  a['data-url']:
                  _=a.extract()
        print("time to bs: " + str(time.time()-time1))
        #print(len(soup))
        #li = soup.find_all("li")
        #print(len(li))

    except Exception as e:
        print(e)
    tst = {"data":str(h3)}
    return (tst)
@get("/watch")
def watch():
    return '<iframe src="http://www.youtube.com/embed/'+ request.query.v+'" width="560" height="315" frameborder="0" allowfullscreen></iframe>'
@get("/")
def redirect():
    return static_file ("index.html", root = "./html")

run( host='0.0.0.0', port=48346, server=PasteServer)
