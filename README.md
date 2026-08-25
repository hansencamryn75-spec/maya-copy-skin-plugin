````markdown
# Copy Skin Weights Plugin for Maya 2018

Maya 2018 拷贝蒙皮权重插件 - 支持在不同网格之间复制和镜像蒙皮权重

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Maya](https://img.shields.io/badge/maya-2018-green.svg)
![Python](https://img.shields.io/badge/python-2.7-orange.svg)

## 功能特性

✨ **核心功能**
- 🎯 在两个网格之间快速拷贝蒙皮权重
- 🔄 自动查找对应顶点（基于世界坐标）
- 🏷️ 智能关节名称映射（搜索替换）
- 📊 实时显示操作结果和错误信息
- ⚙️ 完整的撤销/重做支持

✨ **UI功能**
- 💻 友好的用户界面，易于操作
- 📋 源网格和目标网格选择器
- 🔧 灵活的选项配置
- 📝 实时日志输出

## 系统要求

- **Maya 版本**: 2018 或更高
- **Python**: 2.7+ (Maya 2018 内置)
- **操作系统**: Windows, macOS, Linux

## 快速开始

### 方式 1: 在 Python 脚本编辑器中运行

1. 在 Maya 中打开 Python 脚本编辑器
2. 执行以下代码：

```python
import sys
import os

# 添加插件路径 - 替换为你的下载路径
plugin_path = "C:/path/to/maya-copy-skin-plugin"  # Windows
# plugin_path = "/Users/username/path/to/maya-copy-skin-plugin"  # macOS
# plugin_path = "~/path/to/maya-copy-skin-plugin"  # Linux

if plugin_path not in sys.path:
    sys.path.insert(0, plugin_path)

from copySkinWeightsUI import show_ui
show_ui()
```

### 方式 2: 使用启动脚本

1. 打开 Maya Python 脚本编辑器
2. 执行 `launch.py` 文件中的代码

## 完整安装指南

### Windows 用户

1. 下载项目所有文件
2. 创建文件夹: `Documents\maya\2018\scripts\copySkinWeights`
3. 将所有 .py 文件复制到此文件夹
4. 在 Maya 中执行启动代码

### macOS 用户

```bash
# 创建脚本目录
mkdir -p ~/Library/Preferences/Autodesk/maya/2018/scripts/copySkinWeights

# 复制文件
cp -r /path/to/downloaded/files ~/Library/Preferences/Autodesk/maya/2018/scripts/copySkinWeights/
```

### Linux 用户

```bash
# 创建脚本目录
mkdir -p ~/maya/2018/scripts/copySkinWeights

# 复制文件
cp -r /path/to/downloaded/files ~/maya/2018/scripts/copySkinWeights/
```

## 使用方法

### 1. 打开插件窗口

```python
from copySkinWeightsUI import show_ui
show_ui()
```

### 2. 选择源网格
- 在 Maya 视图中选择有蒙皮的网格
- 点击 "Pick" 按钮（Source Mesh 区域）

### 3. 选择目标网格
- 在 Maya 视图中选择要接收蒙皮的网格
- 点击 "Pick" 按钮（Target Mesh 区域）

### 4. 拷贝权重
- 点击 "Copy Weights" 按钮
- 等待完成，查看日志结果

### 5. 关节名称映射（可选）

如果源目标网格的关节名称不同（如 L_ 和 R_）：

1. 勾选 "Enable Joint Name Mapping"
2. 输入搜索字符串：`L_`
3. 输入替换字符串：`R_`
4. 点击 "Copy Weights"

## 文件说明

| 文件 | 说明 |
|------|------|
| `copySkinWeights.py` | 核心功能模块 |
| `copySkinWeightsUI.py` | UI 界面模块 |
| `pluginLoader.py` | 插件加载器 |
| `userSetup.py` | 自动初始化脚本 |
| `launch.py` | 快速启动脚本 |
| `README.md` | 使用文档 |
| `install.py` | 安装脚本 |

## Python API 使用

### 基本使用

```python
from copySkinWeights import get_plugin_instance

# 获取插件实例
plugin = get_plugin_instance()

# 设置源和目标网格
plugin.set_source('source_mesh')
plugin.set_target('target_mesh')

# 拷贝权重
success_count, fail_count = plugin.copy_weights()
print("Success: {}, Failed: {}".format(success_count, fail_count))
```

### 带关节映射

```python
from copySkinWeights import get_plugin_instance

plugin = get_plugin_instance()
plugin.set_source('source_mesh')
plugin.set_target('target_mesh')

# 将 L_ 替换为 R_
success, fail = plugin.copy_weights(search_replace=('L_', 'R_'))
```

### 获取状态

```python
status = plugin.get_status()
print("Source: {}".format(status['source']))
print("Target: {}".format(status['target']))
print("Source joints: {}".format(status['source_joints']))
print("Target joints: {}".format(status['target_joints']))
```

## 常见问题

### Q1: 执行代码后没有窗口出现

**A:** 确保 Maya 处于 GUI 模式（非批处理模式）。检查脚本编辑器的输出窗口是否有错误信息。

### Q2: 找不到 skinCluster

**A:** 确保选中的网格已绑定蒙皮。可用以下代码检查：

```python
import maya.cmds as cmds

mesh = 'your_mesh_name'
shapes = cmds.listRelatives(mesh, shapes=True)
if shapes:
    shape = shapes[0]
    history = cmds.listHistory(shape)
    skins = cmds.ls(history, type='skinCluster')
    print("Found skinClusters: {}".format(skins))
```

### Q3: 拷贝后网格变形异常

**A:** 可能原因：
1. 源和目标网格顶点位置差异太大
2. 关节映射不正确
3. 目标网格缺少某些关节

**解决方案：**
- 检查网格的世界坐标
- 验证关节命名规则
- 确保所有关节都存在

### Q4: 如何卸载插件

```python
import pluginLoader
pluginLoader.unload_plugin()
```

## 故障排除

### 错误: "ModuleNotFoundError"

**原因:** Python 路径不正确  
**解决:** 检查插件文件位置，确保路径正确

### 错误: "No mesh found"

**原因:** 输入的网格名称不存在  
**解决:** 检查网格名称是否正确

### 错误: "No skinCluster found"

**原因:** 网格没有蒙皮  
**解决:** 为网格添加 Skin 变形器

### UI 无法打开

**原因:** Maya 不在 GUI 模式  
**解决:** 确保使用的是标准 Maya 而不是 mayabatch

## 脚本编辑器快捷代码

将以下代码保存为 Maya 的快捷代码：

```python
# Copy Skin Weights - Open UI
import sys
plugin_path = "path/to/plugin"
if plugin_path not in sys.path:
    sys.path.insert(0, plugin_path)
from copySkinWeightsUI import show_ui
show_ui()
```

## 版本信息

- **版本**: 1.0.0
- **Maya**: 2018+
- **Python**: 2.7+
- **发布日期**: 2026-08-25

## 更新日志

### v1.0.0
- ✅ 初始版本发布
- ✅ 核心拷贝功能
- ✅ 完整 UI 界面
- ✅ 关节名称映射
- ✅ 详细文档

## 许可证

MIT License

## 作者

**hansencamryn75**  
GitHub: https://github.com/hansencamryn75-spec

## 支持

遇到问题？
- 查看 Issues: https://github.com/hansencamryn75-spec/maya-copy-skin-plugin/issues
- 发送邮件: hansencamryn75@gmail.com

---

**最后更新**: 2026-08-25
````
