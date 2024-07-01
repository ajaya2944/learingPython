import qrcode

# MAP QRcode
email = "a.k.a2023technology@gmail.com"
message = "Hello this is my fst email"

# Create qr code generator that send email to user
mail = f"mailto:{email}?subject=QR Code Message&body={message}"
img = qrcode.make(mail)
type(img)  # qrcode.image.pil.PilImage
img.save("email.png")
