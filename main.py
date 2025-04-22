import easyocr
import streamlit as st
from PIL import Image, ImageEnhance,  ImageOps
import numpy as np

upload = None
reader = easyocr.Reader(['en'], gpu = True) # needs to run once

if 'result' not in st.session_state:
    st.session_state.result = 'Text...'
if 'cropimage' not in st.session_state:
    st.session_state.cropimage = None

def detect(): # ! deson't work when upload iamge for first time but does after uplaoding same one again NEED TO FIX
    try: # maybe because of None type
        keyxMin = 1000000
        keyxMax = 0
        keyyMin = 1000000
        keyyMax = 0
        for coord in [i for (i,x,b) in reader.readtext(upload.getvalue())]:
            for c in coord:
                keyxMin = min(keyxMin, c[0])
                keyxMax = max(keyxMax, c[0])
                keyyMin = min(keyyMin, c[1])
                keyyMax = max(keyyMax, c[1])
        print('crop boundry (top left and bottom right):', (keyxMin, keyyMin), (keyxMax, keyyMax))
        image = Image.open(upload)
        image1 = ImageEnhance.Brightness(image)
        image1 = image1.enhance(1.3) 
        sharpner = ImageEnhance.Sharpness(image1)
        image1 = sharpner.enhance(3)
        image1 = ImageOps.grayscale(image1)
        st.session_state.cropimage = image1.crop((keyxMin, keyyMin, keyxMax, keyyMax))

        #
        st.session_state.result = '\n'.join(reader.readtext(np.array(st.session_state.cropimage), detail = 0))

    except Exception as error: print(error)

st.title('Image to Text')
upload = st.file_uploader("Image to be read", type = ['png', 'jpeg', 'jpg'])

if upload != None:
    st.image(upload, caption = 'Uploaded Image') 
    detect()
if st.session_state.cropimage != None: st.image(st.session_state.cropimage, caption = 'edited Image')

resultBox = st.text_area('Text from image', placeholder = st.session_state.result, disabled = True, key = 'result')