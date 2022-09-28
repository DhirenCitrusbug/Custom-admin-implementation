from PIL import Image
from io import BytesIO
from django.core.files import File


def resize_image(full_image, size):
	image_name = full_image.name
	image = Image.open(full_image)
	image = image.resize(size, Image.ANTIALIAS)

	image_io = BytesIO()
	image.save(image_io, format='png')
	new_image = File(image_io, name=image_name)
	return new_image


def resize_review_image(full_image, size):
	image_name = full_image.name
	image = Image.open(full_image)

	left = int(image.size[0]/2-1720/2)
	upper = int(image.size[1]/2-1140/2)
	right = left + 1720
	lower = upper + 1140

	# Crop the center of the image
	im_cropped = image.crop((left, upper,right,lower))
	image = im_cropped.resize(size, Image.ANTIALIAS)
	image_io = BytesIO()
	image.save(image_io, format='png')
	new_image = File(image_io, name=image_name)
	return new_image
