import cv2 as cv
import numpy as np

#Loda the image
img = cv.imread('bad_test.jpg')
if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

# Grayscale 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# 노이즈 제거
gray = cv.medianBlur(gray, 5)
# Adaptive Thresholding으로 엣지 검출
edges = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9, 9)
# Bilateral 필터로 색상 영역 단순화 (여러 번 반복하여 만화 느낌 강화)
color = img.copy()
for _ in range(3):  # 3~5회 반복 적용 추천
    color = cv.bilateralFilter(color, d=9, sigmaColor=100, sigmaSpace=100)
# 색상 이미지에 엣지 덮어씌우기
cartoon = cv.bitwise_and(color, color, mask=edges)
# 가장자리 선 강조 (black line 느낌 강화)
edges_inv = cv.bitwise_not(edges)
edges_inv_colored = cv.cvtColor(edges_inv, cv.COLOR_GRAY2BGR)
cartoon_strong = cv.addWeighted(cartoon, 0.9, edges_inv_colored, 0.1, 0)

# Display the cartoon image
cv.imshow("Cartoon", cartoon_strong)
cv.waitKey(0)
cv.destroyAllWindows()