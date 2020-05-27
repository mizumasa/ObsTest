from obswebsocket import obsws, requests

host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
ws.connect()

scenes = ws.call(requests.GetSceneList())

if scenes.status:
    for s in scenes.getScenes():
        print(s["name"])
        for source in s["sources"]:
            print(s["name"],"->",source["name"])

ret = ws.call(requests.GetCurrentScene())
print("current scene : ",ret.getName())
sources = ret.getSources()
print("current sources : ",sources)
for source in sources:
    properties = ws.call(requests.GetSceneItemProperties(source["name"]))
    print("properties : ",properties.datain)
ws.disconnect()