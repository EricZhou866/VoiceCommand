# 语音按键控制器

这是一个跨平台的语音控制程序，可以通过语音命令自动触发按键操作。当检测到特定关键词时，程序会自动按下数字键"4"并播放提示音。

## 功能特点

- 支持 Windows 和 macOS 系统
- 实时语音识别
- 离线运行，不需要网络连接
- 自动播放按键提示音
- 简单的命令行界面
- 低资源占用

## 系统要求

- Python 3.8 或更高版本
- Windows 10/11 或 macOS 10.15 或更高版本
- 麦克风设备
- 至少 200MB 磁盘空间（主要用于语音模型）

## 安装指南

### 第一步：安装 Python

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载并安装最新版本的 Python
3. 安装时勾选"Add Python to PATH"选项

### 第二步：下载程序

1. 下载程序代码到本地文件夹
2. 打开终端(macOS)或命令提示符(Windows)，进入程序所在目录

### 第三步：创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS:
source venv/bin/activate
```

### 第四步：安装依赖

Windows系统：
```bash
pip install vosk sounddevice numpy keyboard
```

macOS系统：
```bash
pip install vosk sounddevice numpy
```

### 第五步：下载语音模型

1. 访问 [Vosk模型下载页面](https://alphacephei.com/vosk/models)
2. 下载 `vosk-model-cn-0.22.zip` 中文语音模型
3. 解压到程序所在目录，确保文件夹名称为 `vosk-model-cn-0.22`

### 系统权限设置

#### Windows系统：
1. 确保麦克风权限已启用
   - 设置 -> 隐私 -> 麦克风
   - 允许应用访问麦克风
2. 可能需要以管理员身份运行程序

#### macOS系统：
1. 允许终端访问麦克风
   - 系统偏好设置 -> 安全性与隐私 -> 麦克风
   - 勾选终端程序
2. 允许终端使用辅助功能（用于模拟按键）
   - 系统偏好设置 -> 安全性与隐私 -> 辅助功能
   - 勾选终端程序

## 使用说明

1. 在终端或命令提示符中运行程序：
```bash
python voice_command.py
```

2. 程序启动后会显示当前系统信息和运行状态

3. 触发关键词：
   - "广智"
   - "救"
   - "我"

4. 当说出包含以上任意关键词的语句时，程序会：
   - 自动按下数字键"4"
   - 播放提示音
   - 在控制台显示识别结果

5. 按 Ctrl+C 可以安全退出程序

## 常见问题

1. **找不到麦克风设备**
   - 检查麦克风是否正确连接
   - 检查系统麦克风权限设置
   - 确保没有其他程序占用麦克风

2. **语音识别不准确**
   - 确保在安静的环境中使用
   - 靠近麦克风说话
   - 语速保持正常，发音清晰

3. **按键没有响应**
   - Windows：检查是否以管理员权限运行
   - macOS：检查辅助功能权限设置
   - 确保目标窗口处于活动状态

4. **安装依赖失败**
   - 尝试使用管理员权限安装
   - 确保网络连接正常
   - 尝试使用国内镜像源：
     ```bash
     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple 包名
     ```

## 更新日志

### v1.0.0 (2024-03-17)
- 首次发布
- 支持 Windows 和 macOS
- 基础语音识别功能
- 按键模拟与提示音

## 许可证

本项目采用 MIT 许可证。

## 技术支持

如遇到问题，请提交 Issue 或发送邮件至：[EricZhou866 # gmail.com]

