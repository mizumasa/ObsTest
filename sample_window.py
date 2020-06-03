#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import numpy as np
import json
import cv2
from obswebsocket import obsws, requests
from window import WINDOW_EASER

host = "localhost"
port = 4444
password = "secret"


class PROPERTIES:
    def __init__(self,d):
        self.sourceHeight = d["sourceHeight"]
        self.sourceWidth = d["sourceWidth"]
        print(self.sourceHeight,self.sourceWidth)
    def getScale(self,drawHeight):
        return 1.0 * drawHeight / self.sourceHeight

def main():
    ws = obsws(host, port, password)
    ws.connect()

    ret = ws.call(requests.GetCurrentScene())
    print("current scene : ",ret.getName())
    sources = ret.getSources()
    print("current sources : ",sources)
    for source in sources:
        properties = ws.call(requests.GetSceneItemProperties(source["name"]))
        print("properties : ",properties.datain)
        s1 = PROPERTIES(properties.datain)

    w = WINDOW_EASER(1280,720)
    w.setWindow("f1")
    w.setKeyFrame("f1",10*2,[0,0,1,1])
    w.setKeyFrame("f1",20*2,[0.25,0.25,0.5,0.5])
    w.setKeyFrame("f1",30*2,[0.25,0.25,0.5,0.5])
    w.setKeyFrame("f1",40*2,[0.05,0.25,0.4,0.4])
    w.setKeyFrame("f1",50*2,[0.05,0.25,0.4,0.4])
    w.setKeyFrame("f1",60*2,[0.55,0.25,0.4,0.4])
    w.setKeyFrame("f1",70*2,[0.55,0.25,0.4,0.4])
    w.setKeyFrame("f1",80*2,[0,0,1,1])
    w.setupKeyFrame()
    while 1:
        for i in range(80*2):
            #print "=====================",i
            ret = w.update()
            #frame = w.draw()
            for source in sources:
                scale = s1.getScale(ret["f1"][3])
                data = requests.SetSceneItemTransform(source["name"],scale,scale,0).data()
                data["message-id"] = 100
                ws.ws.send(json.dumps(data))
                time.sleep(0.01)

                data = requests.SetSceneItemPosition(source["name"],ret["f1"][0],ret["f1"][1]).data()
                data["message-id"] = 100
                ws.ws.send(json.dumps(data))
                time.sleep(0.01)

            #cv2.imshow("window",frame)
            #cv2.waitKey(1)
        w.initKeyFrame()


    ws.disconnect()


if __name__ == "__main__":
    main()
