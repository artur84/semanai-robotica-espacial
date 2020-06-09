import cv2
import numpy as np

img = cv2.imread('/home/artur/catkin_ws/src/semanai-robotica-espacial/img/stop.jpeg', cv2.IMREAD_GRAYSCALE)  # queryiamge
right = cv2.imread('/home/artur/catkin_ws/src/semanai-robotica-espacial/img/right.jpeg', cv2.IMREAD_GRAYSCALE)  
cap = cv2.VideoCapture(0)
# Features
sift = cv2.xfeatures2d.SIFT_create()
kp_image, desc_image = sift.detectAndCompute(img, None)
kp_right, desc_right = sift.detectAndCompute(right, None)
# Feature matching
index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)

stop = False 
right = False


print index_params
while True:
    _, frame = cap.read()
    grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # trainimage
    kp_grayframe, desc_grayframe = sift.detectAndCompute(grayframe, None)
    matches = flann.knnMatch(desc_image, desc_grayframe, k=2)
    matches_r = flann.knnMatch(desc_right, desc_grayframe, k=2)
    good_points = []
    good_points_r = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good_points.append(m)
    #img3 = cv2.drawMatches(img, kp_image, grayframe, kp_grayframe, good_points, grayframe)

    for m, n in matches_r:
        if m.distance < 0.6 * n.distance:
            good_points_r.append(m)
    #img4 = cv2.drawMatches(right, kp_right, grayframe, kp_grayframe, good_points_r, grayframe)
    # Homography
    if len(good_points) > 10:
        query_pts = np.float32([kp_image[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
        train_pts = np.float32([kp_grayframe[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)
        matches_mask = mask.ravel().tolist()
        #print "matrix"
        #print matrix
        #print "end"
        # Perspective transform
        h, w = img.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        #print pts
        dst = cv2.perspectiveTransform(pts, matrix)
        #print dst
        homography = cv2.polylines(frame, [np.int32(dst)], True, (255, 0, 0), 3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        print type(dst)
        print "-------"
        print np.int32(dst).shape
        print "-------"
        stop = True

        cv2.putText(homography,'Stop',(10,250), font, 1,(255,255,255),2)

        cv2.imshow("Homography", homography)

    elif len(good_points_r) > 10:
        query_pts_r = np.float32([kp_right[m.queryIdx].pt for m in good_points_r]).reshape(-1, 1, 2)
        train_pts_r = np.float32([kp_grayframe[m.trainIdx].pt for m in good_points_r]).reshape(-1, 1, 2)
        matrix_r, mask_r = cv2.findHomography(query_pts_r, train_pts_r, cv2.RANSAC, 5.0)
        matches_mask_r = mask_r.ravel().tolist()
        #print "matrix"
        #print matrix
        #print "end"
        # Perspective transform
        h_r, w_r = img.shape
        pts_r = np.float32([[0, 0], [0, h_r-1], [w_r-1, h_r-1], [w_r-1, 0]]).reshape(-1, 1, 2)
        #print pts
        dst_r = cv2.perspectiveTransform(pts_r, matrix_r)
        #print dst
        homography_r = cv2.polylines(frame, [np.int32(dst_r)], True, (255, 0, 0), 3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        print type(dst_r)
        print "-------"
        print np.int32(dst_r).shape
        print "-------"
        right = True

        cv2.putText(homography_r,'Right',(10,250), font, 1,(255,255,255),2)

        cv2.imshow("Homography", homography_r)

    else:
        stop = False
        right = False
        cv2.imshow("Homography", grayframe)
    # cv2.imshow("Image", img)
    # cv2.imshow("grayFrame", grayframe)
    # cv2.imshow("img3", img3)
    print "Stop: " + str(stop)
    print "Right: " + str(right)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
