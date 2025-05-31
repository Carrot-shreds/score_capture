from image_process import gama_transfer
from main import *

def detect_images(path):
    # path = r"E:\dev_Code\Python\score_capture\output\untitled34"
    # path = r"E:\dev_Code\Python\score_capture\output\untitled320"
    for i in os.listdir(path):
        if i.rfind("detected")>=0:
            os.remove(os.path.join(path, i))
            continue
        if i.rfind("image")>=0:
            image_path = path+"\\"+i
            image = read_image(image_path)
            image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            print(image_path)
            horizontal_lines = detect_horizontal_lines(image_gray)
            vertical_lines = detect_vertical_lines(image_gray, horizontal_lines)
            for l in horizontal_lines:
                l.draw(image)
            for l in vertical_lines:
                l.draw(image)
            save_image(path+"\\"+i.split(".")[0]+"-detected"+"."+i.split(".")[1], image)

def detect_image(file):
    img = read_image(file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    horizontal_lines = detect_horizontal_lines(img_gray)
    print(len(horizontal_lines))
    vertical_lines = detect_vertical_lines(img_gray, horizontal_lines)
    for l in horizontal_lines:
        l.draw(img)
    for l in vertical_lines:
        l.draw(img)
    save_image(file.split(".")[0]+"-detected"+"."+file.split(".")[1], img)
    return vertical_lines

def stitch_image(path, img1, img2):
    path = path
    img1 = read_image(os.path.join(path, img1), "GRAY")
    img2 = read_image(os.path.join(path, img2), "GRAY")

    mse = [np.average(np.square(img1[:, -offset:] - img2[:, :offset])) for offset in range(img1.shape[1])]
    return mse