# -*- coding: utf-8 -*-
"""
Maya 2018 Copy Skin Weights Plugin
拷贝蒙皮权重插件 - 支持在不同网格之间复制和镜像蒙皮权重

Author: hansencamryn75
Version: 1.0.0
Maya Version: 2018
"""

import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim
import maya.mel as mel
from functools import wraps
import traceback


class CopySkinWeights(object):
    """蒙皮权重拷贝核心功能类"""
    
    def __init__(self):
        self.source_mesh = None
        self.source_skin_cluster = None
        self.target_mesh = None
        self.target_skin_cluster = None
        
    @staticmethod
    def undoable(func):
        """装饰器: 包装撤销/重做"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            cmds.undoInfo(openChunk=True)
            try:
                result = func(*args, **kwargs)
                cmds.undoInfo(closeChunk=True)
                return result
            except Exception as e:
                cmds.undoInfo(closeChunk=True)
                raise e
        return wrapper
    
    def get_skin_cluster(self, mesh):
        """获取网格的蒙皮簇"""
        if not cmds.objExists(mesh):
            raise RuntimeError("Mesh does not exist: {}".format(mesh))
        
        # 获取Shape节点
        shapes = cmds.listRelatives(mesh, shapes=True, type='mesh')
        if not shapes:
            raise RuntimeError("No mesh shape found: {}".format(mesh))
        
        shape = shapes[0]
        
        # 查找连接的skinCluster
        history = cmds.listHistory(shape, pruneDagObjects=True)
        skin_clusters = cmds.ls(history, type='skinCluster')
        
        if not skin_clusters:
            raise RuntimeError("No skinCluster found on: {}".format(mesh))
        
        return skin_clusters[0]
    
    def get_joints(self, skin_cluster):
        """获取蒙皮簇的所有关节"""
        geometry = cmds.skinCluster(skin_cluster, query=True, geometry=True)
        joints = cmds.skinCluster(skin_cluster, query=True, influence=True)
        return joints if joints else []
    
    def set_source(self, mesh):
        """设置源网格"""
        try:
            self.source_mesh = mesh
            self.source_skin_cluster = self.get_skin_cluster(mesh)
            joints = self.get_joints(self.source_skin_cluster)
            return True, "Source set: {} ({} joints)".format(mesh, len(joints))
        except Exception as e:
            self.source_mesh = None
            self.source_skin_cluster = None
            return False, str(e)
    
    def set_target(self, mesh):
        """设置目标网格"""
        try:
            self.target_mesh = mesh
            self.target_skin_cluster = self.get_skin_cluster(mesh)
            joints = self.get_joints(self.target_skin_cluster)
            return True, "Target set: {} ({} joints)".format(mesh, len(joints))
        except Exception as e:
            self.target_mesh = None
            self.target_skin_cluster = None
            return False, str(e)
    
    @undoable
    def copy_weights(self, search_replace=None, mirror_axis='x'):
        """
        拷贝权重
        
        Args:
            search_replace: 元组 (搜索字符串, 替换字符串) 用于关节名称映射
            mirror_axis: 镜像轴 ('x', 'y', 'z')
        
        Returns:
            成功的顶点数, 失败的顶点数
        """
        if not self.source_skin_cluster or not self.target_skin_cluster:
            raise RuntimeError("Source and target must be set first")
        
        # 获取源和目标的关节
        source_joints = self.get_joints(self.source_skin_cluster)
        target_joints = self.get_joints(self.target_skin_cluster)
        
        # 创建关节映射字典
        joint_map = {}
        for src_joint in source_joints:
            joint_name = src_joint
            
            # 应用搜索替换
            if search_replace:
                search, replace = search_replace
                joint_name = joint_name.replace(search, replace)
            
            # 检查目标关节是否存在
            if joint_name in target_joints:
                joint_map[src_joint] = joint_name
            else:
                om.MGlobal.displayWarning("Target joint not found: {}".format(joint_name))
        
        # 获取源网格顶点数
        source_shape = cmds.listRelatives(self.source_mesh, shapes=True)[0]
        target_shape = cmds.listRelatives(self.target_mesh, shapes=True)[0]
        
        source_verts = cmds.polyEvaluate(source_shape, vertex=True)
        target_verts = cmds.polyEvaluate(target_shape, vertex=True)
        
        success_count = 0
        fail_count = 0
        
        # 对每个顶点拷贝权重
        for vert_idx in range(target_verts):
            try:
                target_vert = "{}.vtx[{}]".format(self.target_mesh, vert_idx)
                
                # 查找最近的源顶点 (基于世界坐标)
                target_pos = cmds.xform(target_vert, query=True, worldSpace=True, translation=True)
                closest_src_vert = self._find_closest_vertex(source_shape, target_pos)
                
                if closest_src_vert is None:
                    fail_count += 1
                    continue
                
                source_vert = "{}.vtx[{}]".format(self.source_mesh, closest_src_vert)
                
                # 获取源顶点的权重
                weights_data = cmds.skinPercent(
                    self.source_skin_cluster,
                    source_vert,
                    query=True,
                    value=True
                )
                
                # 应用到目标顶点
                transform_data = []
                for i, src_joint in enumerate(source_joints):
                    if src_joint in joint_map:
                        tgt_joint = joint_map[src_joint]
                        transform_data.append((tgt_joint, weights_data[i]))
                
                # 设置权重
                cmds.skinPercent(
                    self.target_skin_cluster,
                    target_vert,
                    transformValue=transform_data,
                    normalize=True
                )
                success_count += 1
                
            except Exception as e:
                fail_count += 1
                om.MGlobal.displayWarning("Failed to copy weight for vertex {}: {}".format(vert_idx, str(e)))
        
        return success_count, fail_count
    
    def _find_closest_vertex(self, mesh_shape, target_pos):
        """查找距离目标位置最近的顶点索引"""
        try:
            mesh = cmds.listRelatives(mesh_shape, parent=True)[0]
            verts = cmds.polyEvaluate(mesh_shape, vertex=True)
            
            min_distance = float('inf')
            closest_vert = None
            
            for vert_idx in range(verts):
                vert = "{}.vtx[{}]".format(mesh, vert_idx)
                vert_pos = cmds.xform(vert, query=True, worldSpace=True, translation=True)
                
                distance = sum((target_pos[i] - vert_pos[i]) ** 2 for i in range(3))
                
                if distance < min_distance:
                    min_distance = distance
                    closest_vert = vert_idx
            
            return closest_vert
        except:
            return None
    
    def get_status(self):
        """获取当前状态"""
        return {
            'source': self.source_mesh,
            'source_joints': len(self.get_joints(self.source_skin_cluster)) if self.source_skin_cluster else 0,
            'target': self.target_mesh,
            'target_joints': len(self.get_joints(self.target_skin_cluster)) if self.target_skin_cluster else 0
        }


# 全局实例
_copy_skin_instance = CopySkinWeights()


def get_plugin_instance():
    """获取插件实例"""
    return _copy_skin_instance
