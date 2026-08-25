# -*- coding: utf-8 -*-
"""
Copy Skin Weights UI Module
拷贝蒙皮权重 - UI界面模块

提供Maya UI窗口和交互功能
"""

import maya.cmds as cmds
import maya.OpenMaya as om
from copySkinWeights import get_plugin_instance
import traceback


class CopySkinWeightsUI(object):
    """蒙皮权重拷贝 UI类"""
    
    WINDOW_NAME = "copySkinWeightsWindow"
    WINDOW_TITLE = "Copy Skin Weights v1.0"
    
    def __init__(self):
        self.plugin = get_plugin_instance()
        self.window = None
        
    def show(self):
        """显示UI窗口"""
        # 删除旧窗口
        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME, window=True)
        
        # 创建新窗口
        self.window = cmds.window(
            self.WINDOW_NAME,
            title=self.WINDOW_TITLE,
            widthHeight=(500, 600),
            resizeToFitChildren=True,
            sizeable=True
        )
        
        # 创建主布局
        self._create_main_layout()
        
        # 显示窗口
        cmds.showWindow(self.window)
        
    def _create_main_layout(self):
        """创建主布局"""
        main_form = cmds.formLayout(numberOfDivisions=100)
        
        # ==================== 标题部分 ====================
        header_frame = cmds.frameLayout(
            label="Copy Skin Weights",
            collapsable=False,
            marginWidth=5,
            marginHeight=5
        )
        cmds.text(label="Maya 2018 Copy Skin Weights Plugin v1.0", 
                 font="boldLabelFont", 
                 align="center")
        cmds.text(label="Copy and mirror skin weights between meshes", 
                 font="smallPlainTextFont",
                 align="center")
        cmds.setParent("..")
        
        # ==================== 源网格设置 ====================
        source_frame = cmds.frameLayout(
            label="Source Mesh",
            collapsable=True,
            marginWidth=10,
            marginHeight=10
        )
        
        source_form = cmds.formLayout(numberOfDivisions=100)
        
        source_text = cmds.text(label="Source Mesh:", align="right", width=120)
        self.source_field = cmds.textField(
            placeholderText="Select source mesh...",
            editable=False
        )
        source_btn = cmds.button(
            label="Pick",
            command=lambda: self._pick_source()
        )
        
        source_info = cmds.text(
            self.source_field + "_info",
            label="No source selected",
            align="left",
            backgroundColor=(0.3, 0.3, 0.3)
        )
        
        cmds.formLayout(
            source_form,
            edit=True,
            attachForm=[
                (source_text, "top", 5),
                (source_text, "left", 5),
                (self.source_field, "top", 5),
                (source_btn, "top", 5),
                (source_btn, "right", 5),
                (source_info, "top", 40),
                (source_info, "left", 5),
                (source_info, "right", 5)
            ],
            attachControl=[
                (self.source_field, "left", 5, source_text),
                (self.source_field, "right", 5, source_btn)
            ]
        )
        
        cmds.setParent("..")
        
        # ==================== 目标网格设置 ====================
        target_frame = cmds.frameLayout(
            label="Target Mesh",
            collapsable=True,
            marginWidth=10,
            marginHeight=10
        )
        
        target_form = cmds.formLayout(numberOfDivisions=100)
        
        target_text = cmds.text(label="Target Mesh:", align="right", width=120)
        self.target_field = cmds.textField(
            placeholderText="Select target mesh...",
            editable=False
        )
        target_btn = cmds.button(
            label="Pick",
            command=lambda: self._pick_target()
        )
        
        target_info = cmds.text(
            self.target_field + "_info",
            label="No target selected",
            align="left",
            backgroundColor=(0.3, 0.3, 0.3)
        )
        
        cmds.formLayout(
            target_form,
            edit=True,
            attachForm=[
                (target_text, "top", 5),
                (target_text, "left", 5),
                (self.target_field, "top", 5),
                (target_btn, "top", 5),
                (target_btn, "right", 5),
                (target_info, "top", 40),
                (target_info, "left", 5),
                (target_info, "right", 5)
            ],
            attachControl=[
                (self.target_field, "left", 5, target_text),
                (self.target_field, "right", 5, target_btn)
            ]
        )
        
        cmds.setParent("..")
        
        # ==================== 选项设置 ====================
        options_frame = cmds.frameLayout(
            label="Options",
            collapsable=True,
            marginWidth=10,
            marginHeight=10
        )
        
        options_form = cmds.formLayout(numberOfDivisions=100)
        
        # 搜索替换选项
        search_label = cmds.text(label="Search String:", align="right")
        self.search_field = cmds.textField(
            placeholderText="e.g. L_",
            text=""
        )
        
        replace_label = cmds.text(label="Replace String:", align="right")
        self.replace_field = cmds.textField(
            placeholderText="e.g. R_",
            text=""
        )
        
        self.use_search_check = cmds.checkBox(
            label="Enable Joint Name Mapping",
            value=False,
            changeCommand=self._toggle_search_fields
        )
        
        # 镜像选项
        mirror_label = cmds.text(label="Mirror Axis:", align="right")
        self.mirror_axis = cmds.radioCollection()
        cmds.radioButton(label="X", select=True, collection=self.mirror_axis)
        cmds.radioButton(label="Y", collection=self.mirror_axis)
        cmds.radioButton(label="Z", collection=self.mirror_axis)
        
        cmds.formLayout(
            options_form,
            edit=True,
            attachForm=[
                (self.use_search_check, "top", 5),
                (self.use_search_check, "left", 5),
                (search_label, "top", 35),
                (search_label, "left", 5),
                (self.search_field, "top", 35),
                (replace_label, "top", 65),
                (replace_label, "left", 5),
                (self.replace_field, "top", 65),
                (mirror_label, "top", 95),
                (mirror_label, "left", 5)
            ],
            attachControl=[
                (self.search_field, "left", 5, search_label),
                (self.search_field, "right", 5, None),
                (self.replace_field, "left", 5, replace_label),
                (self.replace_field, "right", 5, None)
            ]
        )
        
        cmds.setParent("..")
        
        # ==================== 操作按钮 ====================
        button_frame = cmds.frameLayout(
            label="Actions",
            collapsable=False,
            marginWidth=10,
            marginHeight=10
        )
        
        button_form = cmds.formLayout(numberOfDivisions=100)
        
        self.copy_btn = cmds.button(
            label="Copy Weights",
            height=40,
            backgroundColor=(0.2, 0.5, 0.2),
            command=lambda: self._copy_weights()
        )
        
        self.mirror_btn = cmds.button(
            label="Mirror Weights",
            height=40,
            backgroundColor=(0.2, 0.4, 0.6),
            command=lambda: self._mirror_weights()
        )
        
        clear_btn = cmds.button(
            label="Clear",
            height=25,
            command=lambda: self._clear_selection()
        )
        
        cmds.formLayout(
            button_form,
            edit=True,
            attachForm=[
                (self.copy_btn, "top", 5),
                (self.copy_btn, "left", 5),
                (self.copy_btn, "right", 5),
                (self.mirror_btn, "top", 50),
                (self.mirror_btn, "left", 5),
                (self.mirror_btn, "right", 5),
                (clear_btn, "top", 95),
                (clear_btn, "left", 5),
                (clear_btn, "right", 5)
            ]
        )
        
        cmds.setParent("..")
        
        # ==================== 日志输出 ====================
        log_frame = cmds.frameLayout(
            label="Log",
            collapsable=True,
            marginWidth=10,
            marginHeight=10
        )
        
        self.log_text = cmds.scrollField(
            editable=False,
            wordWrap=True,
            height=150
        )
        
        cmds.setParent("..")
        
        # ==================== 主布局排列 ====================
        cmds.formLayout(
            main_form,
            edit=True,
            attachForm=[
                (header_frame, "top", 5),
                (header_frame, "left", 5),
                (header_frame, "right", 5),
                (source_frame, "left", 5),
                (source_frame, "right", 5),
                (target_frame, "left", 5),
                (target_frame, "right", 5),
                (options_frame, "left", 5),
                (options_frame, "right", 5),
                (button_frame, "left", 5),
                (button_frame, "right", 5),
                (log_frame, "left", 5),
                (log_frame, "right", 5),
                (log_frame, "bottom", 5)
            ],
            attachControl=[
                (source_frame, "top", 5, header_frame),
                (target_frame, "top", 5, source_frame),
                (options_frame, "top", 5, target_frame),
                (button_frame, "top", 5, options_frame),
                (log_frame, "top", 5, button_frame)
            ]
        )
    
    def _pick_source(self):
        """选择源网格"""
        selection = cmds.ls(selection=True, type='mesh')
        if not selection:
            self._log("Please select a mesh")
            return
        
        mesh = selection[0]
        try:
            success, message = self.plugin.set_source(mesh)
            if success:
                cmds.textField(self.source_field, edit=True, text=mesh)
                self._update_source_info()
                self._log("✓ " + message)
            else:
                self._log("✗ Error: " + message)
        except Exception as e:
            self._log("✗ Error: " + str(e))
    
    def _pick_target(self):
        """选择目标网格"""
        selection = cmds.ls(selection=True, type='mesh')
        if not selection:
            self._log("Please select a mesh")
            return
        
        mesh = selection[0]
        try:
            success, message = self.plugin.set_target(mesh)
            if success:
                cmds.textField(self.target_field, edit=True, text=mesh)
                self._update_target_info()
                self._log("✓ " + message)
            else:
                self._log("✗ Error: " + message)
        except Exception as e:
            self._log("✗ Error: " + str(e))
    
    def _update_source_info(self):
        """更新源网格信息"""
        status = self.plugin.get_status()
        info_text = "Source: {} | Joints: {}".format(
            status['source'] or "None",
            status['source_joints']
        )
        cmds.text(self.source_field + "_info", edit=True, label=info_text)
    
    def _update_target_info(self):
        """更新目标网格信息"""
        status = self.plugin.get_status()
        info_text = "Target: {} | Joints: {}".format(
            status['target'] or "None",
            status['target_joints']
        )
        cmds.text(self.target_field + "_info", edit=True, label=info_text)
    
    def _toggle_search_fields(self, value):
        """切换搜索字段启用状态"""
        enable = bool(value)
        cmds.textField(self.search_field, edit=True, enable=enable)
        cmds.textField(self.replace_field, edit=True, enable=enable)
    
    def _copy_weights(self):
        """拷贝权重"""
        if not self.plugin.source_mesh or not self.plugin.target_mesh:
            self._log("✗ Please select both source and target meshes")
            return
        
        try:
            self._log("Copying weights...")
            
            search_replace = None
            if cmds.checkBox(self.use_search_check, query=True, value=True):
                search = cmds.textField(self.search_field, query=True, text=True)
                replace = cmds.textField(self.replace_field, query=True, text=True)
                if search and replace:
                    search_replace = (search, replace)
            
            success, fail = self.plugin.copy_weights(search_replace=search_replace)
            self._log("✓ Copy completed: {} success, {} failed".format(success, fail))
            
        except Exception as e:
            self._log("✗ Error: " + str(e))
            traceback.print_exc()
    
    def _mirror_weights(self):
        """镜像权重"""
        if not self.plugin.target_mesh:
            self._log("✗ Please select target mesh")
            return
        
        try:
            self._log("Mirror feature - coming soon!")
            
        except Exception as e:
            self._log("✗ Error: " + str(e))
    
    def _clear_selection(self):
        """清除选择"""
        self.plugin.source_mesh = None
        self.plugin.source_skin_cluster = None
        self.plugin.target_mesh = None
        self.plugin.target_skin_cluster = None
        
        cmds.textField(self.source_field, edit=True, text="")
        cmds.textField(self.target_field, edit=True, text="")
        cmds.text(self.source_field + "_info", edit=True, label="No source selected")
        cmds.text(self.target_field + "_info", edit=True, label="No target selected")
        
        self._log("Cleared all selections")
    
    def _log(self, message):
        """添加日志信息"""
        current = cmds.scrollField(self.log_text, query=True, text=True) or ""
        new_log = current + message + "\n"
        cmds.scrollField(self.log_text, edit=True, text=new_log)


# 全局UI实例
_ui_instance = None


def show_ui():
    """显示UI窗口"""
    global _ui_instance
    if _ui_instance is None:
        _ui_instance = CopySkinWeightsUI()
    _ui_instance.show()


def get_ui_instance():
    """获取UI实例"""
    global _ui_instance
    return _ui_instance
