import qrcode
image = qrcode.make("Ajaya Kandel")

### WIFI LINK
wifi_type = "WPA"
wifi_ssid = "5GPOC-5G"
wifi_password = "bingobingo"
wifi =f"WIFI:T:{wifi_type};S:{wifi_ssid};P:{wifi_password};;"
img = qrcode.make(wifi)
type(img)  # qrcode.image.pil.PilImage
img.save("wifi.png")