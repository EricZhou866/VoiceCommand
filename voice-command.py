from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
import json
import os
import time
import threading
import platform

class KeyPresser:
    def __init__(self):
        self.system = platform.system()
        if self.system == "Windows":
            import keyboard
            self.keyboard = keyboard
        elif self.system == "Darwin":  # macOS
            from subprocess import call
            self.call = call
    
    def press_4(self):
        if self.system == "Windows":
            self.keyboard.press_and_release('4')
            import winsound
            winsound.Beep(1000, 100)  # 1000Hz, 持续100ms
        elif self.system == "Darwin":
            script = '''
            tell application "System Events"
                keystroke "4"
            end tell
            '''
            self.call(["osascript", "-e", script])
            os.system("afplay /System/Library/Sounds/Tink.aiff")

def listen_for_command():
    samplerate = 16000
    key_presser = KeyPresser()
    
    # 检测操作系统
    system = platform.system()
    if system not in ["Windows", "Darwin"]:
        print("错误：不支持的操作系统")
        return
        
    print(f"当前操作系统: {system}")
    
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
                    if any(keyword in text for keyword in ["广智", "救", "我"]):
                        print("检测到关键词，执行按键4...")
                        try:
                            key_presser.press_4()
                        except Exception as e:
                            print(f"按键执行失败: {e}")

    print("\n=== 语音控制程序 ===")
    print("开始监听语音命令...")
    print("当检测到以下任意关键词时将触发按键4: 广智, 救, 我")
    print("按 Ctrl+C 可以退出程序\n")
    
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
        if "PortAudio" in str(e):
            print("提示：请确保已连接麦克风设备")

if __name__ == "__main__":
    listen_for_command()
