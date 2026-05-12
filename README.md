# mp4_convert

[English](#english) | [中文](#中文)

---

## English

Two simple Python scripts for audio/video conversion and MP3 compression, powered by FFmpeg.

### Features

- **convert_to_mp3.py** — GUI tool (tkinter)
  - Convert MP4 to MP3 (extract audio)
  - Convert TS to MP4

- **compress_mp3.py** — Batch MP3 compressor
  - Scan current directory for all MP3 files
  - Reduce bitrate to 1/3 of original (minimum 24kbps)
  - Output to `compressed_output/` folder

### Prerequisites

- Python 3.x
- FFmpeg installed and added to PATH

### Usage

**Convert video:**

```bash
python convert_to_mp3.py
```

A file picker dialog will appear. Select an MP4 or TS file.

**Compress MP3s:**

```bash
python compress_mp3.py
```

Place the script in the same folder as your MP3 files, then run it.

---

## 中文

两个简单的 Python 脚本，用于音视频转换和 MP3 压缩，基于 FFmpeg。

### 功能特点

- **convert_to_mp3.py** — GUI 工具（tkinter）
  - 将 MP4 转换为 MP3（提取音频）
  - 将 TS 转换为 MP4

- **compress_mp3.py** — MP3 批量压缩
  - 扫描当前目录下所有 MP3 文件
  - 将比特率压缩到原来的 1/3（最低 24kbps）
  - 输出到 `compressed_output/` 文件夹

### 环境要求

- Python 3.x
- 已安装 FFmpeg 并添加到系统 PATH

### 使用方法

**转换视频：**

```bash
python convert_to_mp3.py
```

弹出文件选择对话框，选择 MP4 或 TS 文件即可。

**压缩 MP3：**

```bash
python compress_mp3.py
```

将脚本放在 MP3 文件所在目录，然后运行。

---

## License

MIT
