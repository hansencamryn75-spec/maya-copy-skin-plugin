# -*- coding: utf-8 -*-
"""
Copy Skin Weights Plugin - Installation Script
安装脚本 - 自动配置和安装插件到Maya

Usage:
  python install.py
  python install.py uninstall
"""

import os
import sys
import shutil
import platform

def get_maya_scripts_path(maya_version=2018):
    """获取 Maya 脚本文件夹路径"""
    system = platform.system()
    
    if system == 'Windows':
        docs_path = os.path.expanduser("~\\Documents")
        return os.path.join(docs_path, "maya", str(maya_version), "scripts")
    elif system == 'Darwin':  # macOS
        return os.path.expanduser("~/Library/Preferences/Autodesk/maya/{}/scripts".format(maya_version))
    elif system == 'Linux':
        return os.path.expanduser("~/maya/{}/scripts".format(maya_version))
    else:
        return None

def create_plugin_folder(target_path):
    """创建插件文件夹"""
    plugin_folder = os.path.join(target_path, "copySkinWeights")
    
    if not os.path.exists(target_path):
        print("Creating Maya scripts directory: {}".format(target_path))
        os.makedirs(target_path)
    
    if not os.path.exists(plugin_folder):
        print("Creating plugin folder: {}".format(plugin_folder))
        os.makedirs(plugin_folder)
    
    return plugin_folder

def copy_plugin_files(source_dir, target_dir):
    """复制插件文件"""
    plugin_files = [
        'copySkinWeights.py',
        'copySkinWeightsUI.py',
        'pluginLoader.py',
        'launch.py'
    ]
    
    copied_count = 0
    for filename in plugin_files:
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, filename)
        
        if os.path.exists(source_file):
            print("  Copying: {}".format(filename))
            shutil.copy2(source_file, target_file)
            copied_count += 1
        else:
            print("  WARNING: File not found: {}".format(filename))
    
    return copied_count

def install_plugin(maya_version=2018):
    """安装插件"""
    print("=" * 70)
    print("Copy Skin Weights Plugin Installer v1.0")
    print("=" * 70)
    print()
    
    # 获取当前脚本目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print("Plugin source directory: {}".format(current_dir))
    print()
    
    # 获取 Maya 脚本路径
    maya_scripts = get_maya_scripts_path(maya_version)
    if not maya_scripts:
        print("ERROR: Unsupported platform!")
        return False
    
    print("Target Maya version: {}".format(maya_version))
    print("Maya scripts directory: {}".format(maya_scripts))
    print()
    
    # 创建插件文件夹
    print("Creating directories...")
    plugin_dir = create_plugin_folder(maya_scripts)
    print()
    
    # 复制文件
    print("Copying plugin files...")
    copied = copy_plugin_files(current_dir, plugin_dir)
    print("Successfully copied {} files".format(copied))
    print()
    
    print("=" * 70)
    print("Installation completed successfully!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Restart Maya")
    print("2. The plugin will load automatically")
    print("3. Or manually run in Python Script Editor:")
    print("   from copySkinWeightsUI import show_ui; show_ui()")
    print()
    print("Plugin location: {}".format(plugin_dir))
    print("=" * 70)
    print()
    
    return True

def uninstall_plugin(maya_version=2018):
    """卸载插件"""
    print("=" * 70)
    print("Copy Skin Weights Plugin Uninstaller")
    print("=" * 70)
    print()
    
    maya_scripts = get_maya_scripts_path(maya_version)
    if not maya_scripts:
        print("ERROR: Unsupported platform!")
        return False
    
    plugin_dir = os.path.join(maya_scripts, "copySkinWeights")
    
    if not os.path.exists(plugin_dir):
        print("Plugin folder not found: {}".format(plugin_dir))
        print("Nothing to uninstall.")
        return True
    
    print("Removing plugin folder: {}".format(plugin_dir))
    try:
        shutil.rmtree(plugin_dir)
        print("Plugin uninstalled successfully!")
        print("=" * 70)
        return True
    except Exception as e:
        print("ERROR: Failed to uninstall: {}".format(str(e)))
        return False

def main():
    """主函数"""
    command = 'install'
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    
    if command == 'uninstall':
        success = uninstall_plugin()
    else:
        success = install_plugin()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
