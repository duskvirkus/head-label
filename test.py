import cv2

im_path = "/home/duskvirkus/dev/head-label/test-folders/test-input/to-process/_MG_4202.JPG"
x = 0.609073359073359
y = 0.42547033285094066

im = cv2.imread(im_path)
im = cv2.circle(im, (int(x * im.shape[1]), int(y * im.shape[0])), 5, (255, 0, 0), 2)

cv2.imwrite('test.png', im, [cv2.IMWRITE_PNG_COMPRESSION, 0])