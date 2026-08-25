# -*- coding: utf-8 -*-
"""
Quick Setup Guide - Copy Skin Weights Plugin
快速设置指南

包含所有必要的文件和使用说明
"""

SETUP_GUIDE = """
╔════════════════════════════════════════════════════════════════╗
║     Copy Skin Weights Plugin for Maya 2018 - Quick Setup       ║
╚════════════════════════════════════════════════════════════════╝

【文件列表】
  ✓ copySkinWeights.py        - 核心功能模块
  ✓ copySkinWeightsUI.py      - UI 界面模块  
  ✓ pluginLoader.py           - 插件加载器
  ✓ userSetup.py              - 自动启动脚本
  ✓ launch.py                 - 快速启动脚本
  ✓ install.py                - 安装脚本
  ✓ README.md                 - 完整文档

【快速开始 - 方式1: 直接运行】

在 Maya Python 脚本编辑器中执行:

    import sys
    plugin_path = r"C:\\path\\to\\maya-copy-skin-plugin"  # Windows
    # plugin_path = "/path/to/maya-copy-skin-plugin"      # macOS/Linux
    
    if plugin_path not in sys.path:
        sys.path.insert(0, plugin_path)
    
    from copySkinWeightsUI import show_ui
    show_ui()

【快速开始 - 方式2: 使用安装脚本】

Windows:
    1. 右键点击 install.py
    2. 选择 "Edit with IDLE" 或用记事本打开
    3. 点击运行（或在命令行执行 python install.py）
    4. 重启 Maya

macOS/Linux:
    1. 打开终端
    2. cd 到插件目录
    3. python install.py
    4. 重启 Maya

【快速开始 - 方式3: 自动启动】

将整个插件文件夹复制到:

Windows:
    C:\\Users\\YourName\\Documents\\maya\\2018\\scripts\\copySkinWeights

macOS:
    ~/Library/Preferences/Autodesk/maya/2018/scripts/copySkinWeights

Linux:
    ~/maya/2018/scripts/copySkinWeights

然后重启 Maya，插件会自动加载。

【使用步骤】

1. 打开 UI 窗口
   from copySkinWeightsUI import show_ui
   show_ui()

2. 选择源网格
   - 在 Maya 视图中选择有蒙皮的网格
   - 点击 "Pick" 按钮 (Source Mesh 区域)

3. 选择目标网格  
   - 在 Maya 视图中选择要接收蒙皮的网格
   - 点击 "Pick" 按钮 (Target Mesh 区域)

4. 配置选项（可选）
   - 如果需要关节名称映射，勾选并设置搜索/替换字符串
   - 例如: L_ → R_

5. 拷贝权重
   - 点击 "Copy Weights" 按钮
   - 查看日志窗口的结果

【常见问题】

Q: 执行代码后没有窗口出现？
A: 确保 Maya 不在批处理模式。检查脚本编辑器是否有错误信息。

Q: 找不到 skinCluster？
A: 确保选中的网格已绑定蒙皮。

Q: 拷贝后网格变形异常？
A: 检查源目标网格的坐标，验证关节映射是否正确。

Q: 如何卸载？
A: 运行 python install.py uninstall
   或手动删除插件文件夹

【文件详解】

主要文件:
  copySkinWeights.py - 包含 CopySkinWeights 类，实现核心功能
  copySkinWeightsUI.py - 包含 CopySkinWeightsUI 类，提供 UI 窗口

辅助文件:
  pluginLoader.py - 负责加载和初始化插件
  userSetup.py - Maya 自动启动脚本
  launch.py - 快速启动脚本

配置文件:
  install.py - 自动安装脚本
  README.md - 完整使用文档

【Python API 示例】

基本使用:
    from copySkinWeights import get_plugin_instance
    
    plugin = get_plugin_instance()
    plugin.set_source('source_mesh')
    plugin.set_target('target_mesh')
    success, fail = plugin.copy_weights()
    print("Success: {}, Failed: {}".format(success, fail))

带关节映射:
    plugin.copy_weights(search_replace=('L_', 'R_'))

获取状态:
    status = plugin.get_status()
    print(status)

【版本信息】

版本: 1.0.0
Maya: 2018+
Python: 2.7+

【支持和反馈】

GitHub: https://github.com/hansencamryn75-spec/maya-copy-skin-plugin
邮箱: hansencamryn75@gmail.com

【许可证】

MIT License - 可自由使用和修改

════════════════════════════════════════════════════════════════

需要帮助? 查看 README.md 获取详细文档

════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(SETUP_GUIDE)
    
    # 保存为文件
    try:
        with open('SETUP_GUIDE.txt', 'w', encoding='utf-8') as f:
            f.write(SETUP_GUIDE)
        print("\n✓ 设置指南已保存到 SETUP_GUIDE.txt")
    except:
        pass
