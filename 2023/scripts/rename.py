import os
from typing import Dict, List


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )


def rename_unprocessed():
    student = "s2047783"
    folder_path = os.path.join(PREFIX_2023, student)
    file_names = [filename for filename in os.listdir(folder_path) if "ui_trim" not in filename]
    for file_name in file_names:
        parts = file_name.split("_")
        parts = parts[:-2] + ["unprocessed"] + parts[-2:]
        new_name = "_".join(parts)
        old_file_path = os.path.join(folder_path, file_name)
        # 构建新文件名的完整路径
        new_file_path = os.path.join(folder_path, new_name)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f'已重命名文件: {file_name} -> {new_name}')
    
def rename_cleaned():
    student = "s2047783"
    folder_path = os.path.join(PREFIX_2023, student, "ui_trims")
    file_names = os.listdir(folder_path)
    for file_name in file_names:
        parts = file_name.split("_")
        parts = parts[:-2] + ["clean"] + parts[-2:]
        new_name = "_".join(parts)
        old_file_path = os.path.join(folder_path, file_name)
        # 构建新文件名的完整路径
        new_file_path = os.path.join(folder_path, new_name)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f'已重命名文件: {file_name} -> {new_name}')

# rename_cleaned()