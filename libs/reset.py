import network

def disable_wlan(self):
    ap = network.WLAN(network.AP_IF)
    ap.active(False)
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)

disable_wlan()
