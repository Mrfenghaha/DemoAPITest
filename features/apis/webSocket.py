# -*- coding: utf-8 -


def wws(token, sid):

    request = {
        "protocol": "WebSocket",
        "url": ("BeeArt", "/socket.io/?token=%s&sid=%s" % (token, sid)),
        "data": "2"
    }
    return request
