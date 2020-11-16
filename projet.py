from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import io
import os
import cv2
from PIL import Image
import random
import io
import binascii

key= b'1234567890123456'
iv= b'1234567890123456'
file_name ="./lena256.ppm"


#Encrypting Image
def encrypt_image():
    global key,iv,file_name
    
    input_file = open(file_name,"rb")
    input_data = input_file.read()
    input_file.close()  
    
    
    print(len(input_data))
    
    cfb_cipher = AES.new(key, AES.MODE_ECB)
    enc_data = cfb_cipher.encrypt(pad(input_data,16))
    
    print(len(enc_data))
    
    #then add hidden data
    data_size = len(input_data)
    nTest = data_size/128
    random.seed(key);
    #substitution ?
    '''for i in range((int)(nTest)):
        bloc = input_data[i*128:(i+1)*128]
        n = (int)(16*random.random())
        bloc[n]=bloc[n]^1'''
        
    
    #write encrypted image in file
    '''imgBase = cv2.imread(file_name)              
    H = imgBase.shape[0]          # W=H, such that everything fits in
    W = imgBase.shape[1]
    img = Image.frombytes('RGB', (W, H), (enc_data))
    img.save((file_name[:-4])+'enc.bmp')'''
    
    
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

    cfb_decipher = AES.new(key, AES.MODE_ECB)
    plain_data = (cfb_decipher.decrypt(enc_data2))
    
    #plain_data = unpad(plain_data,16)

    dec_file = open((file_name[:-4])+'dec.jpg', "wb")
    dec_file.write(plain_data)
    dec_file.close()

def save_enc_file(filename):
    
    input_file = open(filename+'.enc', 'rb')
    input_data = input_file.read()
    input_file.close()
     
   #write encrypted image in file
    imgBase = cv2.imread(filename)              
    H = imgBase.shape[0]          # W=H, such that everything fits in
    W = imgBase.shape[1]
    img = Image.frombytes('RGB', (W, H), (input_data))
    img.save((file_name[:-4])+'enc.bmp')
    

                
    
    
encrypt_image();
decrypt_image();
#save_enc_file(file_name)