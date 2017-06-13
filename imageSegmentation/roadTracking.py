from __future__ import division

import math
import numpy
from PIL import Image
from skimage.draw import line
from scipy.linalg import block_diag
from __future__ import division

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../..'))
from imageProcessor import colorModel
from imageFilters import filters
from imageMorphology import morphology, edgeDetection

class LaneDetector:
    def __init__(self, road_horizon, prob_hough=True):
        self.prob_hough = prob_hough
        self.vote = 50
        self.roi_theta = 0.3
        self.road_horizon = road_horizon

    def houghLines(self, img):
        w, h = img.shape
        acc = []
        for i in range(h):
            rr, cc = line(0, i, w-1, h-i-1)
            acc.append(numpy.sum(img[rr, cc]))
        mi = numpy.argmax(acc)
        ret = numpy.zeros(img.shape, dtype=numpy.bool)
        rr, cc = line(0, mi, w-1, h-mi-1)
        ret[rr, cc] = True
        return ret

    def _standard_hough(self, img, init_vote):
        # Hough transform wrapper to return a list of points like PHough does
        # lines = cv2.HoughLines(img, 1, numpy.pi/180, init_vote)
        lines = self.houghLines(img)
        points = [[]]
        for l in lines:
            for rho, theta in l:
                a = numpy.cos(theta)
                b = numpy.sin(theta)
                x0 = a*rho
                y0 = b*rho
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*a)
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*a)
                points[0].append((x1, y1, x2, y2))
        return points

    def _base_distance(self, x1, y1, x2, y2, width):
        # compute the point where the give line crosses the base of the frame
        # return distance of that point from center of the frame
        if x2 == x1:
            return (width*0.5) - x1
        m = (y2-y1)/(x2-x1)
        c = y1 - m*x1
        base_cross = -c/m
        return (width*0.5) - base_cross

    def _scale_line(self, x1, y1, x2, y2, frame_height):
        # scale the farthest point of the segment to be on the drawing horizon
        if x1 == x2:
            if y1 < y2:
                y1 = self.road_horizon
                y2 = frame_height
                return x1, y1, x2, y2
            else:
                y2 = self.road_horizon
                y1 = frame_height
                return x1, y1, x2, y2
        if y1 < y2:
            m = (y1-y2)/(x1-x2)
            x1 = ((self.road_horizon-y1)/m) + x1
            y1 = self.road_horizon
            x2 = ((frame_height-y2)/m) + x2
            y2 = frame_height
        else:
            m = (y2-y1)/(x2-x1)
            x2 = ((self.road_horizon-y2)/m) + x2
            y2 = self.road_horizon
            x1 = ((frame_height-y1)/m) + x1
            y1 = frame_height
        return x1, y1, x2, y2

    def detect(self, frame):
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        colorModel.rgbToYuv(frame, frame.shape)
        colorModel.yuvToGrayscaleRgb(frame, frame.shape)

        roiy_end = frame.shape[0]
        roix_end = frame.shape[1]

        img = Image.fromarray(numpy.asarray(numpy.clip(frame, 0, 255), dtype="uint8"))
        img.show()
        roi = frame[self.road_horizon:roiy_end, 0:roix_end]
        print(roi)
        #blur = cv2.medianBlur(roi, 5)
        blur = numpy.copy(frame)
        filters.medianFilter('RGB', 0, blur, blur.shape, (5, 5))
        # contours = cv2.Canny(blur, 60, 120)

        contours = numpy.copy(blur)
        gaussianData = numpy.copy(blur)
        gaussianDeviation = 1.0 ##############################################
        gaussianFilterSize = math.floor(gaussianDeviation*3.0)
        filters.gaussianBlur('RGB', 0, gaussianData,
            gaussianData.shape, (gaussianFilterSize, gaussianFilterSize))
        edgeDetection.canny('RGB', 0, contours, contours.shape,
            gaussianData, amplifier=1.0, threshold=(60, 120))


        # if self.prob_hough:
        #     lines = cv2.HoughLinesP(contours, 1, numpy.pi/180, self.vote, minLineLength=30, maxLineGap=100)
        # else:
        lines = self._standard_hough(contours, self.vote)

        if lines is not None:
            # find nearest lines to center
            lines = lines+numpy.array([0, self.road_horizon, 0, self.road_horizon]).reshape((1, 1, 4))  # scale points from ROI coordinates to full frame coordinates
            left_bound = None
            right_bound = None
            for l in lines:
                # find the rightmost line of the left half of the frame and the leftmost line of the right half
                for x1, y1, x2, y2 in l:
                    theta = numpy.abs(numpy.arctan2((y2-y1), (x2-x1)))  # line angle WRT horizon
                    if theta > self.roi_theta:  # ignore lines with a small angle WRT horizon
                        dist = self._base_distance(x1, y1, x2, y2, frame.shape[1])
                        if left_bound is None and dist < 0:
                            left_bound = (x1, y1, x2, y2)
                            left_dist = dist
                        elif right_bound is None and dist > 0:
                            right_bound = (x1, y1, x2, y2)
                            right_dist = dist
                        elif left_bound is not None and 0 > dist > left_dist:
                            left_bound = (x1, y1, x2, y2)
                            left_dist = dist
                        elif right_bound is not None and 0 < dist < right_dist:
                            right_bound = (x1, y1, x2, y2)
                            right_dist = dist
            if left_bound is not None:
                left_bound = self._scale_line(left_bound[0], left_bound[1], left_bound[2], left_bound[3], frame.shape[0])
            if right_bound is not None:
                right_bound = self._scale_line(right_bound[0], right_bound[1], right_bound[2], right_bound[3], frame.shape[0])

            return [left_bound, right_bound]

