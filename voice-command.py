
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
from pynput.keyboard import Key, Controller
import time

def listen_for_command():
    # 初始化音频设置
    samplerate = 16000
    keyboard = Controller()
    
    # 加载Vosk模型
    try:
        model = Model("vosk-model-cn-0.22")  # 需要下载中文模型
        recognizer = KaldiRecognizer(model, samplerate)
    except Exception as e:
        print(f"错误：无法加载语音模型: {e}")
        print("请先下载中文语音模型，可以从 https://alphacephei.com/vosk/models 下载 vosk-model-cn-0.1")
        return

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        if any(indata):
            # 将音频数据转换为正确的格式
            data = np.int16(indata * 32767).tobytes()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"识别到: {text}")
                    if "我" in text:
                        print("执行按键4...")
                        keyboard.press('4')
                        keyboard.release('4')

    print("开始监听语音命令...")
    try:
        with sd.InputStream(channels=1,
                          samplerate=samplerate,
                          dtype=np.float32,
                          callback=audio_callback):
            print("请说话...")
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    listen_for_command()
