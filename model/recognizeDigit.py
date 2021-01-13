import numpy as np
from PIL import Image
import xlwt
import cv2
import os
#import scipy.misc as mi
from keras.models import model_from_json
from .processData import processData
from .cropDigit import getDigit1, getDigit2

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def reStoreModel():
    # load json and create model
    json_file = open('./model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("./model/model.h5")
    print("loaded model from disk")
    return loaded_model

def recognizeDigit(cnnModel, digit_location):
    digit_img = Image.open(digit_location).convert('L')
    digit_arr = np.asarray(digit_img)
    digit_arr = np.require(digit_arr, dtype='f4', requirements=['O', 'W'])
    digit_arr.setflags(write=1)
    digit_arr = cv2.resize(digit_arr, (28, 28))
    digit_arr[0] = 0
    digit_arr[1] = 0
    digit_arr[2] = 0
    for x in digit_arr:
        i = 0
        for y in x:
            if y < 30:
                x[i] = 0
            i += 1
    
    # img = np.zeros((20,20,3), np.uint8)
    # mi.imsave('test.jpg', test)
    
    digit_arr = digit_arr / 255.0
    digit_arr = digit_arr.reshape(-1,28,28,1)
    # predict results
    results = cnnModel.predict(digit_arr)
    # select the indix with the maximum probability
    accuracy  = np.amax(results,axis = 1)
    results = np.argmax(results,axis = 1)
    ketqua = [results[0], accuracy[0]]
    # results = pd.Series(result,name="Label")

    return ketqua

def run():
    print("--> running")
    model = reStoreModel()
    
    inputdir = "./input"
    outputdir = "./output1"
    filelist = os.listdir(inputdir)
    
    for name in filelist:
        book = xlwt.Workbook()
        sh = book.add_sheet("Sheet 1")
        sh.write(0, 0, 'STT')
        sh.write(0, 1, 'Diem')
        sh.write(0, 2, 'Do chinh xac')
        sh.write(0, 3, 'Check?')
        stt = 1
        print("processing " + name)
        direction = './input/' + name
        output_filename = name + "_result.xls"
        digit_name = name
        # Start recognize digit
        input_img = Image.open(direction).convert('L')
        # Process input data
        coordinates = processData(direction)
        
        # check empty case
        for x in coordinates:               
            img = input_img.crop(x)
            check = np.asarray(img)
            check = np.require(check, dtype='f4', requirements=['O', 'W'])
            check.setflags(write=1)
            for x in check:
                i = 0
                for y in x:
                    t = 255 - y
                    x[i] = t
                    i += 1
            for x in check:
                i = 0
                for y in x:
                    if y < 40:
                        x[i] = 0
                    i += 1
            for x in check.T:
                check_weigh = len(x)
                break
            i = 0
            j = 0
            k = False
            for x in check:
                if i == int(check_weigh/2):
                    for y in x:
                        if j < 10 or j > len(x) - 10:
                            j += 1
                            continue
                        if y == 0:
                            k = False
                        else: 
                            k = True
                            break
                        j += 1
                i += 1
            if k == False:
                digit1 = [0, 1.0]
                digit2 = [0, 1.0]
            else:
                # get and recognize digit
                getDigit1(img, digit_name, stt)
                getDigit2(img, digit_name, stt)
                digit1_location = './model/temp/digit1.jpg'
                digit2_location = './model/temp/digit2.jpg'
                digit1 = recognizeDigit(model, digit1_location)
                digit2 = recognizeDigit(model, digit2_location)
                if digit2[0] != 5:
                    digit2[0] = 0
            sh.write(stt, 0, stt)
            sh.write(stt, 1, str(str(digit1[0]) + ',' + str(digit2[0])))
            sh.write(stt, 2, str(round(digit1[1], 4)))
            if digit1[1] < 0.5:
                sh.write(stt, 3, 'check')
            print("Ket qua: %s,%s (%s)" %(digit1[0], digit2[0], digit1[1]))
            stt += 1
        
        output_path='./output/' + output_filename
        book.save(output_path)
    os.remove(inputdir+'/'+filelist[0])
        
