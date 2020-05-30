#!/usr/bin/env python
# -*- coding: utf-8 -*-
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



import perlin

if __name__ == "__main__":
    ws = obsws(host, port, password)
    ws.connect()

    ret = ws.call(requests.GetCurrentScene())
    print("current scene : ",ret.getName())
    sources = ret.getSources()
    print("current sources : ",sources)
    for source in sources:
        properties = ws.call(requests.GetSceneItemProperties(source["name"]))
        print("properties : ",properties.datain)


    PNFactoryX = perlin.PerlinNoiseFactory(1)
    PNFactoryY = perlin.PerlinNoiseFactory(1)

    for i in range(1200):
        for source in sources:
            data = requests.SetSceneItemPosition(source["name"],PNFactoryX(i/30.0)*20-20,PNFactoryY(i/30.0)*20-20).data()
            data["message-id"] = 100
            ws.ws.send(json.dumps(data))
            time.sleep(0.03)
    t2 = time.time()

    ws.disconnect()