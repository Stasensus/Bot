from PIL import Image, ImageDraw, ImageFont

width = 250
height = 250
message = "Hello boss!"
font = ImageFont.truetype("arial.ttf", size=36)

img = Image.new('RGB', (width, height), color='black')

imgDraw = ImageDraw.Draw(img)

textWidth, textHeight = imgDraw.textsize(message, font=font)
xText = (width - textWidth) / 2
yText = (height - textHeight) / 2

imgDraw.text((xText, yText), message, font=font, fill=(255, 255, 255))

img.save('result.png')
img.show()