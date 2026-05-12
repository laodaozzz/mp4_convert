import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

def convert_file():
    # 打开文件选择对话框
    filepath = filedialog.askopenfilename(
        title="选择一个视频文件",
        filetypes=[("Video files", "*.mp4 *.ts")]
    )
    if not filepath:
        return

    # 获取文件扩展名
    ext = os.path.splitext(filepath)[1].lower()
    dirname = os.path.dirname(filepath)
    basename = os.path.splitext(os.path.basename(filepath))[0]

    try:
        if ext == ".mp4":
            # mp4 转 mp3
            output_file = os.path.join(dirname, basename + ".mp3")
            cmd = ["ffmpeg", "-i", filepath, "-q:a", "0", "-map", "a", output_file]
        elif ext == ".ts":
            # ts 转 mp4
            output_file = os.path.join(dirname, basename + ".mp4")
            cmd = ["ffmpeg", "-i", filepath, "-c", "copy", output_file]
        else:
            messagebox.showerror("错误", "只支持 mp4 或 ts 文件")
            return

        # 执行 FFmpeg 命令
        subprocess.run(cmd, check=True)
        messagebox.showinfo("完成", f"转换成功！输出文件：\n{output_file}")

    except subprocess.CalledProcessError:
        messagebox.showerror("错误", "转换失败，请检查是否已安装 FFmpeg")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    convert_file()
