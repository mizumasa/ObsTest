import time
import json
import numpy as np
from obswebsocket import obsws, requests

#document
# https://github.com/Elektordi/obs-websocket-py/blob/master/obswebsocket/requests.py
#original document
# https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md


host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
ws.connect()

ret = ws.call(requests.GetCurrentScene())
print("current scene : ",ret.getName())
sources = ret.getSources()
print("current sources : ",sources)
for source in sources:
    properties = ws.call(requests.GetSceneItemProperties(source["name"]))
    print("properties : ",properties.datain)

t0 = time.time()
for i in range(50):
    for source in sources:
        properties = ws.call(requests.SetSceneItemPosition(source["name"],np.sin(i/20.0)*100+100,0))
t1 = time.time()

#command no wait mode
for i in range(200):
    for source in sources:
        #properties = ws.send(requests.SetSceneItemPosition(source["name"],0,np.sin(i/20.0)*100+100).data())
        data = requests.SetSceneItemPosition(source["name"],0,np.sin(i/20.0)*100+100).data()
        data["message-id"] = 100
        ws.ws.send(json.dumps(data))
        time.sleep(0.03)
t2 = time.time()

for i in range(50):
    for source in sources:
        properties = ws.call(requests.SetSceneItemPosition(source["name"],np.sin(i/10.)*100+100,np.cos(i/10.)*100+100))
t3 = time.time()

for i in range(50):
    for source in sources:
        properties = ws.call(requests.SetSceneItemCrop(source["name"],np.sin(i/10.)*10+10,np.cos(i/10.)*10+10,0,0))
t4 = time.time()
print(t1-t0)
print(t2-t1)
print(t3-t2)
print(t4-t3)

ws.disconnect()