from Crypto.Cipher import AES
import cv2
import random
from PIL import Image
import math

key= b'1234567890123456'
dh_key= b'1234567890123456'
iv= b'1234567890123456'
file_name ="./lena256.ppm"

message = 'je suis super secret'


#IMPORTANT : both these functions start at 0 index !
def flip_bit(byte,bit):
    byte = byte ^ (pow(2,bit))
    return byte

def set_bit0(byte,bit):
    tmp=get_bit(byte,bit)
    if tmp==1:
        byte=flip_bit(byte,bit)
    return byte

def set_bit1(byte,bit):
    tmp=get_bit(byte,bit)
    if tmp==0:
        byte=flip_bit(byte,bit)
    return byte
        

def get_bit(byte, bit):
        return (int)((byte >> bit) & 1)
        
def print_bit(byte, bit):
        print((byte >> bit) & 1)

def print_byte(byte):
    for i in range(8):
        print( (byte >> i) & 1)
    print("----------------------")

'''test=255
print_byte(test)
test = flip_bit(test,1)
print_byte(test)
get_bit(test,1)'''

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
    image.save(filename_out[:-4]+'_readable.bmp')
	
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


            
def hide_message(filename_in,filename_out):
    input_file = open(filename_in, 'rb')
    input_data = input_file.read()
    input_file.close()

    generator = random.Random()
    generator.seed(dh_key)
    data_size = len(input_data)
    #mess=bytearray(message,'utf8')
    data=bytearray(input_data)
    #start at 5 to not touch ppm header ?
    for i in range(16,data_size//16):
        #flip one bit within one of 16 bytes, making it a change within a 128 bit block
        #for now we are just setting every modified bit to 1. Need a new function to change a bit with a message bit
        rand16=(int)(generator.randrange(16))
        tmp_byte = data[16*i + rand16]
        tmp_byte = set_bit1(tmp_byte,generator.randrange(8))
        data[16*i + rand16]=tmp_byte
    
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
    for i in range(16,data_size//16):
        #read one bit within one of 16 bytes, making it a change within a 128 bit block
        tmp_byte = data[16*i + generator.randrange(16)]
        #tmp_byte = print_bit(tmp_byte,generator.randrange(8))
        
    
    #old version here
    '''data=bytearray(input_data)
    for i in range(0,data_size//128):
        print(data[128*i + generator.randrange(128)])'''
    
    
def remove_message_and_decrypt(filename_in,filename_out):
    global key,iv,entry_for_folder
   
    input_file = open(filename_in, 'rb')
    input_data = input_file.read()
    input_file.close()

    #first, decrypt the data for 2 versions : one with the modified bit at 0 everytime, and the other with 1
    generator = random.Random()
    generator.seed(dh_key)
    data_size = len(input_data)
    
    data=bytearray(input_data)
    
    end_data = data.copy()
    
    data1=data.copy()
    data0=data.copy()
    
    #WARNING : this part! how to "fix" the value here ?
    for i in range(16,data_size//16):
        rand16=(int)(generator.randrange(16))
        rand8=(int)(generator.randrange(8))
        tmp_byte1 = data1[16*i + rand16]
        tmp_byte1 = set_bit1(tmp_byte1,rand8)
        data1[16*i + rand16] = tmp_byte1
        tmp_byte0 = data0[16*i + rand16]
        tmp_byte0 = set_bit0(tmp_byte0,rand8)
        data0[16*i + rand16] = tmp_byte0
    
    cfb_decipher = AES.new(key, AES.MODE_CFB,iv)
    plain_data1 = (cfb_decipher.decrypt(data1))
    plain_data0 = (cfb_decipher.decrypt(data0))
    
    #then compute the dtandard deviations per block of each decrypted data
    for i in range(0,data_size//16):
        avg1=0
        sd1=0
        avg0=0
        sd0=0
        #compute local average first
        for j in range(0,16):
            avg1+=plain_data1[16*i+j]
            avg0+=plain_data0[16*i+j]
        #then compute standard deviation
        for j in range(0,16):
            sd1+=pow(plain_data1[16*i+j]-avg1,2)
            sd0+=pow(plain_data0[16*i+j]-avg0,2)
        sd1 = math.sqrt(sd1/16)
        sd0 = math.sqrt(sd0/16)
        #finally, choose each block with the lowest standard deviation
        if(sd0<sd1):
            end_data[i*16:(i+1)*16] = plain_data0[i*16:(i+1)*16]
        else:
            end_data[i*16:(i+1)*16] = plain_data1[i*16:(i+1)*16]

    
    #tests with PIL to save images
    #imgBase = cv2.imread(filename_in)             
    #H = imgBase.shape[0]          # W=H, such that everything fits in
    #W = imgBase.shape[1]
    
    end=bytes(plain_data0)
    image = Image.frombytes('RGB', (512, 512), end)         # create image
    image.save(filename_out[:-4]+'_TESTDEC.bmp')


    dec_file = open(filename_out, "wb")
    dec_file.write(data)
    dec_file.close()


 
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
remove_message_and_decrypt(file_name[:2]+'hid'+file_name[2:],file_name[:2]+'REMOVED'+file_name[2:])
#save_file(file_name[:2]+'dec'+file_name[2:])
print("decryption complete")
