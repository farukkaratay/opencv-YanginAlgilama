# OpenCV ve NumPy kütüphanelerini içe aktar
import cv2
import numpy as np

# Kamera nesnesini oluştur
kamera = cv2.VideoCapture(0)

# Ateş renginin HSV renk aralığını belirle

lower = [18, 50, 50]
upper = [35, 130, 100]

lower_fire = np.array(lower, dtype='uint8')  # Ateşin alt sınırları
upper_fire = np.array(upper, dtype='uint8')  # Ateşin üst sınırları

while True:
    # Görüntüyü oku
    ret, frame = kamera.read()
    frame = cv2.resize(frame, (1000, 600))
    # Görüntüyü bulanıklaştırma işlemi uygula
    blur = cv2.GaussianBlur(frame, (21, 21), 0)

    # Maske için işlemler
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)  # Görüntüyü HSV renk uzayına dönüştür
    maske = cv2.inRange(hsv, lower_fire, upper_fire)  # Ateş rengi için maske oluştur
    output = cv2.bitwise_and(frame, hsv, mask=maske)
    no_red = cv2.countNonZero(maske)

    # Ateşin konturunu bul
    contours, hierarchy = cv2.findContours(maske, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Ateş olarak kabul edilen minimum kontur alanı
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Ateşin etrafına dikdörtgen çiz

    if int(no_red) > 150000:
        print("Ateş")

    # Görüntüleri ekranda göster
    cv2.imshow("Kamera Görüntüsü", frame)
    cv2.imshow("output", output)

    # Çıkış tuşuna basılırsa döngüyü sonlandır
    if cv2.waitKey(1) == ord('q'):
        break

# Belleği ve kamera nesnesini serbest bırak
kamera.release()
cv2.destroyAllWindows()



