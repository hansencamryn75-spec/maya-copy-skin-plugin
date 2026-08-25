# -*- coding: utf-8 -*-
"""
批量下载脚本 - 用于快速获取所有插件文件

如果无法下载整个文件夹，使用此脚本逐个下载文件
"""

import urllib.request
import os
import sys

# GitHub 原始文件地址
BASE_URL = "https://raw.githubusercontent.com/hansencamryn75-spec/maya-copy-skin-plugin/main"

# 需要下载的文件列表
FILES_TO_DOWNLOAD = [
    'copySkinWeights.py',
    'copySkinWeightsUI.py',
    'pluginLoader.py',
    'userSetup.py',
    'launch.py',
    'install.py',
    'README.md',
    'SETUP_GUIDE.py'
]

def download_file(url, filename, output_dir='.'):
    """下载单个文件"""
    output_path = os.path.join(output_dir, filename)
    
    try:
        print("Downloading: {}...".format(filename), end=' ')
        urllib.request.urlretrieve(url, output_path)
        print("✓ Done")
        return True
    except Exception as e:
        print("✗ Failed: {}".format(str(e)))
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("Copy Skin Weights Plugin - File Downloader")
    print("=" * 70)
    print()
    
    # 创建输出目录
    output_dir = "maya-copy-skin-plugin"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print("Created directory: {}".format(output_dir))
    
    print()
    print("Downloading files from GitHub...")
    print()
    
    success_count = 0
    fail_count = 0
    
    for filename in FILES_TO_DOWNLOAD:
        url = "{}/{}".format(BASE_URL, filename)
        if download_file(url, filename, output_dir):
            success_count += 1
        else:
            fail_count += 1
    
    print()
    print("=" * 70)
    print("Download Summary")
    print("=" * 70)
    print("Success: {}".format(success_count))
    print("Failed: {}".format(fail_count))
    print("Output directory: {}".format(os.path.abspath(output_dir)))
    print()
    
    if fail_count == 0:
        print("✓ All files downloaded successfully!")
        print()
        print("Next steps:")
        print("1. Run: python {}/install.py".format(output_dir))
        print("2. Restart Maya")
        print("3. Run in Python Script Editor: from copySkinWeightsUI import show_ui; show_ui()")
    else:
        print("✗ Some files failed to download.")
        print("Please check your internet connection and try again.")
    
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
