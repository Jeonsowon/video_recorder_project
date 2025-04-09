# video_recorder_project
My video recorder project using Python, OpenCV

## video_recorder.py [📁](video_recorder/video_recorder.py) [📷](video_recorder/video_recoder_output.avi)
- You can start recording by clicking the Space key.
- When recording, a red circle and the phrase "REC" are displayed.
- You can exit the video by clicking the ESC key.
- This video is shown by merging the screen flipped

## cartoon_rendering.py [📁](cartoon_rendering/cartoon_rendering.py) [📷](cartoon_rendering)
- image procesisng으로 만화 스타일로 변환할 수 있다.
- good_test.jpg의 경우 3D이미지의 edge 표현이 잘 되었으며 배경의 도시이미지가 블러처리되어 자연스러워졌다.
- bad_test.jpg의 경우 부드럽게 표현된 사진이라 테두리가 명확하지 않아 오히려 뭉게지게 되었다.
- 색상 대비를 높이고 코드를 추가하거나 edge를 더 강조할 수 있는 다른 필터를 사용하면 개선 될 수 있을거 같은 한계가 있다.
### Good Test Output / Bad Test Output 데모 이미지
 ![good_test_output](https://github.com/user-attachments/assets/05f9351b-534d-4a25-adb3-18c1d9beca37)
 ![bad_test_output](https://github.com/user-attachments/assets/39da5168-9860-49a2-aaa2-0b04b69eeee7)


## camera_calibration.py [📁](Image_Formation/camera_calibration.py) [📷](Image_Formation/rectified_001.png) [📷](Image_Formation/rectified_002.png)
- 해상도 : 960 X 540
- Calibration 영상 가이드
  - Space = Pause and show corners
  - Enter = Select the image
  - ESC = Exit (Complete image selection)
  - 영상 종료 후에 아래와 같이 Calibration Results 출력됨  
### Camera Calibration Results
  * The number of selected images = 16
  * RMS error = 0.4815605295508748
  * Camera matrix (K) =
  [[1.66696314e+03 0.00000000e+00 9.54822792e+02]
   [0.00000000e+00 1.66430436e+03 5.39212517e+02]
   [0.00000000e+00 0.00000000e+00 1.00000000e+00]]
  * Distortion coefficient (k1, k2, p1, p2, k3, ...) = [ 1.36772126e-01  1.57500520e-01  1.13082038e-03 -2.58548829e-03
 -2.23836350e+00]

- Lens distortion correction 영상 가이드
  - Tab = original 영상과 rectified 영상 전환
  - S = original 이미지와 rectified 이미지 합병하여 비교 이미지로 저장, filename = rectified_001.png, 파일명 idx는 1개씩 늘어남, 현재 폴더에 저장됨
  - ESC = Exit
 
### Lens Distortion Correction 데모 이미지
![rectified_001](https://github.com/user-attachments/assets/d8ffdaac-b03d-484f-851f-e5fe34b77f8b)
![rectified_002](https://github.com/user-attachments/assets/51db8fa3-ed8d-4cef-84af-940f658d70eb)

## pose_estimation.py [📁](Image_Geometry/pose_estimation.py) [📷](Image_Geometry/demo_image_001.png) [📷](Image_Geometry/demo_image_002.png) [📷](Image_Geometry/demo_image_003.png)
- 해상도 : 960 X 540 으로 조정
- calibration 결과로 얻은 Camera matrix(K)와 Distortion coefficient 값을 이용하였고, 해상도 축소에 따라 값 조정함
- AR 물체 : 3D 네모 하트

### Pose Estimation 데모 이미지
![demo_image_001](https://github.com/user-attachments/assets/6d0e344e-6644-471c-8756-64c16b92e3a6)
![demo_image_002](https://github.com/user-attachments/assets/a415734b-fed7-4727-a293-af4d4c88c7af)
![demo_image_003](https://github.com/user-attachments/assets/4f49adaa-8cbb-4b15-b9ae-13b9fc80cc4d)




  

