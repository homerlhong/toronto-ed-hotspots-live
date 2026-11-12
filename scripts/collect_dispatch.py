import json, re, urllib.request, datetime, pathlib, xml.etree.ElementTree as ET
URL = "https://www.toronto.ca/data/fire/livecad.xml"
OUT = pathlib.Path("dispatch-data.json")
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
request = urllib.request.Request(URL, headers={"User-Agent":"REVENGERS-Research-Demo/1.0"})
with urllib.request.urlopen(request, timeout=25) as response:
    payload = response.read()
root = ET.fromstring(payload)
# Only count known incident nodes. Refuse ambiguous schemas rather than fabricate values.
names = {"event", "incident", "call", "row"}
candidates = [node for node in root.iter() if node.tag.rsplit("}",1)[-1].lower() in names]
if not candidates:
    raise ValueError("Unrecognized CAD XML structure: no count recorded")
count = len(candidates)
if count > 2000:
    raise ValueError("Implausible incident count")
data = json.loads(OUT.read_text()) if OUT.exists() else {"fire":{"history":[]}}
history = data.setdefault("fire",{}).setdefault("history",[])
history.append({"at":now,"count":count})
data["fire"]["history"] = history[-288:]
data["fire"]["source"] = URL
data["fire"]["measurement"] = "Count of published active CAD incident entries"
data["police"] = {"status":"UNAVAILABLE","reason":"No verified TPS API connected"}
OUT.write_text(json.dumps(data,indent=2)+"\n")
print("Collected",count,"Toronto Fire incidents at",now)
