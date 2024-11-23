import cv2
import time
import os
import hand as htm

pTime = 0
cap = cv2.VideoCapture(0)

FolderPath = "Fingers" #Đường dẫn đến thư mục
lst = os.listdir(FolderPath) #Liệt kê tất cả các file trong thư mục "Fingers" và lưu vào lst
lst_2 = [] #Lưu các ảnh đã đọc được

# Duyệt qua từng file
for i in lst:
    image = cv2.imread(f"{FolderPath}/{i}") #Đọc ảnh bằng opencv
    lst_2.append(image)

detector = htm.handDetector(detectionCon=0.55)

fingerid = [4 , 8 , 12 , 16 , 20] # Danh sách các chỉ số của từng ngón tay

while True:
    ret , frame = cap.read()
    frame = detector.findHands(frame) #Phát hiện và vẽ các bàn tay lên khung hình
    lmList = detector.findPosition(frame, draw=False) #Phát hiện vị trí

    if len(lmList) != 0: #Kiểm tra nếu có tọa độ điểm mốc được phát hiện
        fingers = [] #Lưu trạng thái của từng ngón tay (giơ lên hay hạ xuống)

        #Bàn tay trái
        if lmList[fingerid[0]][1] < lmList[fingerid[4]][1]:
            # Viết cho ngón cái (điểm 4 nằm bên trái , hay bên phải điểm 3)
            if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        #Bàn tay phải
        elif lmList[fingerid[0]][1] > lmList[fingerid[4]][1]:
            # Viết cho ngón cái (điểm 4 nằm bên trái , hay bên phải điểm 3)
            if lmList[fingerid[0]][1] > lmList[fingerid[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # Viết cho ngón dài
        for id in range(1,5):
            if lmList[fingerid[id]][2] < lmList[fingerid[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        songontay = fingers.count(1) #Đếm số ngón tay đang giơ lên

        h, w, c = lst_2[songontay-1].shape #Lấy chiều cao, chiều rộng và số kênh màu của ảnh ngón tay tương ứng
        frame[0:h , 0:w] = lst_2[songontay-1] #Chèn ảnh ngón tay tương ứng vào khung hình

        # Vẽ hình chữ nhật (xanh lá) hiển thị số ngón tay
        cv2.rectangle(frame,(0,200) , (150,400), (0,255,0) , -1)
        cv2.putText(frame, str(songontay) , (30,390) , cv2.FONT_HERSHEY_PLAIN , 10 , (255,0,0), 5)

    # Viết ra FPS
    cTime = time.time() # Trả về số giây , tính từ 0:00:00 ngày 1/1/1070 theo giờ utc , gọi là thời điểm bắt đầu thời gian
    fps = 1/(cTime-pTime) # Tính fps (frames per second) - đây là chỉ số khung hình trên mỗi giây
    pTime = cTime

    # Show fps lên màn hình
    cv2.putText(frame,f"FPS: {int(fps)}" , (150 ,70) , cv2.FONT_HERSHEY_PLAIN , 3 , (255,0,0) , 3)

    cv2.imshow("Finger_Math" , frame)
    if cv2.waitKey(1) == ord("q"): # Độ trễ 1/1000s , nếu bấm q sẽ Thoát
        break
        
cap.release() #Giải phóng camera
