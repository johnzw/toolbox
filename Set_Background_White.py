########################################################################
# USER STORY:
# When you take a pic of your signature
# but the background is not entirely white
# you can "python Set_Background_White YOUR_SIGNATURE_FILE" to turn the background white
# GIVEN that your signature is somewhat black or dark color
########################################################################


import sys
from PIL import Image

# ORIGINAL_IMAGE_NAME is the original image file
ORIGINAL_IMAGE_NAME = sys.argv[1]

# # assume jpg file
original_image = Image.open(ORIGINAL_IMAGE_NAME)

# #load image to pixel
original_pix = original_image.load()

for i in range(original_image.size[0]):
	for j in range(original_image.size[1]):
		# sum of background pixel's rbg
		# NOTE: user can CUSTOMIZE this
		background_color = 200
		if original_pix[i,j][0]+original_pix[i,j][1]+original_pix[i,j][2]> background_color:
			# turn the it to white
			original_pix[i,j] = (255,255,255)

# save file
original_image.save("output_"+ORIGINAL_IMAGE_NAME)