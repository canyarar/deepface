import cv2
from deepface import DeepFace
from gtts import gTTS
import os
import subprocess
import threading
import time

# Metni okuyan iş parçacığı fonksiyonu
def play_audio(filename):
    tts = gTTS(text=filename, lang='tr')
    tts.save('temp.mp3')
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    subprocess.call([vlc_path, "--play-and-exit", "temp.mp3"])
    os.remove("temp.mp3")

def main():
    cap = cv2.VideoCapture(0)

    # Zamanlayıcı ayarları
    interval = 16  # Her 10 saniyede bir metni oku ve oynat
    last_play_time = time.time() - interval
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # DeepFace ile yüz analizi yapın
        results = DeepFace.analyze(frame, actions=['age', 'gender', 'emotion'])

        # Her bir sonucu işleyin
        for result in results:
            age = result['age']
            gender_probabilities = result['gender']
            emotion = result['dominant_emotion']
            
            # Cinsiyeti olasılıklara göre belirleyin
            if gender_probabilities['Woman'] > gender_probabilities['Man']:
                gender_text = "Kadın"
            else:
                gender_text = "Erkek"
                
            # Duygu durumunu Türkçe'ye çevirin
            if emotion == "neutral":
                emotion_text = "Normal"
            elif emotion == "happy":
                emotion_text = "Mutlu"
            elif emotion == "sad":
                emotion_text = "Üzgün"
            else:
                emotion_text = "Bilinmeyen"
                
            age_range = f"yaşın ortalama {age}"
            sohret = f"Lütfen bekle seni analiz ediyorum."
            gender_text = f"Analiz edildin! Cinsiyetin: {gender_text}"
            emotion_text = f"Duygu durumun: {emotion_text}"
            combined_text = f"{gender_text}. {emotion_text}. {age_range}"
            
            current_time = time.time()
            
            # Belirli bir aralıkta metni okuma ve oynatma işlemini kontrol et
            if current_time - last_play_time >= interval:
                last_play_time = current_time
                # Metni okumak için yeni bir iş parçacığı başlatın
                audio_thread = threading.Thread(target=play_audio, args=(combined_text,))
                audio_thread.start()
                print("x")
            
        cv2.imshow('Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
