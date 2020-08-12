import cv2
import numpy as np

COLORS = ['blue', 'green', 'red']
FIGURES = ['cube', 'tetrahedron', 'sphere']

def encode_color(color:str):
    encoded_color = (np.array(COLORS) == color).astype('int') * 255
    encoded_color = map(int, encoded_color)
    return list(encoded_color)

def max_color(color):
    color = color[:3]
    return np.argsort(color)

def color_filter(img, color):
    c3, c2, c1 = max_color(color)
    mask = (img[:,:,c1] > img[:,:,c2]) * (img[:,:,c1] > img[:,:,c3])
    mask = mask * (img[:,:,c1] - img[:,:,c2]) > 60
    mask = mask * 255
    mask = np.uint8(mask)
    kernel = np.ones((3,3),np.uint8)
    mask = cv2.dilate(mask,kernel,iterations=2)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 2)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel, iterations = 2)
    #mask = cv2.erode(mask,kernel,iterations=3)
    dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
    _, mask = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return mask

def filter_yellow(img):
    img = cv2.GaussianBlur(img, (3,3), 2)
    pixel = np.uint8([0,255,255])
    img = np.abs(pixel - img)
    img[:,:,1] = cv2.equalizeHist(img[:,:,1])
    img[:,:,2] = cv2.equalizeHist(img[:,:,2])
    mask = img[:,:,0] > (img[:,:,1] + img[:,:,1])/2
    mask = mask * np.abs(img[:,:,0] - ((img[:,:,1] + img[:,:,1])/2)) > 150
    mask = mask * 255
    mask = np.uint8(mask)
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.erode(mask,kernel,iterations=1)
    mask = cv2.dilate(mask,kernel,iterations=6)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel, iterations = 5)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel, iterations = 5)
    mask = cv2.GaussianBlur(mask, (3,3), 2)
    dist_transform = cv2.distanceTransform(mask,cv2.DIST_L2,5)
    _, mask = cv2.threshold(dist_transform,0.4*dist_transform.max(),255,0)
    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return mask

def find_all_objects(img):
    mask_b = color_filter(img, encode_color(COLORS[0]))
    mask_g = color_filter(img, encode_color(COLORS[1]))
    mask_r = color_filter(img, encode_color(COLORS[2]))
    mask = cv2.bitwise_or(mask_b, mask_g)
    mask = cv2.bitwise_or(mask, mask_r)
    return mask

def find_contours(mask):
    #mask = cv2.UMat(mask)
    mask = np.uint8(mask)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    contours,_ = cv2.findContours(mask,1,2)
    return contours

def get_locations(contours):
    locations = []
    for i in contours:
        #Calcular el centro a partir de los momentos
        momentos = cv2.moments(i)
        if momentos['m00']:
            cx = int(momentos['m10']/momentos['m00'])
            cy = int(momentos['m01']/momentos['m00'])
        else:
            cx = int(momentos['m10'])
            cy = int(momentos['m01'])
        #Dibujar el centro
        locations.append([cx, cy])
    return np.int32(locations)

def display_analysis(frame, figures:list):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for figure in figures:
        shape = figure.shape
        cx, cy = figure.location
        cv2.circle(frame, (cx, cy), 3, (0,255,255), -1)
        #cv2.putText(frame, f"(x: {str(cx)}, y: {str(cy)})",(cx+10,cy+10), font, 0.3,(0,0,0),1)
        cv2.putText(frame, f"id:{figure.id}" , (cx,cy-5),font,0.5,(0,0,0),2)
        pass
def display_agent(frame, agents:list):
    font = cv2.FONT_HERSHEY_SIMPLEX
    for agent in agents:
        cx, cy = agent.location
        cv2.circle(frame, (cx, cy), 3, (0,255,255), -1)
        cv2.putText(frame, f"(x: {str(cx)}, y: {str(cy)})",(cx+10,cy+10), font, 0.5,(255,255,255),1)
        cv2.putText(frame, f"agent: {agent.id}" , (cx,cy-5),font,0.75,(0,0,0),2)

def find_figure(contour):
    figure = None
    area=cv2.contourArea(contour)
    if (area > 100):
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) > 3 and len(approx) < 5:
            figure = 'cubo'
        elif len(approx) >= 5:
            figure = 'esfera'
        elif len(approx) < 4:
            figure = 'tetraedro'
    return figure

def find_shape(contour):
    figure = None
    area=cv2.contourArea(contour)
    if (area > 100):
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        if len(approx) > 3 and len(approx) < 5:
            figure = 'cuadrado'
        elif len(approx) >= 5:
            figure = 'circulo'
        elif len(approx) < 4:
            figure = 'triangulo'
    return figure