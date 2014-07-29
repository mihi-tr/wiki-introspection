import urllib2
import json
import lxml.html
import datetime

base="http://wiki.okfn.org"

start="%s/Special:Categories"%base


nodes=[]
nodelookup={}

def get_pages(root):
    return root.xpath("//div[@id='content']//ul/li/a/@href")

def get_categories():
    u=urllib2.urlopen(start)
    r=lxml.html.fromstring(u.read())
    return get_pages(r)

def get_category(l):
    u=urllib2.urlopen("%s%s"%(base,l))
    r=lxml.html.fromstring(u.read())
    return [(l,i) for i in get_pages(r)]

def get_data():
    return reduce(lambda x,y: x+y, [get_category(i) for i in
    get_categories()],[])

def construct_dump():
    links=[]
    for link in get_data():
        links.append(get_link(link))
    return {"nodes": [{"name":i, "degree":count_node(i,links)} for i in nodes],
        "links": links}

def count_node(n,links):
    return sum(map(lambda x: get_node(n) in x.values(), links))

def get_link(l):
    return {"source": get_node(l[0]),
        "target": get_node(l[1]), }

def get_node(n):    
    if n not in nodes:
        nodes.append(n)
        nodelookup[n]=len(nodes)-1
        return len(nodes)-1
    else:
        return nodelookup[n]

if __name__=="__main__":
    date=datetime.datetime.now()
    data=construct_dump()
    with open("categories.json","wb") as f:
        json.dump(data,f)
    with open("categories-%s.json"%date.isoformat(),"wb") as f:
        json.dump(data,f)
