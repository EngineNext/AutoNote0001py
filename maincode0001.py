import pyaudio
import wave
 
CHUNK = 2**10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
record_time = 15
output_path = "./output.wav"
 
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
 
print("Recording ...")
frames = []
for i in range(0, int(RATE / CHUNK * record_time)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Done.")
 
stream.stop_stream()
stream.close()
p.terminate()
 
wf = wave.open(output_path, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()


import speech_recognition as sr

def transcribe_audio(wav_file):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav_file) as source:
        print("音声を読み込んでいます...")
        audio_data = recognizer.record(source)
        
    try:
        print("文字起こしを開始...")
        text = recognizer.recognize_google(audio_data, language="ja-JP")
        print("文字起こし完了:")
        print(text)
        return text
    except sr.UnknownValueError:
        print("音声を認識できませんでした。")
    except sr.RequestError:
        print("Google Speech Recognition サービスにアクセスできませんでした。")

if __name__ == "__main__":
    wav_file = "output.wav"  # 変換したいWAVファイルのパスを指定
    transcribe_audio(wav_file)
