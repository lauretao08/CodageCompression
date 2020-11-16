from Crypto.Cipher import AES
import io
import os
import cv2

key= b'1234567890123456'
iv= b'1234567890123456'
file_name ="./img/lapin.jpg"


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

            
encrypt_image();
decrypt_image();