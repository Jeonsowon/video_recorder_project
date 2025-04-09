import numpy as np
import cv2 as cv

# The given video and calibration data
video_file = './Image_Geometry/checkerboard.mp4'
K = np.array([[1.66696314e+03, 0, 9.54822792e+02],
              [0, 1.66430436e+03, 5.39212517e+02],
              [0, 0, 1]])
dist_coeff = np.array([1.36772126e-01, 1.57500520e-01, 1.13082038e-03, -2.58548829e-03, -2.23836350e+00])
board_pattern = (8, 6)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

# Open a video
video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

# 원본 해상도 얻기
orig_w = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
orig_h = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
original_size = (orig_w, orig_h)

# 원하는 출력 해상도
display_size = (960, 540)

# 카메라 행렬 조정
scale_x = display_size[0] / original_size[0]
scale_y = display_size[1] / original_size[1]
K_resized = K.copy()
K_resized[0, 0] *= scale_x  # fx
K_resized[0, 2] *= scale_x  # cx
K_resized[1, 1] *= scale_y  # fy
K_resized[1, 2] *= scale_y  # cy

# Prepare 3D box and chessboard object points
box_lower = board_cellsize * np.array([[2, 1,  0], [3, 1,  0], [3, 2,  0], [4, 2,  0], [4, 1,  0], [5, 1,  0], [5, 2,  0], 
                                       [6, 2,  0], [6, 3,  0], [5, 3,  0], [5, 4,  0], [4, 4,  0], [4, 5,  0], [3, 5,  0], 
                                       [3, 4,  0], [2, 4,  0], [2, 3,  0], [1, 3,  0], [1, 2,  0], [2, 2,  0],])
box_upper = board_cellsize * np.array([[2, 1,  -1], [3, 1,  -1], [3, 2,  -1], [4, 2,  -1], [4, 1,  -1], [5, 1,  -1], [5, 2,  -1], 
                                       [6, 2,  -1], [6, 3,  -1], [5, 3,  -1], [5, 4,  -1], [4, 4,  -1], [4, 5,  -1], [3, 5,  -1], 
                                       [3, 4,  -1], [2, 4,  -1], [2, 3,  -1], [1, 3,  -1], [1, 2,  -1], [2, 2,  -1],])
obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

# Run pose estimation
while True:
    valid, img = video.read()
    if not valid:
        break

    # 프레임 크기 줄이기
    resized_img = cv.resize(img, display_size)

    # 체스보드 인식
    success, img_points = cv.findChessboardCorners(resized_img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K_resized, dist_coeff)

        # 박스 투영
        line_lower, _ = cv.projectPoints(box_lower, rvec, tvec, K_resized, dist_coeff)
        line_upper, _ = cv.projectPoints(box_upper, rvec, tvec, K_resized, dist_coeff)

        cv.polylines(resized_img, [np.int32(line_lower)], True, (255, 0, 0), 2)
        cv.polylines(resized_img, [np.int32(line_upper)], True, (0, 0, 255), 2)
        for b, t in zip(line_lower, line_upper):
            cv.line(resized_img, np.int32(b.flatten()), np.int32(t.flatten()), (0, 255, 0), 2)

        # 카메라 위치 표시
        R, _ = cv.Rodrigues(rvec)
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(resized_img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))

    # 이미지 출력
    cv.imshow('Pose Estimation (Chessboard)', resized_img)
    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27:
        break

video.release()
cv.destroyAllWindows()