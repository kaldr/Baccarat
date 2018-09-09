from PIL import Image
import pytesseract
import os


def cv_folder():
    rooter = './CV/assets'
    plist = os.listdir('./CV/assets')
    for i in plist:
        path = os.path.join(rooter, i)
        print("===================================")
        print(path)
        if os.path.isfile(path):
            ext = os.path.splitext(path)[1]
            if ext.lower() in ['.jpg', '.png', '.jpeg', '.gif', '.bmp']:
                text = pytesseract.image_to_string(Image.open(path), lang='chi_sim', config="psm 15")
                print(text)


text = pytesseract.image_to_string(Image.open('./CV/assets/g.png'), lang='chi_sim', config="psm 15")
print(text)




