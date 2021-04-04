from os.path import exists
from twitter_autobase import watermark as wm


def test_make_watermarked_image():
	wm.watermark_text_image(
		filename='twitter_autobase/watermark/filename.jpg',
		watermark='twitter_autobase/watermark/photo.png',
		font='twitter_autobase/watermark/FreeMono.ttf',
		text='TESTING',
		ratio=0.15,
		pos=('right','bottom'),
		output='watermarked.jpg',
		color=(0,0,0,0),
		stroke_color=(225,225,225,1)
	)	
	assert exists('watermarked.jpg')
