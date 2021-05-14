from PIL import Image, ImageDraw

def image_resize(img, h_new):
	w, h = img.size
	w_new = int(w * h_new / h)
	return img.resize((w_new, h_new))


def get_square_image(img):
	width, height = img.size
	mx = max(width, height)
	bg = Image.new(img.mode, (mx, mx), (255, 255, 255))
	if width == height:
		return img
	elif width > height:
		bg.paste(img, (0, (width - height) // 2))
	else:
		bg.paste(img, ((height - width) // 2, 0))
	return bg

def get_circle_image(img):
	mask = Image.new("L", img.size, 255)
	draw = ImageDraw.Draw(mask)
	draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)
	result = img.copy()
	result.putalpha(mask)
	return result