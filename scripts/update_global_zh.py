#!/usr/bin/env python3
"""Public-source snapshots for REVENGERS Traditional Chinese dashboard."""
import datetime as dt
import email.utils
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
NOW=dt.datetime.now(dt.timezone.utc)
HEADERS={"User-Agent":"REVENGERSGlobal/1.0 (public informational dashboard)"}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=17) as r:
        return json.load(r)
def rss(query):
    q=urllib.parse.quote(query)
    url=f"https://news.google.com/rss/search?q={q}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    with urllib.request.urlopen(urllib.request.Request(url,headers=HEADERS),timeout=17) as r:
        root=ET.fromstring(r.read(1500000))
    out=[]; seen=set()
    for x in root.findall("./channel/item"):
        title=(x.findtext("title") or "").strip();link=(x.findtext("link") or "").strip()
        try: t=email.utils.parsedate_to_datetime(x.findtext("pubDate")).astimezone(dt.timezone.utc)
        except (TypeError,ValueError):continue
        if title and title not in seen and link.startswith("https://") and NOW-dt.timedelta(hours=36)<=t<=NOW+dt.timedelta(minutes=5):
            out.append({"title":title[:240],"url":link,"source":(x.findtext("source") or "媒體")[:80],"published_at":t.isoformat()});seen.add(title)
        if len(out)>=8:break
    return out
data={"updated_at":NOW.isoformat(),"status":{},"news":{}}
def attempt(name,func):
    try:
        val=func();data["status"][name]="OK";return val
    except Exception as e:
        data["status"][name]="UNAVAILABLE: "+str(e)[:120]
        print(name,data["status"][name])
        return None
def quake():
    j=get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson")
    pts=[]
    for f in j["features"]:
        c=f.get("geometry",{}).get("coordinates",[])
        if len(c)<2:continue
        pts.append({"lat":c[1],"lon":c[0],"mag":f["properties"].get("mag"),"kind":"quake","title":f["properties"].get("place","地震")})
    return {"count":len(pts),"points":pts[:600]}
def eonet():
    j=get("https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=150")
    pts=[]
    for e in j["events"]:
        geom=next((g for g in reversed(e.get("geometry",[])) if g.get("type")=="Point" and len(g.get("coordinates",[]))>=2),None)
        if geom:
            lon,lat=geom["coordinates"][:2]
            pts.append({"lat":lat,"lon":lon,"kind":"event","title":e.get("title","自然事件")})
    return {"count":len(j["events"]),"points":pts}
def space():
    j=get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json")
    if len(j)<2:raise ValueError("No Kp observations")
    row=j[-1]
    return {"kp":row[1],"observed_at":row[0],"note":"Kp 是地磁活動指標，並非太空船返航安全許可"}
def tornado():
    j=get("https://api.weather.gov/alerts/active?event=Tornado%20Warning")
    return {"count":len(j.get("features",[])),"scope":"United States NWS active Tornado Warning"}
def weather():
    cities=[("臺北",25.03,121.56),("東京",35.68,139.69),("紐約",40.71,-74.01),("多倫多",43.65,-79.38),("倫敦",51.51,-.13),("雪梨",-33.87,151.21)]
    lat=",".join(str(c[1]) for c in cities);lon=",".join(str(c[2]) for c in cities)
    url="https://api.open-meteo.com/v1/forecast?"+urllib.parse.urlencode({"latitude":lat,"longitude":lon,"current":"temperature_2m,cloud_cover,wind_speed_10m","timezone":"UTC"})
    j=get(url);j=j if isinstance(j,list) else [j]
    return {"cities":[{"name":c[0],"temp":v["current"]["temperature_2m"],"cloud":v["current"]["cloud_cover"],"wind":v["current"]["wind_speed_10m"]} for c,v in zip(cities,j)]}
for name,func in [("quakes",quake),("events",eonet),("space_weather",space),("tornado",tornado),("weather",weather)]:
    data[name]=attempt(name,func)
queries={"politics":"國際 政治 重大新聞 when:1d","technology":"人工智慧 科技 資安 IT when:1d","finance":"全球 金融 股市 經濟 when:1d","stormnews":"颱風 颶風 龍捲風 天氣 警報 when:1d","space":"NASA ISS 太空人 返回 地球 太空天氣 when:1d"}
for name,query in queries.items():
    data["news"][name]=attempt("news_"+name,lambda q=query:rss(q)) or []
def youtube_videos():
    """Optional official YouTube Data API; no guessed video IDs or scraped embeds."""
    key=os.environ.get("YOUTUBE_API_KEY","").strip()
    if not key:
        raise RuntimeError("YOUTUBE_API_KEY not configured; video discovery disabled")
    categories=[
        ("world","world breaking news today"),
        ("weather","severe weather hurricane tornado latest news"),
        ("earth","earthquake wildfire natural disaster latest news"),
        ("space","NASA space news latest"),
        ("business","global economy technology news today"),
    ]
    found=[]
    for category,query in categories:
        params=urllib.parse.urlencode({"part":"snippet","type":"video","videoEmbeddable":"true",
            "videoSyndicated":"true","order":"date","maxResults":3,"q":query,
            "publishedAfter":(NOW-dt.timedelta(hours=48)).strftime("%Y-%m-%dT%H:%M:%SZ"),"key":key})
        try:
            result=get("https://www.googleapis.com/youtube/v3/search?"+params)
        except Exception as e:
            print("youtube",category,str(e)[:100]);continue
        for item in result.get("items",[]):
            vid=item.get("id",{}).get("videoId","")
            snippet=item.get("snippet",{})
            if len(vid)!=11 or not all(c.isalnum() or c in "_-" for c in vid):continue
            if any(v["id"]==vid for v in found):continue
            found.append({"id":vid,"category":category,"title":snippet.get("title","")[:180],
                "channel":snippet.get("channelTitle","")[:90],"published_at":snippet.get("publishedAt"),
                "url":"https://www.youtube.com/watch?v="+vid})
            break
    if not found:raise RuntimeError("No eligible recent embeddable videos returned")
    return found[:5]
data["videos"]=attempt("youtube_videos",youtube_videos) or []
if not any(data["news"].values()) and not any(data.get(k) for k in ("quakes","events","space_weather","weather","tornado")):
    raise SystemExit("All sources failed; refusing to publish")
Path("global-zh-data.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
print("Updated Traditional Chinese dashboard snapshot")
