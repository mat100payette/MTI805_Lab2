# import the necessary packages
import numpy as np
import imutils
import cv2


class Stitcher:
    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        (image2, image1) = images
        (kps1, features1) = self.detectAndDescribe(image1)
        (kps2, features2) = self.detectAndDescribe(image2)

        M = self.matchKeypoints(kps1, kps2,
                                features1, features2, ratio, reprojThresh)
        if M is None:
            return None

        (matches, H, status) = M
        result = cv2.warpPerspective(image1, H,
                                     (image1.shape[1] + image2.shape[1], image1.shape[0]))
        result[0:image2.shape[0], 0:image2.shape[1]] = image2

        return result

    def detectAndDescribe(self, image):
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)

        kps = np.float32([kp.pt for kp in kps])

        return (kps, features)

    def matchKeypoints(self, kps1, kps2, features1, features2,
                       ratio, reprojThresh):

        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(features1, features2, 2)
        matches = []


        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 4:
            pts1 = np.float32([kps1[i] for (_, i) in matches])
            pts2 = np.float32([kps2[i] for (i, _) in matches])

            (H, status) = cv2.findHomography(pts1, pts2, cv2.RANSAC,
                                             reprojThresh)

            return (matches, H, status)

        return None


#image1 = cv2.imread("C:/Users/AlexGP/Desktop/hotel-01.png")
#image2 = cv2.imread("C:/Users/AlexGP/Desktop/hotel-00.png")

image1 = cv2.imread("C:/Users/AlexGP/Desktop/Boat/boat1.jpg")
image2 = cv2.imread("C:/Users/AlexGP/Desktop/Boat/boat2.jpg")
image1 = imutils.resize(image1, width=600)
image2 = imutils.resize(image2, width=600)

stitcher = Stitcher()
result = stitcher.stitch([image1, image2], showMatches=True)

cv2.imshow("Image 1", image1)
cv2.imshow("Image 2", image2)
cv2.imshow("Panorama", result)
cv2.waitKey(0)
