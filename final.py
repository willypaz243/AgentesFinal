import cv2 

from project.controllers import FigureCounter
    
fc = FigureCounter()

colors = ['blue', 'green', 'red']
shapes = ['cuadrado', 'circulo', 'triangulo']

def main(filename):
    image = cv2.imread(filename)
    inp = -1
    running = True
    img = image.copy()
    while running:
        while not inp > 0 and inp <= 4:
            print("elige criterio")
            print(" 1. color")
            print(" 2. shape")
            print(" 3. ninguno")
            print(" 4. exit")
            try:
                inp = int(input("su opción >>> "))
            except:
                pass
        
        if (inp == 1):
            print("Elige color", colors)
            inp_str = 'none'
            while not inp_str in colors:
                inp_str = input("color >>> ")
            fc.mark_figures(img, color=inp_str)
        elif inp == 2:
            print("Elige forma", shapes)
            inp_str = 'none'
            while not inp_str in shapes:
                inp_str = input("color >>> ")
            fc.mark_figures(img, shape=inp_str)
        elif inp == 3:
            fc.mark_figures(img)
        elif inp == 4:
            running = False
        if inp !=4:
            cv2.imshow('Image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        inp = -1
        img = image.copy()

if __name__ == "__main__":
    main('./media/photo_2.jpg')
    pass