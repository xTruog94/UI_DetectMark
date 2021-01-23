import numpy as np
import imageio
import cv2
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
class DetectCode:
    def __init__(self,input_dir,file_name):
        self.input_dir = input_dir
        self.file_name = file_name
        self.output_dir = './code_output/'
    def area_code(self):
        file_path = self.input_dir +'/'+ self.file_name
        input_img = cv2.imread(file_path)
        gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        #edges = cv2.Canny(gray,50,150,apertureSize = 3)
        #lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=40, maxLineGap=1)
        height = gray.shape[0]
        width = gray.shape[1]
        class_code = input_img[155:195, 360:538]
        output = self.output_dir + 'code_' + self.file_name
        cv2.imwrite(output, class_code)
        return 1
    def detect_code(self):
        if self.area_code():
            file_path = self.output_dir+'code_' + self.file_name
            img = cv2.imread(file_path)
            text = pytesseract.image_to_string(img)
            code = ''
            count = 0
            for character in text:
                if character==':':
                    code=text[count + 1 : count + 6]
                    break
                count += 1
            return code
        else:
            return 0

#Last output ['81933', '81933', '81924', '81924', '81925', '81925', '81927', '81927', '81936', '81936', '14.1.png', '81940', '81876', '81876', '81945', '81945', '81825', '17.2.png', '81828', '81828', '81826', '81826', '81934', '81934', '81915', '81915', '81916', '81916', '81919', '81919', '81918', '7.2.png', '8.1.png', '81922', '81921', '81924']
        