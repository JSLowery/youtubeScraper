from bottle import static_file,route, run, template, get, Bottle, request, hook, PasteServer
import requests
import time
from bs4 import BeautifulSoup, SoupStrainer
from multiprocessing.dummy import Pool
def worker(i):
    r = None
    try:
        r = requests.get('http://www.google.com')
    except Exception as e:
        print(e)
    if (r==None):
        r = 'no'
        return ('<p>no</p>')
    else:
        print(r.status_code+i)
        return ('<p>'+str(r.status_code+i)+'</p>') 
@get("/youtube/<search>")
def youtube(search):
    ret = []
    div = []
    try:
        time1 = time.time()
        #http = urllib3.PoolManager()
        #sauce = http.request('GET','https://youtube.com/results?search_query='+search)
        print("time to urllib: " + str(time.time()-time1))
        r = requests.Session()
        sauce = r.get('https://youtube.com/results?search_query='+search)
        time1 = time.time()
        strainer = SoupStrainer("ol",attrs={'class':'item-section'})
        soup = BeautifulSoup(sauce.text,'lxml', parse_only= strainer)
        print("time to bs: " + str(time.time()-time1))
        #print(len(soup))
        #li = soup.find_all("li")
        #print(len(li))

    except Exception as e:
        print(e)
    tst = {"data":str(soup)}
    return (tst)
@get("/watch")
def watch():
    return '<iframe src="http://www.youtube.com/embed/'+ request.query.v+'" width="560" height="315" frameborder="0" allowfullscreen></iframe>'
@get("/")
def redirect():
    return static_file ("index.html", root = "./html")
@get('/root')
def root():
    tim = time.time()
    p = Pool(32)
    ret =p.map(worker, [i for i in range (32)])
    p.close()
    p.join()
    tim2 = time.time()-tim
    print('time to run was: ', tim2)
    ret.append(str(tim2))
    return (ret)
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run( host='0.0.0.0', port=48346, server=PasteServer)
