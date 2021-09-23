import argparse
import os

import cv2

import numpy as np

def parse_args():
    desc = "Tools to crop unnecessary space from outside of images" 
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-i','--input_folder', type=str,
        default='./input/',
        help='Directory path to the inputs folder. (default: %(default)s)')

    parser.add_argument('-o','--out_file', type=str,
        default='./output.csv',
        help='Output csv. (default: %(default)s)')

    args = parser.parse_args()
    return args


class Context:
    def __init__(self,img,label):
        self.start = False
        self.label = label
        self.img = img
        self.img_show = np.copy(img)
        self.head_points = []

    def display(self):
        self.img_show = np.copy(self.img)

        for head_point in self.head_points:
            self.img_show = cv2.circle(self.img_show, head_point, 5, (255, 0, 0), 2)


        cv2.imshow('head-label', self.img_show)
        cv2.resizeWindow('head-label', self.img_show.shape[1], self.img_show.shape[0])

    # def on_click(self):
    #     self.img_show = cv2.circle(self.img_show, center_coordinates, radius, color, thickness)

    def add_head_point(self, x, y):
        self.head_points.append([x, y])

    def export_to_list(self, ls, file):
        for head_point in self.head_points:
            ls.append([file, head_point[0] / float(self.img_show.shape[1]), head_point[1] / float(self.img_show.shape[0])])

def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:

        c.add_head_point(x, y)
        

        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(c.img_show, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)


def main():

    global args
    global c

    args = parse_args()

    all_points = []

    done = False

    for root, subdirs, files, in os.walk(args.input_folder):

        print(root)

        for file in files:
            im_path = os.path.join(root, file)

            im = cv2.imread(im_path)
            print(im.shape)

            scale_percent = 20
            width = int(im.shape[1] * scale_percent / 100)
            height = int(im.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)

            # cv2.imshow('head-label', resized)

            # cv2.waitKey(0)

            cv2.namedWindow('head-label',cv2.WINDOW_NORMAL)

            cv2.setMouseCallback('head-label', click_event)


            c = Context(resized,1)

            running = True

            while(running):

                c.display()

                k = cv2.waitKey(33)

                if k==-1:
                    continue
                elif k == 13: # enter
                    running = False
                elif k == 27: # ESC
                    running = False
                    done = True
                elif k == 91: # a key
                    c.head_points = []
                else:
                    print('pressed: ', k)

            c.export_to_list(all_points, file)

            cv2.destroyAllWindows()

            if done:
                break

    # Save list as csv

    print(all_points)

    f = open(args.out_file, "w")
    f.write(f'filename,norm_x,norm_y\n')
    for i in range(len(all_points)):
        f.write(f'{all_points[i][0]},{all_points[i][1]},{all_points[i][2]}')
        if i != len(all_points) - 1:
            f.write('\n')
    f.close

if __name__ == "__main__":
    main()