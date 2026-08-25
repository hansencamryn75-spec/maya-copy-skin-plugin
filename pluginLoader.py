# -*- coding: utf-8 -*-
"""
Copy Skin Weights Plugin Loader
插件加载器 - 在Maya中初始化和加载插件

用于在userSetup.py或插件管理器中调用
"""

import maya.cmds as cmds
import sys
import os

# 获取当前脚本目录
PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))

# 添加插件目录到Python路径
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)


def load_plugin():
    """加载Copy Skin Weights插件"""
    try:
        # 导入插件模块
        import copySkinWeights
        import copySkinWeightsUI
        
        print("=" * 60)
        print("Copy Skin Weights Plugin v1.0 loaded successfully!")
        print("=" * 60)
        print("Usage:")
        print("  from copySkinWeightsUI import show_ui")
        print("  show_ui()")
        print("=" * 60)
        
        return True
        
    except ImportError as e:
        print("ERROR: Failed to load Copy Skin Weights Plugin")
        print("Import Error: {}".format(str(e)))
        return False
    except Exception as e:
        print("ERROR: Failed to initialize Copy Skin Weights Plugin")
        print("Error: {}".format(str(e)))
        return False


def show_copy_skin_weights_ui():
    """显示Copy Skin Weights UI"""
    try:
        from copySkinWeightsUI import show_ui
        show_ui()
    except Exception as e:
        print("ERROR: Failed to show Copy Skin Weights UI")
        print("Error: {}".format(str(e)))


def create_maya_menu():
    """在Maya菜单栏创建Copy Skin Weights菜单"""
    try:
        # 获取主菜单栏
        gMainWindow = mel.eval('$tmpVar=$gMainWindow')
        
        # 检查菜单是否已存在
        menu_name = "copySkinWeightsMenu"
        if cmds.menu(menu_name, exists=True):
            cmds.deleteUI(menu_name)
        
        # 创建菜单
        menu = cmds.menu(
            menu_name,
            label="Skin Tools",
            parent=gMainWindow,
            tearOff=True
        )
        
        # 添加菜单项
        cmds.menuItem(
            label="Copy Skin Weights...",
            command="from copySkinWeightsUI import show_ui; show_ui()",
            parent=menu
        )
        
        cmds.menuItem(
            optionBox=True,
            parent=menu,
            command="print('Copy Skin Weights Options')"
        )
        
        print("Menu created successfully")
        return True
        
    except Exception as e:
        print("WARNING: Failed to create Maya menu")
        print("Error: {}".format(str(e)))
        return False


def unload_plugin():
    """卸载插件"""
    try:
        # 删除UI窗口
        if cmds.window("copySkinWeightsWindow", exists=True):
            cmds.deleteUI("copySkinWeightsWindow", window=True)
        
        # 删除菜单
        if cmds.menu("copySkinWeightsMenu", exists=True):
            cmds.deleteUI("copySkinWeightsMenu")
        
        # 清除模块
        if 'copySkinWeights' in sys.modules:
            del sys.modules['copySkinWeights']
        if 'copySkinWeightsUI' in sys.modules:
            del sys.modules['copySkinWeightsUI']
        
        print("Copy Skin Weights Plugin unloaded")
        return True
        
    except Exception as e:
        print("ERROR: Failed to unload Copy Skin Weights Plugin")
        print("Error: {}".format(str(e)))
        return False


# 当脚本被导入时自动加载
if __name__ != "__main__":
    load_plugin()
