import os
import subprocess
import json
import sys

def check_ffmpeg():
    """检查系统是否安装了 ffmpeg"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_audio_info(file_path):
    """获取音频文件的比特率和采样率"""
    try:
        # 使用 ffprobe 获取 JSON 格式的音频信息
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            file_path
        ]
        result = subprocess.check_output(cmd)
        data = json.loads(result)
        
        # 获取比特率 (bit_rate)
        # 优先从 format 中获取，如果没有则尝试从 stream 中获取
        bit_rate = data.get('format', {}).get('bit_rate')
        if not bit_rate:
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'audio':
                    bit_rate = stream.get('bit_rate')
                    break
        
        if bit_rate:
            return int(bit_rate)
        return None
    except Exception as e:
        print(f"读取文件信息失败 {file_path}: {e}")
        return None

def compress_mp3(input_file, output_file):
    """压缩单个 MP3 文件"""
    original_bitrate = get_audio_info(input_file)
    
    if not original_bitrate:
        print(f"[跳过] 无法获取比特率: {input_file}")
        return

    # 计算目标比特率：原大小的 1/3
    target_bitrate = int(original_bitrate / 3)

    # 为了保证最低音质，限制最低比特率不低于 32k (32000)
    # 如果是纯语音录音，可以接受更低，如果是音乐，低于 64k 会很难听
    # 这里为了严格执行“体积减小到 1/3”，不做强制下限，但建议一般不低于 24k
    if target_bitrate < 24000:
        target_bitrate = 24000
        print(f"  警告: 计算出的比特率过低，已自动调整为 24kbps 以防音频损坏。")

    print(f"[处理中] {input_file}")
    print(f"  原比特率: {int(original_bitrate/1000)}k -> 目标比特率: {int(target_bitrate/1000)}k")

    try:
        # 核心 FFmpeg 命令
        # -i: 输入文件
        # -b:a: 设置音频比特率
        # -y: 覆盖输出文件（如果存在）
        # -v error: 只显示错误信息，减少刷屏
        cmd = [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-b:a", str(target_bitrate),
            "-v", "error",
            output_file
        ]
        
        subprocess.run(cmd, check=True)
        print(f"  [完成] 已保存至: {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"  [失败] FFmpeg 转换出错: {e}")

def main():
    # 检查 ffmpeg 是否存在
    if not check_ffmpeg():
        print("错误: 未找到 ffmpeg。请先安装 ffmpeg 并添加到系统环境变量。")
        input("按回车键退出...")
        return

    # 获取当前目录
    current_dir = os.getcwd()
    
    # 创建输出文件夹，避免覆盖原文件
    output_dir = os.path.join(current_dir, "compressed_output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 扫描当前文件夹下的 mp3
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.mp3')]
    
    if not files:
        print("当前文件夹下没有找到 .mp3 文件。")
        return

    print(f"找到 {len(files)} 个 MP3 文件，准备开始压缩...\n")

    for file in files:
        input_path = os.path.join(current_dir, file)
        output_path = os.path.join(output_dir, file)
        compress_mp3(input_path, output_path)

    print("\n所有任务已完成！压缩后的文件在 'compressed_output' 文件夹中。")

if __name__ == "__main__":
    main()