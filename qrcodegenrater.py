import qrcode
img = qrcode.make('AJAYA KANDEL',
                  "Phone:+810902961733",
                  "Address:Tokyo,Japan"
                  )
type(img)  # qrcode.image.pil.PilImage
img.save("ajaya.png")