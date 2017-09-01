import glob 
import pickle
import matplotlib.image as mpimg
import numpy as np
from .image_gen import *
from PIL import Image

#--------------------------------------------------------------------
#PROCESSING FUNCTIONS

def undistort(image):
    #undistort
    calibration = pickle.load( open("./roadLaneFinding/calibration.p", "rb") )
    mtx = calibration['mtx']
    dist = calibration['dist']
    undist = find_coeffs(mtx, image)
    return undist


def process(undist):
    #binary thresholds
    abs_canny_thresh_1 = abs_canny_thresh(undist, thresh=(30, 100))
    mag_thresh_1 = mag_thresh(undist, thresh=(60, 100))
    dir_thresh_1 = dir_thresh(undist, thresh=(-np.pi/4, np.pi/4))
    rgb_thresh_1 = rgb_thresh(undist, channel="r", thresh=(0, 100))
    hls_thresh_1 = hls_thresh(undist, channel="s", thresh=(0, 110))

    #combine thresholds
    combined = np.zeros_like(undist[:,:,0])
    combined[hls_thresh_1 == 1] = 1
    combined[abs_canny_thresh_1 == 1] = 1

    #apply filter
    proc = filterf(combined)

    return proc


def transform(proc):

    img_size = (proc.shape[1], proc.shape[0])
    src = np.float32([(257, 685), (1050, 685), (583, 460),(702, 460)])
    dst = np.float32([(200, 720), (1080, 720), (200, 0), (1080, 0)])
    M = find_coeffs(src, dst) 
    Minv = find_coeffs(dst, src) #inverse
    trans = find_coeffs(proc, M)

    return trans, Minv


def find_lanes(image, trans, Minv):
    #create historgram for bottom half of trans
    hist = np.sum(trans[int(trans.shape[0]/2):,:], axis=0) 
    #output image to draw on + visualize
    out_img = np.dstack((trans, trans, trans))*255
    #peaks of left + right halves if hist	
    midpoint = np.int(hist.shape[0]/2)
    leftx_base = np.argmax(hist[:midpoint])
    rightx_base = np.argmax(hist[midpoint:]) + midpoint
    #number of sliding windows
    nwindows = 9
    #window height 
    window_height = np.int(trans.shape[0]/nwindows)

    #x and y positions of all nonzero pizels in img
    nonzero = trans.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    #current positions to be updated
    leftx_current = leftx_base
    rightx_current = rightx_base

    #width of windows +/- margin
    margin = 100
    #min number of pixels to recenter window
    minpix = 50

    #empty lists to receive left and right lane pixel indices
    left_lane_indices = []
    right_lane_indices = []


    #step through windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = trans.shape[0] - (window+1)*window_height
        win_y_high = trans.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Draw the windows on the visualization image
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),(win_xleft_high,win_y_high),(0,255,0), 2) 
        cv2.rectangle(out_img,(win_xright_low,win_y_low),(win_xright_high,win_y_high),(0,255,0), 2) 
        # Identify the nonzero pixels in x and y within the window
        good_left_indices = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_indices = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_indices.append(good_left_indices)
        right_lane_indices.append(good_right_indices)
        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_left_indices) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_indices]))
        if len(good_right_indices) > minpix:        
            rightx_current = np.int(np.mean(nonzerox[good_right_indices]))

    # Concatenate the arrays of indices
    left_lane_indices = np.concatenate(left_lane_indices)
    right_lane_indices = np.concatenate(right_lane_indices)

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_indices]
    lefty = nonzeroy[left_lane_indices] 
    rightx = nonzerox[right_lane_indices]
    righty = nonzeroy[right_lane_indices] 

    # Fit a second order polynomial to each
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)


    # Generate x and y values for plotting
    ploty = np.linspace(0, trans.shape[0]-1, trans.shape[0] )
    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

    out_img[nonzeroy[left_lane_indices], nonzerox[left_lane_indices]] = [255, 0, 0]
    out_img[nonzeroy[right_lane_indices], nonzerox[right_lane_indices]] = [0, 0, 255]
    
    #curvature radius
    y_eval = np.max(ploty)
    ym_per_pix = 30./720 # meters per pixel in y dimension
    xm_per_pix = 3.7/700 # meteres per pixel in x dimension

    left_fit_cr = np.polyfit(ploty*ym_per_pix, left_fitx*xm_per_pix, 2)
    right_fit_cr = np.polyfit(ploty*ym_per_pix, right_fitx*xm_per_pix, 2)

    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])

    radi = [left_curverad, right_curverad]

    
    #position from center
    pos = trans.shape[1]/2
    offset = (abs(pos - (leftx_base + rightx_base)/2))*xm_per_pix

    #unwarp
    warp_zero = np.zeros_like(trans).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    #Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))
     # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    newwarp = find_coeffs(color_warp, Minv) 
    # Combine the result with the original image
    #alpha = 1, beta = 0.3, gamma = 0
    result = image + newwarp*0.3

    return out_img, result, left_fitx, right_fitx, ploty, radi, offset


#--------------------------------------------------------------------
#PROCESS FUNCTION
def process_image(image, path='./test_result/test0.jpg'):
    undist = undistort(image)
    proc = process(undist)
    trans, Minv = transform(proc)
    out_img, result, left_fitx, right_fitx, ploty, radi, offset = find_lanes(image, trans, Minv)
    #img = Image.fromarray(out_img, 'RGB')
    #img.show()
    img = Image.fromarray(result, 'RGB')
    #img.show()
    #print(image)
    img.save(path)

    return result

def doFindLane(originalPath, outPath):
    sample_image = cv2.imread(originalPath)
    process_image(sample_image, path=outPath)


#ORIGINALS
if __name__ == '__main__':
    originals = glob.glob('./test_images/*.jpg')

    #store images
    sample_images = []

    #add images to vector
    for originalPath in originals:
        print(originalPath)
        sample_image = cv2.imread(originalPath)
        sample_images.append(sample_image)
        process_image(sample_image, path=originalPath.replace('/test_images/', '/test_result/'))

#--------------------------------------------------------------------
















































































from .camera_cal.lane import *

