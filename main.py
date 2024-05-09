import cv2
import cvzone
import pickle
import numpy as np

# Video feed
cap = cv2.VideoCapture('carPark.mp4')

with open('car_park_pos', 'rb') as f:
    pos_list = pickle.load(f)

width, height = 107, 48


def check_parking_space(processed_img):

    space_counter = 0

    for pos in pos_list:
        x, y = pos

        img_crop = processed_img[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), img_crop)
        count = cv2.countNonZero(img_crop)

        #900 is the threshold for number of pixels
        #if count is less than threshold, space is free, if greater, there is a car/obstruction
        if count < 900:
            color = (0, 255, 0) #green
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255) #red
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
        #                    thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Free: {space_counter}/{len(pos_list)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
while True:

    #looping the given video for testing
    #ideally this will be connected to a live video stream
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    #get image from capture
    success, img = cap.read()
    #grayscale and blur it
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    #convert into binary image (each pixel is marked black/white based on pixel intensity threshold)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    #reduce salt&pepper noise
    img_median = cv2.medianBlur(img_threshold, 5)
    #use a kernel and dilate to accentuate white pixels for better visibility
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    #call check function
    check_parking_space(img_dilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    cv2.waitKey(10)
