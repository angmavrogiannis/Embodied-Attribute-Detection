import cv2
[160, 36, 463, 428]
img=cv2.imread("panda.jpeg")
x0 = 160
y0 = 36
x1 = 463
y1 = 428
start_point = (int(x0), int(y0))
end_point = (int(x1), int(y1))
cv2.rectangle(img, start_point, end_point, color=(0,0,0), thickness=2)
cv2.imwrite("bbox.jpg", img)   
