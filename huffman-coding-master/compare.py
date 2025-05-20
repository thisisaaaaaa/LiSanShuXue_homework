import os

def get_file_size(file_path):
    try:
        size_bytes = os.path.getsize(file_path)
        return {
            "bytes": size_bytes,
            "readable": convert_size(size_bytes),
            "type": "Binary" if file_path.endswith(".bin") else "Text"
        }
    except FileNotFoundError:
        return "文件不存在！"

def convert_size(bytes_num):
    units = ["B", "KB", "MB", "GB"]
    for unit in units:
        if bytes_num < 1024:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024
    return f"{bytes_num:.2f} TB"

# 测试
files = ["task.txt", "task.bin"]
for file in files:
    info = get_file_size(file)
    if isinstance(info, dict):
        print(f"[{info['type']}] {file}: {info['readable']} ({info['bytes']} 字节)")
    else:
        print(f"[错误] {file}: {info}")