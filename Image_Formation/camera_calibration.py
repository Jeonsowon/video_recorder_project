import numpy as np
import cv2 as cv

# 수동으로 이미지 선택 함수
def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10, wnd_name='Camera Calibration'):
    # Open a video
    video = cv.VideoCapture(video_file)
    assert video.isOpened()

    cv.namedWindow(wnd_name, cv.WINDOW_NORMAL)
    cv.resizeWindow(wnd_name, 960, 540)

    # Select images
    img_select = []
    while True:
        # Grab an images from the video
        valid, img = video.read()
        if not valid:
            break

        if select_all:
            img_select.append(img)
        else:
            # Show the image
            display = img.copy()
            cv.putText(display, f'NSelect: {len(img_select)}', (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
            cv.imshow(wnd_name, display)

            # Process the key event
            key = cv.waitKey(wait_msec)
            if key == ord(' '):             # Space: Pause and show corners
                complete, pts = cv.findChessboardCorners(img, board_pattern)
                cv.drawChessboardCorners(display, board_pattern, pts, complete)
                cv.imshow(wnd_name, display)
                key = cv.waitKey()
                if key == ord('\r'):
                    img_select.append(img) # Enter: Select the image
            if key == 27:                  # ESC: Exit (Complete image selection)
                break

    video.release()
    cv.destroyAllWindows()
    return img_select

# 카메라 캘리브레이션 함수
def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    # Find 2D corner points from given images
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0, 'There is no valid image for calibration.'

    # Prepare 3D points of the chess board
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points) # Must be `np.float32`

    # Calibrate the camera
    return cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)

# 보정 영상 보기 및 저장 함수
def show_rectified_video(video_file, K, dist_coeff):
    video = cv.VideoCapture(video_file)
    assert video.isOpened(), 'Cannot read the given input, ' + video_file

    show_rectify = True
    map1, map2 = None, None
    frame_idx = 1

    display_size = (960, 540)

    while True:
        valid, img_orig = video.read()
        if not valid:
            break

        img_display = img_orig.copy()
        info = "Original"

        if show_rectify:
            if map1 is None or map2 is None:
                map1, map2 = cv.initUndistortRectifyMap(
                    K, dist_coeff, None, None,
                    (img_orig.shape[1], img_orig.shape[0]),
                    cv.CV_32FC1
                )
            img_rectified = cv.remap(img_orig, map1, map2, interpolation=cv.INTER_LINEAR)
            img_display = img_rectified
            info = "Rectified"

        img_show = cv.resize(img_display, display_size)
        cv.putText(img_show, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0), 1)
        cv.imshow("Geometric Distortion Correction", img_show)

        key = cv.waitKey(10)
        if key == ord(' '):  # 일시정지
            key = cv.waitKey()
        elif key == ord('\t'):  # 원본 ↔ 보정 토글
            show_rectify = not show_rectify
        elif key == ord('s'):  # 비교 이미지 저장
            if show_rectify and 'img_rectified' in locals():
                img_orig_rs = cv.resize(img_orig, display_size)
                img_rect_rs = cv.resize(img_rectified, display_size)
                concat = np.hstack([img_orig_rs, img_rect_rs])
                filename = f'rectified_{frame_idx:03d}.png'  # 현재 폴더에 저장
                success = cv.imwrite(filename, concat)
                if success:
                    print(f"저장 완료: {filename}")
                else:
                    print(f"저장 실패: {filename}")
                frame_idx += 1
            else:
                print("보정된 이미지가 없습니다.")
        elif key == 27:  # ESC
            break

    video.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    video_file = './Image_Formation/checkerboard.mp4'
    board_pattern = (8, 6)
    board_cellsize = 0.025

    img_select = select_img_from_video(video_file, board_pattern)
    assert len(img_select) > 0, 'There is no selected images!'
    rms, K, dist_coeff, rvecs, tvecs = calib_camera_from_chessboard(img_select, board_pattern, board_cellsize)

    # Print calibration results
    print('## Camera Calibration Results')
    print(f'* The number of selected images = {len(img_select)}')
    print(f'* RMS error = {rms}')
    print(f'* Camera matrix (K) = \n{K}')
    print(f'* Distortion coefficient (k1, k2, p1, p2, k3, ...) = {dist_coeff.flatten()}')

    print("\n 보정된 영상 확인을 시작합니다 (Tab: 전환, S: 저장, ESC: 종료)")
    show_rectified_video(video_file, K, dist_coeff)