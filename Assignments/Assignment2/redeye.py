import cv2
import numpy as np

def redeye(path):
    print "executing red eye correction"

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

    input = cv2.imread(path)
    img = input.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            
            ex = x + ex + int(ew/4);
            ey = y + ey + int(eh/4);
            ew = int(ew/2);
            eh = int(eh/2);
            gray = cv2.cvtColor(img[ey:ey+eh, ex:ex+ew , :], cv2.COLOR_BGR2GRAY)
            gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
            kernel = np.ones((3,3), np.uint8)
            gray = cv2.erode(gray,kernel,iterations = 6)
            gray = cv2.dilate(gray,kernel,iterations = 3)
            circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2, 50, param1=30, param2=45, minRadius=0, maxRadius=0)

            if circles is not None:
                print "found eyes"
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:

                    padding = 50
                    r = r + padding

                    cw = 2*r
                    ch = 2*r
                    cx = ex + x -  r
                    cy = ey + y -  r
                    print(x,y,r)
                    condition = img[cy:cy+ch, cx:cx+cw , 2] > np.maximum((0.8*img[cy:cy+ch, cx:cx+cw , 0] + 0.8*img[cy:cy+ch, cx:cx+cw,1]),80)
                    # condition = img[cy:cy+ch, cx:cx+cw , 2] > np.maximum(img[cy:cy+ch, cx:cx+cw , 0] + img[cy:cy+ch, cx:cx+cw , 1],100)
                    # if condition is not None:
                    condition = condition.astype(np.uint8)*255
                    # condition = cv2.dilate(condition, None, anchor=(-1, -1), iterations=3, borderType=1, borderValue=1)
                    condition = condition.astype(bool)
                    condition = np.repeat(condition[:, :, np.newaxis], 3, axis=2)

                    val = (0.5*img[cy:cy+ch, cx:cx+cw , 0] + 0.5*img[cy:cy+ch, cx:cx+cw , 1]).copy()
                    val = val.astype(np.uint8)
                    val = np.repeat(val[:, :, np.newaxis], 3, axis=2)

                    print val.shape
                    print condition.shape

                    np.copyto(img[cy:cy+ch, cx:cx+cw , :], val ,where=condition)
                    # img[cy:cy+ch, cx:cx+cw , :][condition] = 0


            else:
                condition = img[ey:ey+eh, ex:ex+ew , 2] > np.maximum((0.8*img[ey:ey+eh, ex:ex+ew , 0] + 0.8*img[ey:ey+eh, ex:ex+ew,1]),100)
                # condition = img[ey:ey+eh, ex:ex+ew , 2] > np.maximum(img[ey:ey+eh, ex:ex+ew , 0] + img[ey:ey+eh, ex:ex+ew , 1],150)
                condition = condition.astype(np.uint8)*255
                condition = cv2.dilate(condition, None, anchor=(-1, -1), iterations=3, borderType=1, borderValue=1)
                condition = condition.astype(bool)
                condition = np.repeat(condition[:, :, np.newaxis], 3, axis=2)

                val = (0.5*img[ey:ey+eh, ex:ex+ew , 0] + 0.5*img[ey:ey+eh, ex:ex+ew , 1]).copy()
                val = val.astype(np.uint8)
                val = np.repeat(val[:, :, np.newaxis], 3, axis=2)

                print val.shape
                print condition.shape
                # print img[ey:ey+eh, ex:ex+ew , :][condition[:, :, np.newaxis]].shape
                np.copyto(img[ey:ey+eh, ex:ex+ew , :], val ,where=condition)
                # img[ey:ey+eh, ex:ex+ew , :][condition] = 0


    if(faces == ()):
        eyes = eye_cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=4)
        roi_color = img
        for (ex,ey,ew,eh) in eyes:
            # cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            gray = cv2.cvtColor(img[ey:ey+eh, ex:ex+ew , :], cv2.COLOR_BGR2GRAY)
            gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
            kernel = np.ones((3,3), np.uint8)
            gray = cv2.erode(gray,kernel,iterations = 6)
            gray = cv2.dilate(gray,kernel,iterations = 3)
            circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 2, 50, param1=30, param2=45, minRadius=0, maxRadius=10)

            if circles is not None:
                print "found eyes"
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:

                    padding = 50
                    r = r + padding

                    cw = 2*r
                    ch = 2*r
                    cx = x -  r
                    cy = y -  r
                    print(x,y,r)
                    condition = img[cy:cy+ch, cx:cx+cw , 2] > np.maximum((0.8*img[cy:cy+ch, cx:cx+cw , 0] + 0.8*img[cy:cy+ch, cx:cx+cw,1]),80)
                    # condition = img[cy:cy+ch, cx:cx+cw , 2] > np.maximum(img[cy:cy+ch, cx:cx+cw , 0] + img[cy:cy+ch, cx:cx+cw , 1],100)
                    # if condition is not None:
                    condition = condition.astype(np.uint8)*255
                    # condition = cv2.dilate(condition, None, anchor=(-1, -1), iterations=3, borderType=1, borderValue=1)
                    condition = condition.astype(bool)
                    condition = np.repeat(condition[:, :, np.newaxis], 3, axis=2)

                    val = (0.5*img[cy:cy+ch, cx:cx+cw , 0] + 0.5*img[cy:cy+ch, cx:cx+cw , 1]).copy()
                    val = val.astype(np.uint8)
                    val = np.repeat(val[:, :, np.newaxis], 3, axis=2)

                    print val.shape
                    print condition.shape

                    np.copyto(img[cy:cy+ch, cx:cx+cw , :], val ,where=condition)
                    # img[cy:cy+ch, cx:cx+cw , :][condition] = 0


            else:
                ex = ex + int(ew/4);
                ey = ey + int(eh/4);
                ew = int(ew/2);
                eh = int(eh/2);
                condition = img[ey:ey+eh, ex:ex+ew , 2] > np.maximum((0.8*img[ey:ey+eh, ex:ex+ew , 0] + 0.8*img[ey:ey+eh, ex:ex+ew,1]),100)
                # condition = img[ey:ey+eh, ex:ex+ew , 2] > np.maximum(img[ey:ey+eh, ex:ex+ew , 0] + img[ey:ey+eh, ex:ex+ew , 1],150)
                condition = condition.astype(np.uint8)*255
                condition = cv2.dilate(condition, None, anchor=(-1, -1), iterations=3, borderType=1, borderValue=1)
                condition = condition.astype(bool)
                condition = np.repeat(condition[:, :, np.newaxis], 3, axis=2)

                val = (0.5*img[ey:ey+eh, ex:ex+ew , 0] + 0.5*img[ey:ey+eh, ex:ex+ew , 1]).copy()
                val = val.astype(np.uint8)
                val = np.repeat(val[:, :, np.newaxis], 3, axis=2)

                print val.shape
                print condition.shape
                # print img[ey:ey+eh, ex:ex+ew , :][condition[:, :, np.newaxis]].shape
                np.copyto(img[ey:ey+eh, ex:ex+ew , :], val ,where=condition)
                # img[ey:ey+eh, ex:ex+ew , :][condition] = 0

    return input,img

    # if(len(sys.argv[-1]) > 0):
    #     img = cv2.imread(str(sys.argv[-1]))
    #     print str(sys.argv[-1])
    # else:
        # img  = cv2.imread('red_2.jpg')
