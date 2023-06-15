import paho.mqtt.client as mqtt
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

mqtt_server = "172.30.1.112"
mqtt_port = 1883

fs = 48000  # Sample rate
seconds = 5  # Duration of recording
buffer = []

def on_connect(client, userdata, flags, rc):
    client.subscribe("Sound_Data")

def on_message(client, userdata, msg):
    data = int(msg.payload.decode())
    print(f"데이터 수신!: {data}")  # 수신 확인 출력
    buffer.append(data)
    print(f"Buffer size: {len(buffer)}")
    if len(buffer) >= fs * seconds:
        record_audio()

def record_audio():
    try:
        print("record_audio() called")
        recording = np.array(buffer[:fs*seconds])
        buffer[:] = buffer[fs*seconds:]
        write("output.wav", fs, recording)
        print("오디오 파일 저장 완료!")
    except Exception as e:
        print(f"파일 저장 시 에러 발생!: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_server, mqtt_port, 60)
client.loop_start()

while True:
    pass
