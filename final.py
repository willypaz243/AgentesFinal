import cv2 

from project.controllers import FigureCounter
    
fc = FigureCounter()

def main(filename):
    img = cv2.imread(filename)
    fc.find_figures(img)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main('./media/photo_2.jpg')
    pass