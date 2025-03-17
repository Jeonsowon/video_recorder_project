import cv2 as cv
import numpy as np

# 카메라 웹캠으로 객체 생성
video = cv.VideoCapture(0)

# 동영상 저장 설정
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = None
recording = False

# 윈도우 창 생성
cv.namedWindow("Camera")

while video.isOpened():
    valid, img = video.read()
    img_flip = cv.flip(img, 1)
    merge = np.hstack((img, img_flip))
    if not valid:
        break

    if recording:
        if out is None:
            out = cv.VideoWriter("video_recorder.avi", fourcc, 20.0, (merge.shape[1], merge.shape[0]))  # 파일 생성
        out.write(merge)  # 프레임 저장
        cv.circle(merge, (25, 25), 15, (0, 0, 255), -1)  # 빨간 원 그리기 (녹화 중 표시)
        cv.putText(merge, 'REC', (45, 33), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv.imshow("Camera", merge)

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC 키 종료
        break
    elif key == 32:  # Space 키: 녹화 모드 변경
        recording = not recording
        if not recording and out is not None:
            out.release()  # 녹화 중지 시 파일 닫기
            out = None

# 자원 해제
video.release()
if out is not None:
    out.release()
cv.destroyAllWindows()