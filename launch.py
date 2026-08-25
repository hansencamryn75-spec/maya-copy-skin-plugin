# -*- coding: utf-8 -*-
"""
Maya 2018 Copy Skin Weights Plugin - Quick Launch Script
拷贝蒙皮权重插件 - 快速启动脚本

在Maya Python脚本编辑器中执行此脚本可快速打开UI窗口
"""

import sys
import os

# 获取脚本目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 添加到路径
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# 导入并显示UI
try:
    from copySkinWeightsUI import show_ui
    show_ui()
    print("\n" + "="*60)
    print("Copy Skin Weights UI opened successfully!")
    print("="*60)
    print("\nInstructions:")
    print("1. Click 'Pick' to select source and target meshes")
    print("2. Configure joint name mapping if needed")
    print("3. Click 'Copy Weights' to copy skin weights")
    print("="*60 + "\n")
    
except Exception as e:
    print("Error opening Copy Skin Weights UI: {}".format(str(e)))
    import traceback
    traceback.print_exc()