class LaneTracker:
    def __init__(self, n_lanes, proc_noise_scale, meas_noise_scale, process_cov_parallel=0, proc_noise_type='white'):
        self.n_lanes = n_lanes
        self.meas_size = 4 * self.n_lanes
        self.state_size = self.meas_size * 2
        self.contr_size = 0

        self.kf = cv2.KalmanFilter(self.state_size, self.meas_size, self.contr_size)
        self.kf.transitionMatrix = numpy.eye(self.state_size, dtype=numpy.float32)
        self.kf.measurementMatrix = numpy.zeros((self.meas_size, self.state_size), numpy.float32)
        for i in range(self.meas_size):
            self.kf.measurementMatrix[i, i*2] = 1

        if proc_noise_type == 'white':
            block = numpy.matrix([[0.25, 0.5],
                               [0.5, 1.]], dtype=numpy.float32)
            self.kf.processNoiseCov = block_diag(*([block] * self.meas_size)) * proc_noise_scale
        if proc_noise_type == 'identity':
            self.kf.processNoiseCov = numpy.eye(self.state_size, dtype=numpy.float32) * proc_noise_scale
        for i in range(0, self.meas_size, 2):
            for j in range(1, self.n_lanes):
                self.kf.processNoiseCov[i, i+(j*8)] = process_cov_parallel
                self.kf.processNoiseCov[i+(j*8), i] = process_cov_parallel

        self.kf.measurementNoiseCov = numpy.eye(self.meas_size, dtype=numpy.float32) * meas_noise_scale

        self.kf.errorCovPre = numpy.eye(self.state_size)

        self.meas = numpy.zeros((self.meas_size, 1), numpy.float32)
        self.state = numpy.zeros((self.state_size, 1), numpy.float32)

        self.first_detected = False

    def _update_dt(self, dt):
        for i in range(0, self.state_size, 2):
            self.kf.transitionMatrix[i, i+1] = dt

    def _first_detect(self, lanes):
        for l, i in zip(lanes, range(0, self.state_size, 8)):
            self.state[i:i+8:2, 0] = l
        self.kf.statePost = self.state
        self.first_detected = True

    def update(self, lanes):
        if self.first_detected:
            for l, i in zip(lanes, range(0, self.meas_size, 4)):
                if l is not None:
                    self.meas[i:i+4, 0] = l
            self.kf.correct(self.meas)
        else:
            if lanes.count(None) == 0:
                self._first_detect(lanes)

    def predict(self, dt):
        if self.first_detected:
            self._update_dt(dt)
            state = self.kf.predict()
            lanes = []
            for i in range(0, len(state), 8):
                lanes.append((state[i], state[i+2], state[i+4], state[i+6]))
            return lanes
        else:
            return None



def roadSegmentation(imagePath='./1416652722Road.jpg'):
    print(imagePath)
    #cap = cv2.VideoCapture(video_path)

    ticks = 0

    lt = track.LaneTracker(2, 0.1, 500)
    ld = detect.LaneDetector(180)
    #while cap.isOpened():
    precTick = ticks
    ticks = cv2.getTickCount()
    dt = (ticks - precTick) / cv2.getTickFrequency()

    #ret, frame = cap.read()
    img = Image.open(imagePath)
    frame = numpy.asarray(img, dtype="float")

    predicted = lt.predict(dt)

    lanes = ld.detect(frame)

    if predicted is not None:
        cv2.line(frame, (predicted[0][0], predicted[0][1]), (predicted[0][2], predicted[0][3]), (0, 0, 255), 5)
        cv2.line(frame, (predicted[1][0], predicted[1][1]), (predicted[1][2], predicted[1][3]), (0, 0, 255), 5)

    lt.update(lanes)

    cv2.imshow('', frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

if __name__ == '__main__':
    main(imagePath='./1416652722Road.jpg')
