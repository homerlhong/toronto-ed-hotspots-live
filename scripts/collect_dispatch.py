"""Collect Toronto Fire CAD active incidents. Fail closed if schema is unknown."""
import datetime as dt
import json
import pathlib
import urllib.request
import xml.etree.ElementTree as ET

URL = "https://www.toronto.ca/data/fire/livecad.xml"
OUTPUT = pathlib.Path("dispatch-data.json")
request = urllib.request.Request(URL, headers={"User-Agent": "REVENGERS-Public-Safety-Dashboard/1.1"})
with urllib.request.urlopen(request, timeout=30) as response:
    payload = response.read()
root = ET.fromstring(payload)
def local(tag):
    return tag.rsplit("}", 1)[-1].lower()
# Known incident record tag candidates. Inspect the real XML and refuse unknown formats.
for tag in ("event", "incident", "row", "call"):
    records = [e for e in root.iter() if local(e.tag) == tag]
    if records:
        break
else:
    raise ValueError("Unrecognized Toronto Fire XML schema; no sample saved")
# Avoid counting unrelated nested tags or an XML wrapper.
count = len(records)
if count > 500:
    raise ValueError("Unexpectedly high active incident count; inspect source")
now = dt.datetime.now(dt.timezone.utc).isoformat()
data = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {}
fire = data.setdefault("fire", {})
history = fire.setdefault("history", [])
history.append({"at": now, "count": count})
fire["history"] = history[-2016:]
fire["source"] = URL
fire["measurement"] = "Number of publicly listed active fire dispatch incidents"
fire["last_success_utc"] = now
data["police"] = {"status": "UNAVAILABLE", "measurement": "Public police calls for service; not total 911 calls"}
OUTPUT.write_text(json.dumps(data, indent=2) + "\n")
print("Verified active fire incidents:", count, "at", now)
