import cv2
from Crypto.Cipher import AES
from Crypto import Random
from PIL import Image
import PIL


img = cv2.imread('TurtleD.tif')




##crypt image
iv_AES = Random.new().read(AES.block_size)
key_AES = 'abcdefghijklmnop'.encode("utf8")


aese = AES.new(key_AES, AES.MODE_CFB, iv_AES)
aesd = AES.new(key_AES, AES.MODE_CFB, iv_AES)


input_file = open('TurtleD.tif', 'rb')
input_data = input_file.read()
input_file.close()

imgC = aese.encrypt(input_data)


#then treat encrypted data as a bitmap
# calculate sizes
num_bytes = len(imgC)
num_pixels = int((num_bytes+2)/3)                     # 3 bytes per pixel
H = img.shape[0]          # W=H, such that everything fits in
W = img.shape[1]

# fill the image with zeros, because probably len(imagedata) < needed W*H*3
#imagedata = imgC + '\0' * (W*H*3 - len(imgC))

image = Image.frombytes('RGB', (W, H), imgC)         # create image
image.save('image.bmp')  

#now decrypt
output_file = open('image.bmp', 'rb')
output_data = output_file.read()
output_file.close()

imgD = aesd.decrypt(output_data)

num_bytes = len(imgD)
num_pixels = int((num_bytes+2)/3)                     # 3 bytes per pixel
H = img.shape[0]          # W=H, such that everything fits in
W = img.shape[1]

# fill the image with zeros, because probably len(imagedata) < needed W*H*3
#imagedata = imgC + '\0' * (W*H*3 - len(imgC))

imageD = Image.frombytes('RGB', (W, H), imgD)         # create image
imageD.save('recreated.bmp')  


# save to a file

'''
cv2.namedWindow('imgC',cv2.WINDOW_NORMAL) # Can be resized
cv2.namedWindow('img',cv2.WINDOW_NORMAL) # Can be resized

cv2.imshow('img',img)
cv2.imshow('imgC',imgC)

cv2.waitKey(0)
'''