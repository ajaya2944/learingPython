import qrcode


### WIFI LINK
phone = "08029617333"
message = "Hello How are you?"
sms =f"SMSTO:{phone}:{message};"
img = qrcode.make(sms)
type(img)  # qrcode.image.pil.PilImage
img.save("sms.png")