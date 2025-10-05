import easyocr
import streamlit as st
from streamlit_push_notifications import send_alert
from PIL import Image, ImageEnhance,  ImageOps, ImageDraw
import numpy as np
from lang import languages

upload = None
language = ['en']
reader = easyocr.Reader(language, gpu = False) # needs to run once

if 'result' not in st.session_state:
    st.session_state.result = 'Text...'
if 'cropimage' not in st.session_state:
    st.session_state.cropimage = None

def detect():
    try: # maybe because of None type
        image = Image.open(upload)
        image1 = ImageEnhance.Brightness(image)
        image1 = image1.enhance(1.3) 
        sharpner = ImageEnhance.Sharpness(image1)
        image1 = sharpner.enhance(3)
        image1 = ImageOps.grayscale(image1)

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

        image1 = image1.crop((keyxMin, keyyMin, keyxMax, keyyMax))
            
        print('crop boundry (top left and bottom right):', (keyxMin, keyyMin), (keyxMax, keyyMax))
        image2 = image1.copy()
        draw = ImageDraw.Draw(image2)
        for coord in [i for (i,x,b) in reader.readtext(upload.getvalue())]:
            draw.rectangle(((int(coord[0][0]) - keyxMin, int(coord[0][1]) - keyyMin), (int(coord[-2][0]) - keyxMin, int(coord[-2][1]) - keyyMin)), outline = 50, width = 2) 
            print((int(coord[0][0]), int(coord[0][1])), (int(coord[-1][0]), int(coord[-1][1])))

        st.session_state.cropimage = image2

        #
        st.session_state.result = '\n'.join(reader.readtext(np.array(image1), detail = 0))

    except Exception as error: print(error)

st.title('Image to Text')
language1 = st.multiselect('Language(s) to be read from image', languages.keys(), default = ['English'])
if language != list(map(lambda x: languages[x], language1)):
    language = list(map(lambda x: languages[x], language1))
    reader = easyocr.Reader(language, gpu = False) # needs to run once

upload = st.file_uploader("Image to be read", type = ['png', 'jpeg', 'jpg'])

if upload != None:
    st.image(upload, caption = 'Uploaded Image') 
    if language != []: detect()
    else: st.warning('Please select a language to detect from the image'); send_alert('Please select a language to detect from the image')
if st.session_state.cropimage != None and language != []: st.image(st.session_state.cropimage, caption = 'edited Image')

resultBox = st.text_area('Text from image', placeholder = st.session_state.result, disabled = True, key = 'result')



# print('\n'.join(result))



# import keras_ocr # need numpy==1.26 ! check how to implement only in this folder to not cause other issues
# pipeline = keras_ocr.pipeline.Pipeline()
# pipeline.recognize(['test.png'])




# make sure to put text saying that they must put the right langauge to detect corrctly
# ? give streamlit front end option to change modules (pytesseract, ocr, kerus ocr) to see different results
# *TODO: give option change language too (find out how to include all languages and then impliment in the form that each lirbary like pytesseract requries)
# *TODO: look at other paramters for easyocr's read text function to give more changability for hte usaer in stremalit like how confident the model must be to show as text
# *TODO: for output, give text and iamge showing detection too
# *TODO: also give an option to use camera using open Cv to dertect in real time using easy ocr (check easyocr documentation to help)
# *TODO: add option to add multiple iagmes and maybe in output seperate the results of each img
# ? maybe try to impliment pytesseract/tesseract too as it is better for documents
# *TODO: do streamlit shjaring thing (on their website): https://docs.streamlit.io/get-started/tutorials/create-an-app - at bottom
# *TODO: make it so thjat when they remove the iamge, the image display and text go to normal or get rmeoved
# *TODO: make it so that when removing the thing (as it still counts as a change) it won't refresh and detect again calling the detect function (maybe just change dtect instread of not calling it)
# *TODO: when refrresh, and file goes away, text needs to reset too
# fix that if removing image then it shoudl remove edited iamge too and also when person didn't pick language
# also when don't pick language remvoe the result text too (and do this for other times too - think when -)
# make cookie type memroy thing
#make it so that program is contrrlled by button so that person can add many lagnagues (do manychanges) and then click detect to see the result isntead of the program constantly running after each small change

#DONE
# * crop, icnrease  brightness and clairty and turn into balck and white (opencv) or l-25+1 something with numpy as image is numpy array