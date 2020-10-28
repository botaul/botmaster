import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from os import remove
import time
from os.path import exists


class Media:
    def __init__(self):
        print("Initialize media..")

    def download_image(self):
        '''
        download random image from picsum
        save downloaded_bg.png
        '''
        try:
            url = 'https://picsum.photos/720/1280/?random'
            r = requests.get(url, allow_redirects=True)
            with open("downloaded_bg.png", 'wb') as f:
                f.write(r.content)
                f.close()
            time.sleep(2)
            while exists('downloaded_bg.png') == False:
                time.sleep(3)
        except Exception as ex:
            print(ex)
            pass

    def process_image(self, text, author):
        '''
        edit image
        text: -> str
        author: -> str
        save ready.png
        '''
        try:
            text = textwrap.fill(text, width=35)
            image = Image.open("downloaded_bg.png").filter(
                ImageFilter.GaussianBlur(5))
            image = ImageEnhance.Brightness(image)
            image.enhance(0.5).save('image.png')
            time.sleep(2)
            while exists('image.png') == False:
                time.sleep(3)
            image = Image.open('image.png')
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('Mulish-VariableFont_wght.ttf', size=30)
            w, h = draw.textsize(text, font=font)
            draw.text(((720 - w) / 2, (1280 - h) / 2), text,
                      (255, 255, 255), align="center", font=font)
            if author is not None:
                _author = '@%s' % str(author)
                font = ImageFont.truetype(
                    'Mulish-VariableFont_wght.ttf', size=25)
                x, y = draw.textsize(_author, font=font)
                draw.text(((720 - x) / 2, ((1280 / 2) + h) + 60),
                          _author, (255, 255, 255), font=font, align="bottom")
            image.save('ready.png')
            time.sleep(2)
            while exists('ready.png') == False:
                time.sleep(3)
            remove('downloaded_bg.png')
            remove('image.png')
        except Exception as ex:
            print(ex)
            pass
