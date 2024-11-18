from vosk import Model, KaldiRecognizer
import sounddevice as sd
import numpy as np
import json
import os
import time
import threading
import platform
from queue import Queue

class KeyPresser:
    def __init__(self):
        self.system = platform.system()
        self.last_press_time = 0
        self.min_interval = 0.3  # 设置最小触发间隔为300ms
        
        if self.system == "Windows":
            import keyboard
            self.keyboard = keyboard
        elif self.system == "Darwin":  # macOS
            from subprocess import call
            self.call = call
    
    def press_4(self):
        current_time = time.time()
        if current_time - self.last_press_time < self.min_interval:
            return
        
        self.last_press_time = current_time
        if self.system == "Windows":
            self.keyboard.press_and_release('4')
            import winsound
            winsound.Beep(1000, 100)
        elif self.system == "Darwin":
            script = 'tell application "System Events" to keystroke "4"'
            self.call(["osascript", "-e", script])
            os.system("afplay /System/Library/Sounds/Tink.aiff &")

class VoiceProcessor:
    def __init__(self, model_path="vosk-model-cn-0.22"):
        self.samplerate = 16000
        self.buffer_size = int(self.samplerate * 0.2)  # 200ms缓冲区
        self.key_presser = KeyPresser()
        self.audio_queue = Queue()
        self.is_running = True
        
        # 初始化语音模型
        try:
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, self.samplerate)
            # 设置部分参数以提高响应速度
            self.recognizer.SetWords(True)
            self.recognizer.SetPartialWords(True)
        except Exception as e:
            print(f"错误：无法加载语音模型: {e}")
            raise

    def process_audio(self):
        while self.is_running:
            if not self.audio_queue.empty():
                data = self.audio_queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    self.handle_result(result)
            else:
                time.sleep(0.01)

    def handle_result(self, result):
        text = result.get("text", "")
        if text:
            print(f"识别到: {text}")
            if any(keyword in text for keyword in ["广智","广志","就", "救", "我"]):
                print("检测到关键词，执行按键4...")
                try:
                    self.key_presser.press_4()
                except Exception as e:
                    print(f"按键执行失败: {e}")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        if any(indata):
            data = np.int16(indata * 32767).tobytes()
            self.audio_queue.put(data)

    def run(self):
        system = platform.system()
        if system not in ["Windows", "Darwin"]:
            print("错误：不支持的操作系统")
            return

        print(f"\n=== 语音控制程序 ===")
        print(f"当前操作系统: {system}")
        print("开始监听语音命令...")
        print("当检测到以下任意关键词时将触发按键4: 广智, 救, 我")
        print("按 Ctrl+C 可以退出程序\n")

        # 启动音频处理线程
        process_thread = threading.Thread(target=self.process_audio, daemon=True)
        process_thread.start()

        try:
            with sd.InputStream(
                channels=1,
                samplerate=self.samplerate,
                dtype=np.float32,
                blocksize=self.buffer_size,
                callback=self.audio_callback
            ):
                print("请说话...")
                while self.is_running:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n程序已停止")
        except Exception as e:
            print(f"发生错误: {e}")
            if "PortAudio" in str(e):
                print("提示：请确保已连接麦克风设备")
        finally:
            self.is_running = False

if __name__ == "__main__":
    processor = VoiceProcessor()
    processor.run()
