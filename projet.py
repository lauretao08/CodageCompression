from Crypto.Cipher import AES
import io
import os
import cv2
from PIL import Image

key= b'1234567890123456'
iv= b'1234567890123456'
file_name ="./TurtleD.tif"


#Encrypting Image
def encrypt_image():
    global key,iv,file_name
    
    input_file = open(file_name,"rb")
    input_data = input_file.read()
    input_file.close()
    
    cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
    enc_data = cfb_cipher.encrypt(input_data)
    
    enc_file = open(file_name+".enc", "wb")
    enc_file.write(enc_data)
    enc_file.close()
	
    img = cv2.imread(file_name)
    cv2.namedWindow('img',cv2.WINDOW_NORMAL) # Can be resized
    cv2.imshow('img',img)
    cv2.waitKey(0)
    
    
def decrypt_image():
    global key,iv,entry_for_folder
   
    enc_file2 = open((file_name)+'.enc',"rb")
    enc_data2 = enc_file2.read()
    enc_file2.close()

    cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
    plain_data = (cfb_decipher.decrypt(enc_data2))

    dec_file = open((file_name[:-8])+'dec.jpg', "wb")
    dec_file.write(plain_data)
    dec_file.close()

def save_enc_file(filename):
    
    input_file = open(filename+".enc", 'rb')
    input_data = input_file.read()
    input_file.close()
     
    
    #then treat encrypted data as a bitmap
    # calculate sizes
    imgBase = cv2.imread(filename)              
    H = imgBase.shape[0]          # W=H, such that everything fits in
    W = imgBase.shape[1]
    
    # fill the image with zeros, because probably len(imagedata) < needed W*H*3
    #imagedata = imgC + '\0' * (W*H*3 - len(imgC))
    
    image = Image.frombytes('RGB', (W, H), input_data)         # create image
    image.save('imageC.bmp')  
                
encrypt_image();
decrypt_image();
save_enc_file(file_name)