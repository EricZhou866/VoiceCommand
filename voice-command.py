from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
import json
import os
import time
import threading
from subprocess import call

def press_key_4():
    # 使用 osascript 在 Mac 上模拟按键4
    script = '''
    tell application "System Events"
        keystroke "4"
    end tell
    '''
    call(["osascript", "-e", script])
    # 播放系统提示音
    os.system("afplay /System/Library/Sounds/Tink.aiff")

def listen_for_command():
    samplerate = 16000
    
    try:
        model = Model("vosk-model-cn-0.22")
        recognizer = KaldiRecognizer(model, samplerate)
    except Exception as e:
        print(f"错误：无法加载语音模型: {e}")
        print("请先下载中文语音模型 vosk-model-cn-0.22")
        return

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        if any(indata):
            data = np.int16(indata * 32767).tobytes()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print(f"识别到: {text}")
                    if any(keyword in text for keyword in ["广志","广智", "救", "我", "就"]):
                        print("检测到关键词，执行按键4...")
                        press_key_4()

    print("开始监听语音命令...")
    print("当检测到以下任意关键词时将触发按键4: 广智, 救, 我")
    print("按 Ctrl+C 可以退出程序")
    
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
