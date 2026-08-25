# -*- coding: utf-8 -*-
"""
userSetup.py
Maya用户初始化脚本 - 自动加载Copy Skin Weights插件

将此文件复制到 Maya脚本文件夹:
  Windows: %USERPROFILE%\Documents\maya\2018\scripts
  Mac: ~/Library/Preferences/Autodesk/maya/2018/scripts
  Linux: ~/maya/2018/scripts
"""

import sys
import os

# 获取插件目录路径
# 假设插件在标准的Maya脚本目录下
PLUGIN_BASE_DIR = os.path.join(
    os.path.expanduser("~"),
    "Documents" if sys.platform == "win32" else "",
    "maya",
    "2018",
    "scripts",
    "copySkinWeights"
)

# 如果标准路径不存在，尝试其他常见位置
if not os.path.exists(PLUGIN_BASE_DIR):
    # 尝试从当前脚本目录的上级目录查找
    current_script = os.path.abspath(__file__)
    possible_paths = [
        os.path.join(os.path.dirname(current_script), "copySkinWeights"),
        os.path.expanduser("~/maya/2018/scripts/copySkinWeights"),
        os.path.expanduser("~/Documents/maya/2018/scripts/copySkinWeights"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            PLUGIN_BASE_DIR = path
            break

# 添加插件目录到Python路径
if os.path.exists(PLUGIN_BASE_DIR) and PLUGIN_BASE_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_BASE_DIR)
    print("Copy Skin Weights plugin directory added to path: {}".format(PLUGIN_BASE_DIR))

# 加载插件
try:
    import pluginLoader
    
    # 加载主插件
    pluginLoader.load_plugin()
    
    # 创建菜单 (如果在GUI模式下)
    try:
        import maya.cmds as cmds
        if not cmds.about(batch=True):
            pluginLoader.create_maya_menu()
    except:
        pass
    
    print("Copy Skin Weights Plugin initialized from userSetup.py")
    
except ImportError as e:
    print("WARNING: Could not load Copy Skin Weights plugin from userSetup.py")
    print("Make sure the plugin is installed in: {}".format(PLUGIN_BASE_DIR))
except Exception as e:
    print("ERROR in userSetup.py: {}".format(str(e)))
