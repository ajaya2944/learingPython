import qrcode

# MAP QRcode
latt = 35.7031578
long = 139.7723765

# Create a Google Maps URL with the latitude and longitude
address = f"https://www.google.com/maps?q={latt},{long}"
img = qrcode.make(address)
type(img)  # qrcode.image.pil.PilImage
img.save("address.png")

