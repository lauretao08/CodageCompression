from Crypto.Cipher import AES
import cv2
import random
from PIL import Image

key= b'1234567890123456'
dh_key= b'1234567890123456'
iv= b'1234567890123456'
file_name ="./lena256.ppm"

message = 'je suis super secret'


#Encrypting Image
def encrypt_image(filename_in,filename_out):
    global key,iv
    
    input_file = open(filename_in,"rb")
    input_data = input_file.read()
    input_file.close()
    
    cfb_cipher = AES.new(key, AES.MODE_CFB,iv)
    enc_data = cfb_cipher.encrypt(input_data)
    
    enc_file = open(filename_out, "wb")
    enc_file.write(enc_data)
    enc_file.close()
    
    #and save a visible bitmap of the encrypted image
    imgBase = cv2.imread(filename_in)             
    H = imgBase.shape[0]          # W=H, such that everything fits in
    W = imgBase.shape[1]
    
    image = Image.frombytes('RGB', (W, H), enc_data)         # create image
    image.save(filename_out[:-4]+'enc_readable.bmp')
	
    #img = cv2.imread(file_name)
    #cv2.namedWindow('img',cv2.WINDOW_NORMAL) # Can be resized
    #cv2.imshow('img',img)
    #cv2.waitKey(0)
    
    
def decrypt_image(filename_in,filename_out):
    global key,iv,entry_for_folder
   
    enc_file2 = open(filename_in,"rb")
    enc_data2 = enc_file2.read()
    enc_file2.close()

    cfb_decipher = AES.new(key, AES.MODE_CFB,iv)
    plain_data = (cfb_decipher.decrypt(enc_data2))

    dec_file = open(filename_out, "wb")
    dec_file.write(plain_data)
    dec_file.close()

def save_file(filename):
    
    input_file = open(filename, 'rb')
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
    image.save(filename+'.bmp')  
              
def hide_message(filename_in,filename_out):
    input_file = open(filename_in, 'rb')
    input_data = input_file.read()
    input_file.close()

    generator = random.Random()
    generator.seed(dh_key)
    data_size = len(input_data)
    #mess=bytearray(message,'utf8')
    data=bytearray(input_data)
    for i in range(0,data_size//128):
        data[128*i + generator.randrange(128)]=i%2
    
    hid_file = open(filename_out, "wb")
    hid_file.write(data)
    hid_file.close()
    
def find_message(filename_in):
    input_file = open(filename_in, 'rb')
    input_data = input_file.read()
    input_file.close()

    mess=bytes(message,'utf8')
    
    generator = random.Random()
    generator.seed(dh_key)
    data_size = len(input_data)
    
    data=bytearray(input_data)
    for i in range(0,data_size//128):
        print(data[128*i + generator.randrange(128)])
    
    
#save_file(file_name)
encrypt_image(file_name,file_name[:2]+'enc'+file_name[2:])
#save_file(file_name[:2]+'enc'+file_name[2:])
print("encryption complete")
hide_message(file_name[:2]+'enc'+file_name[2:],file_name[:2]+'hid'+file_name[2:])
#save_file(file_name[:2]+'hid'+file_name[2:])
print("DH complete")

find_message(file_name[:2]+'hid'+file_name[2:])
print("Data recuperation complete")

decrypt_image(file_name[:2]+'hid'+file_name[2:],file_name[:2]+'dec'+file_name[2:])
#save_file(file_name[:2]+'dec'+file_name[2:])
print("decryption complete")
