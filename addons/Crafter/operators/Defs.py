import bpy
import os
import subprocess
import platform
import json
import zipfile
import sqlite3
import ctypes
import tempfile
import textwrap

# 只在Windows上导入wintypes
if platform.system() == "Windows":
    from ctypes import wintypes

from ..config import __addon_name__
from ....common.i18n.i18n import i18n
from bpy.props import *
from ..__init__ import dir_blend_append, dir_init_main
from..properties import dirs_temp

donot = ["Crafter Materials Settings"]
len_color_jin = 21
name_library = "Crafter"


def load_icon_from_zip(zip_path, icons, name_icons, index):
    dir_temp = tempfile.mkdtemp()
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        if "pack.png" in zip_file.namelist():
            zip_file.extract("pack.png", dir_temp)
            have = True
        else:
            have = False
    dir_icon = os.path.join(dir_temp, "pack.png")
    icons.load(name_icons + "_icon_" + str(index), dir_icon, 'IMAGE')
    dirs_temp.append(dir_temp)
    return have

def get_dir_saves(context):
    addon_prefs = context.preferences.addons[__addon_name__].preferences

    dir_root = addon_prefs.History_World_Roots_List[addon_prefs.History_World_Roots_List_index].name
    dir_undivided_saves = os.path.join(dir_root,"saves")
    if os.path.exists(dir_undivided_saves):
        
        return dir_undivided_saves
    else:
        dir_verisons = dir_root_2_dir_versions(dir_root)
        dir_version = os.path.join(dir_verisons,addon_prefs.History_World_Versions_List[addon_prefs.History_World_Versions_List_index].name)
        dir_saves = dir_version_2_dir_saves(dir_version)
        
        return dir_saves

def get_dir_save(context):
    addon_prefs = context.preferences.addons[__addon_name__].preferences

    dir_save = os.path.join(get_dir_saves(context), addon_prefs.History_World_Saves_List[addon_prefs.History_World_Saves_List_index].name)
    
    return dir_save

def dir_root_2_dir_versions(dir_root):
    list_folder_minecraft = os.listdir(dir_root)
    if "Instances" in list_folder_minecraft:
        dir_versions = os.path.join(dir_root, "Instances")
    elif "profiles" in list_folder_minecraft:
        dir_versions = os.path.join(dir_root, "profiles")
    else:
        dir_versions = os.path.join(dir_root, "versions")
    return dir_versions

def dir_version_2_dir_saves(dir_version):
    list_floder_version = os.listdir(dir_version)
    if ("instance.cfg" in list_floder_version) and ("mmc-pack.json" in list_floder_version):
        dir_saves = os.path.join(dir_version, "minecraft", "saves")
    else:
        dir_saves = os.path.join(dir_version, "saves")
    return dir_saves

def dir_back_saves_2_dir_version(dir_back_saves):
    dir_back_back_saves = os.path.dirname(dir_back_saves)
    list_floder_back_back_saves = os.listdir(dir_back_back_saves)
    if ("instance.cfg" in list_floder_back_back_saves) and ("mmc-pack.json" in list_floder_back_back_saves):
         dir_versions = dir_back_back_saves
    else:
        dir_versions = dir_back_saves
    return dir_versions

def dir_version_2_dir_jar(dir_version):
    dir_versions = os.path.dirname(dir_version)
    name_versions = os.path.basename(dir_versions)
    if name_versions == "Instances":
        list_floder_version = os.listdir(dir_version)
        if ("instance.cfg" in list_floder_version) and ("mmc-pack.json" in list_floder_version):
            
            dir_jar = ""# 暂未支持prime laucher（似乎与官方启动器使用同样的jar存储方式）
        else:
            dir_json_Instance = os.path.join(dir_version, "minecraftinstance.json")
            with open(dir_json_Instance, "r", encoding="utf-8") as file:
                json_instance = json.load(file)
            json_versionjson = json.loads(json_instance["baseModLoader"]["versionJson"])
            name_folder = json_versionjson["id"]
            name_jar = name_folder + ".jar"
            dir_minecraft = os.path.dirname(dir_versions)
            dir_jar = os.path.join(dir_minecraft, "Install", "versions", name_folder, name_jar)
    elif name_versions == "profiles":
        name_version = os.path.basename(dir_version)
        dir_ModrinthApp = os.path.dirname(dir_versions)
        dir_db_app = os.path.join(dir_ModrinthApp, "app.db")
        dir_meta = os.path.join(dir_ModrinthApp, "meta")
        dir_versions_meta = os.path.join(dir_meta, "versions")

        db_app = sqlite3.connect(dir_db_app)
        cursor = db_app.cursor()
        cursor.execute("SELECT * FROM profiles")
        rows = cursor.fetchall()
        for row in rows:
            if row[0] == name_version:
                if row[6] == None:
                    name_jar = row[4]
                else:
                    name_jar = row[4] + "-" + row[6]
                break
        dir_jar = os.path.join(dir_versions_meta, name_jar, name_jar + ".jar")
    else:
        name_version = os.path.basename(dir_version)
        dir_jar = os.path.join(dir_version, name_version+".jar")
    return dir_jar

def reloadwindow():
    bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP")

def view_2_active_object(context):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                # 需要同时覆盖window/area/region三个上下文参数
                for region in area.regions:
                    if region.type == 'WINDOW':  # 只处理主区域
                        try:
                            with context.temp_override(window=window, area=area, region=region):
                                bpy.ops.view3d.view_selected()
                        except:
                            pass
                        break
    reloadwindow()

def draw_multiline_label( text, parent,context):
    # 获取当前面板宽度和UI缩放比例
    panel_width = context.region.width
    
    # 计算有效字符宽度（考虑UI缩放对字体大小的影响）
    chars_per_line = max(10, int(panel_width / 50))  # 防下限
    
    # 使用textwrap分割文本
    wrapper = textwrap.TextWrapper(
        width=chars_per_line,
        break_long_words=True,
        replace_whitespace=False
    )
    lines = wrapper.wrap(text=text)
    
    # 动态生成多行标签
    for line in lines:
        parent.label(text=line)

def run_as_admin_and_wait(exe_path, work_dir=None, shell=False):
    """
    跨平台运行可执行文件并等待完成
    Windows: 使用管理员权限运行
    macOS/Linux: 使用普通权限运行
    """
    current_platform = platform.system()
    print(f"[DEBUG] Platform detected: {current_platform}")
    print(f"[DEBUG] Executable path: {exe_path}")
    print(f"[DEBUG] Working directory: {work_dir}")

    if current_platform == "Windows":
        print("[DEBUG] Using Windows execution path")
        return _run_windows_admin(exe_path, work_dir, shell)
    elif current_platform == "Darwin":  # macOS
        print("[DEBUG] Using macOS execution path")
        return _run_macos(exe_path, work_dir, shell)
    else:  # Linux或其他Unix系统
        print(f"[DEBUG] Using Unix execution path for {current_platform}")
        return _run_unix(exe_path, work_dir, shell)

def _run_windows_admin(exe_path, work_dir=None, shell=False):
    """Windows平台使用管理员权限运行"""
    # 只在Windows平台上执行
    if platform.system() != "Windows":
        return False

    try:
        # 确保wintypes可用
        if 'wintypes' not in globals():
            from ctypes import wintypes

        # 定义SHELLEXECUTEINFOW结构体
        class SHELLEXECUTEINFOW(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("fMask", ctypes.c_ulong),
                ("hwnd", wintypes.HWND),
                ("lpVerb", wintypes.LPCWSTR),
                ("lpFile", wintypes.LPCWSTR),
                ("lpParameters", wintypes.LPCWSTR),
                ("lpDirectory", wintypes.LPCWSTR),
                ("nShow", ctypes.c_int),
                ("hInstApp", wintypes.HINSTANCE),
                ("lpIDList", ctypes.c_void_p),
                ("lpClass", wintypes.LPCWSTR),
                ("hKeyClass", wintypes.HKEY),
                ("dwHotKey", wintypes.DWORD),
                ("hIcon", wintypes.HANDLE),
                ("hProcess", wintypes.HANDLE)
            ]

        # 配置结构体参数
        sei = SHELLEXECUTEINFOW()
        sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFOW)
        sei.fMask = 0x00000040  # SEE_MASK_NOCLOSEPROCESS
        sei.lpVerb = 'runas'    # 管理员权限
        sei.lpFile = exe_path.replace("\\", "\\\\")  # 处理Windows路径转义
        sei.lpDirectory = work_dir.replace("\\", "\\\\") if work_dir else None
        sei.nShow = shell  # SW_SHOWNORMAL

        # 调用ShellExecuteExW
        if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
            error_code = ctypes.GetLastError()
            error_msg = ctypes.FormatError(error_code)
            return False

        # 等待进程结束
        WAIT_TIMEOUT = 0x00000102
        WAIT_OBJECT_0 = 0x0
        while True:
            wait_result = ctypes.windll.kernel32.WaitForSingleObject(sei.hProcess, 100)  # 100ms间隔
            if wait_result == WAIT_OBJECT_0:
                break
            elif wait_result == WAIT_TIMEOUT:
                continue
            else:
                ctypes.windll.kernel32.CloseHandle(sei.hProcess)
                return False

        # 获取退出码
        exit_code = wintypes.DWORD()
        ctypes.windll.kernel32.GetExitCodeProcess(sei.hProcess, ctypes.byref(exit_code))
        ctypes.windll.kernel32.CloseHandle(sei.hProcess)

        return exit_code.value == 0

    except Exception as e:
        print(f"Windows execution error: {e}")
        return False

def _run_macos(exe_path, work_dir=None, shell=False):
    """macOS平台运行"""
    try:
        # 检查是否是Windows可执行文件，如果是则替换为macOS版本
        if exe_path.endswith("WorldImporter.exe"):
            macos_exe_path = exe_path.replace("WorldImporter.exe", "WorldImporter")
            if os.path.exists(macos_exe_path):
                exe_path = macos_exe_path
                print("macOS")  # 输出给Blender
            else:
                print(f"macOS executable not found: {macos_exe_path}")
                return False

        print(f"[DEBUG] Final executable path: {exe_path}")
        print(f"[DEBUG] Working directory: {work_dir}")

        # 检查配置文件是否存在
        config_path = os.path.join(work_dir, "config_macos", "config.json")
        print(f"[DEBUG] Expected config path: {config_path}")
        if os.path.exists(config_path):
            print(f"[DEBUG] Config file exists and size: {os.path.getsize(config_path)} bytes")
        else:
            print(f"[DEBUG] Config file does not exist!")

        # 使用subprocess运行程序
        process = subprocess.Popen(
            [exe_path],
            cwd=work_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # 等待进程完成
        stdout, stderr = process.communicate()

        # 打印输出（可选）
        if stdout:
            print("=== STDOUT ===")
            print(stdout.decode('utf-8'))
        if stderr:
            print("=== STDERR ===")
            print(stderr.decode('utf-8'))

        print(f"[DEBUG] Process return code: {process.returncode}")
        return process.returncode == 0

    except Exception as e:
        print(f"macOS execution error: {e}")
        import traceback
        traceback.print_exc()
        return False

def _run_unix(exe_path, work_dir=None, shell=False):
    """Unix/Linux平台运行"""
    try:
        process = subprocess.Popen(
            [exe_path],
            cwd=work_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if stdout:
            print(stdout.decode('utf-8'))
        if stderr:
            print(stderr.decode('utf-8'))

        return process.returncode == 0

    except Exception as e:
        print(f"Unix execution error: {e}")
        return False


def open_folder(folder_path: str):
    '''
    打开目标文件夹
    folder_path: 文件夹路径
    '''
    if platform.system() == "Windows":
        os.startfile(folder_path)
    elif platform.system() == "Darwin":  # MacOS
        subprocess.run(["open", folder_path])
    else:  # Linux
        subprocess.run(["xdg-open", folder_path])

def make_dict_together(dict1, dict2):
    '''
    递归合并json最底层的键值对
    dict1: 字典1
    dict2: 字典2
    '''
    for key, value in dict2.items():
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(value, dict):
                make_dict_together(dict1[key], value)
            elif isinstance(dict1[key], list) and isinstance(value, list):
                dict1[key] = list(set(dict1[key] + value))
            else:
                dict1[key] = value
        else:
            dict1[key] = value
    return dict1

def unzip(zip_path, extract_to):
    '''
    解压压缩文件
    zip_path: 压缩文件路径
    extract_to: 解压路径
    '''
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def add_node_moving_texture(node_tex, nodes, links):
    '''
    为基础色节点添加动态纹理节点并连接
    node_tex_base: 基础纹理节点
    nodes: 目标材质节点组
    links:目标材质连接组
    return:动态纹理节点
    '''
    dir_image = os.path.dirname(node_tex.image.filepath)
    dir_mcmeta = os.path.join(bpy.path.abspath(dir_image), fuq_bl_dot_number(node_tex.image.name) + ".mcmeta")
    if os.path.exists(dir_mcmeta):
        node_Moving_texture = nodes.new(type="ShaderNodeGroup")
        node_Moving_texture.location = (node_tex.location.x - 200, node_tex.location.y)
        node_Moving_texture.node_tree = bpy.data.node_groups["Crafter-Moving_texture"]
        try:
            with open(dir_mcmeta, 'r', encoding='utf-8') as file:
                mcmeta = json.load(file)
                frametime = mcmeta["animation"]["frametime"]
                node_Moving_texture.inputs["frametime"].default_value = frametime
        except:
            pass
        try:
            with open(dir_mcmeta, 'r', encoding='utf-8') as file:
                mcmeta = json.load(file)
                frametime = mcmeta["animation"]["interpolate"]
                node_Moving_texture.inputs["interpolate"].default_value = frametime
        except:
            pass
        if not node_tex.image.size[0] == 0:
            node_Moving_texture.inputs["row"].default_value = node_tex.image.size[1] / node_tex.image.size[0]
        else:
            node_Moving_texture.inputs["row"].default_value = 1
        links.new(node_Moving_texture.outputs["Vector"], node_tex.inputs["Vector"])
        return node_Moving_texture

def fuq_bl_dot_number(name: str):
    '''
    去除blender中重复时烦人的.xxx
    name: 待处理的字符串
    return: 处理后的字符串
    '''
    last_dot_index = name.rfind('.')
    if not last_dot_index == -1:
        if all("0" <= i <= "9" for i in name[last_dot_index + 1:]):
            name = name[:last_dot_index]
    return name

def add_to_mcmts_collection(object,context):
    '''
    object: 目标对象
    context: 目标上下文
    '''
    if object.type == "MESH":
        list_name_context_material = []
        for context_material in bpy.data.materials:
            list_name_context_material.append(context_material.name)
        list_name_object_material = []
        for material_object in object.data.materials:
            list_name_object_material.append(material_object.name)
        if (object.name not in donot) and object.type == "MESH" and object.data.materials:
            for name_material in list_name_object_material:
                if (name_material not in context.scene.Crafter_mcmts) and (name_material not in donot):
                    new_mcmt = context.scene.Crafter_mcmts.add()
                    new_mcmt.name = name_material
        for i in range(len(context.scene.Crafter_mcmts)-1,-1,-1):
            if context.scene.Crafter_mcmts[i].name not in list_name_context_material:
                context.scene.Crafter_mcmts.remove(i)

def add_to_crafter_mcmts_collection(object,context):
    '''
    object: 目标对象
    context: 目标上下文
    '''
    if object.type == "MESH":
        list_name_context_material = []
        for context_material in bpy.data.materials:
            list_name_context_material.append(context_material.name)
        list_name_object_material = []
        for object_material in object.data.materials:
            list_name_object_material.append(object_material.name)
        if (object.name not in donot) and object.type == "MESH" and object.data.materials:
            for name_material in list_name_object_material:
                if (name_material not in context.scene.Crafter_crafter_mcmts) and (name_material not in donot):
                    new_mcmt = context.scene.Crafter_crafter_mcmts.add()
                    new_mcmt.name = name_material
        for i in range(len(context.scene.Crafter_crafter_mcmts)-1,-1,-1):
            if context.scene.Crafter_crafter_mcmts[i].name not in list_name_context_material:
                context.scene.Crafter_crafter_mcmts.remove(i)
                
def find_CI_group(classification_list,real_block_name,group_CI):
    '''
    classification_list: 分类列表
    real_block_name: 真实方块名称
    group_CI: CI节点组
    '''
    found = False
    for group_name in classification_list:
        if group_name == "ban" or group_name == "ban_keyw":
            continue
        banout = False
        if "ban_keyw" in classification_list[group_name]:
            for item in classification_list[group_name]["ban_keyw"]:
                if item in real_block_name:
                    banout = True
                    break
        if banout:
            continue
        if "ban" in classification_list[group_name]:
            for item in classification_list[group_name]["ban"]:
                if item == real_block_name:
                    banout = True
                    break
        if banout:
            continue
        if "full" in classification_list[group_name]:
            for item in classification_list[group_name]["full"]:
                if item == real_block_name:
                    name_node = "CI-" + group_name
                    if name_node in bpy.data.node_groups:
                        group_CI.node_tree = bpy.data.node_groups[name_node]
                    else:
                        group_CI.node_tree = bpy.data.node_groups["CI-"]
                    found = True
                    break
        if found:
            break
        if "keyw" in classification_list[group_name]:
            for item in classification_list[group_name]["keyw"]:
                if item in real_block_name:
                    name_node = "CI-" + group_name
                    if name_node in bpy.data.node_groups:
                        group_CI.node_tree = bpy.data.node_groups[name_node]
                    else:
                        group_CI.node_tree = bpy.data.node_groups["CI-"]
                    found = True
                    break
        if found:
            break
    if not found:
                group_CI.node_tree = bpy.data.node_groups["CI-"]

def link_CI_output(group_CI, node_output_EEVEE, node_output_Cycles, links):
    '''
    group_CI: 材质组节点
    node_output_EEVEE: EEVEE输出节点
    node_output_Cycles: Cycles输出节点
    nodes: 目标材质节点组
    links:目标材质连接组
    '''
    if "EEVEE-Surface" in group_CI.outputs:
        links.new(group_CI.outputs["EEVEE-Surface"], node_output_EEVEE.inputs["Surface"])
    if "EEVEE-Volume" in group_CI.outputs: 
        links.new(group_CI.outputs["EEVEE-Volume"], node_output_EEVEE.inputs["Volume"])
    if "EEVEE-Displacement" in group_CI.outputs: 
        links.new(group_CI.outputs["EEVEE-Displacement"], node_output_EEVEE.inputs["Displacement"])
    if "EEVEE-Thickness" in group_CI.outputs: 
        if "Thickness" in node_output_EEVEE.inputs:
            links.new(group_CI.outputs["EEVEE-Thickness"], node_output_EEVEE.inputs["Thickness"])
        
    if "Cycles-Surface" in group_CI.outputs: 
        links.new(group_CI.outputs["Cycles-Surface"], node_output_Cycles.inputs["Surface"])
    if "Cycles-Volume" in group_CI.outputs: 
        links.new(group_CI.outputs["Cycles-Volume"], node_output_Cycles.inputs["Volume"])
    if "Cycles-Displacement" in group_CI.outputs: 
        links.new(group_CI.outputs["Cycles-Displacement"], node_output_Cycles.inputs["Displacement"])
    if "Cycles-Thickness" in group_CI.outputs: 
        if "Thickness" in node_output_Cycles.inputs:
            links.new(group_CI.outputs["Cycles-Thickness"], node_output_Cycles.inputs["Thickness"])

def add_node_parser(group_CI, nodes, links):
    '''
    gout_CI: 材质组节点
    nodes: 目标材质节点组
    links:目标材质连接组
    return: node_C_PBR_Parser
    '''
    node_C_PBR_Parser = nodes.new(type="ShaderNodeGroup")
    node_C_PBR_Parser.location = (group_CI.location.x - 200, group_CI.location.y - 160)
    node_C_PBR_Parser.node_tree = bpy.data.node_groups["C-PBR_Parser"]
    for output in node_C_PBR_Parser.outputs:
        if output.name in group_CI.inputs:
            links.new(output, group_CI.inputs[output.name])
    return node_C_PBR_Parser

def load_normal_and_PBR(node_tex_base, nodes, links):
    '''
    以基础色节点添加法向贴图节点和PBR贴图节点、连接并添加动态纹理节点
    node_tex_base: 基础色节点
    nodes: 目标材质节点组
    links:目标材质连接组
    '''
    node_tex_normal = None
    node_tex_PBR = None
    if node_tex_base != None:
        name_image = fuq_bl_dot_number(node_tex_base.image.name)
        name_block = name_image[:-4]
        dir_image = os.path.dirname(node_tex_base.image.filepath)
        dir_n = os.path.join(dir_image,name_block + "_n.png")
        dir_s = os.path.join(dir_image,name_block + "_s.png")
        dir_a = os.path.join(dir_image,name_block + "_a.png")
        add_node_moving_texture(node_tex_base, nodes, links)
        node_tex_normal = None
        node_tex_PBR = None
        if os.path.exists(bpy.path.abspath(dir_n)):
            node_tex_normal = nodes.new(type="ShaderNodeTexImage")
            node_tex_normal.location = (node_tex_base.location.x, node_tex_base.location.y - 300)
            node_tex_normal.image = bpy.data.images.load(dir_n)
            node_tex_normal.interpolation = "Closest"
            bpy.data.images[node_tex_normal.image.name].colorspace_settings.name = "Non-Color"
            add_node_moving_texture(node_tex_normal, nodes, links)
        if os.path.exists(bpy.path.abspath(dir_s)):
            node_tex_PBR = nodes.new(type="ShaderNodeTexImage")
            node_tex_PBR.location = (node_tex_base.location.x, node_tex_base.location.y - 600)
            node_tex_PBR.image = bpy.data.images.load(dir_s)
            node_tex_PBR.interpolation = "Closest"
            bpy.data.images[node_tex_PBR.image.name].colorspace_settings.name = "Non-Color"
            add_node_moving_texture(node_tex_PBR, nodes, links)
        elif os.path.exists(bpy.path.abspath(dir_a)):
            node_tex_PBR = nodes.new(type="ShaderNodeTexImage")
            node_tex_PBR.location = (node_tex_base.location.x, node_tex_base.location.y - 600)
            node_tex_PBR.image = bpy.data.images.load(dir_a)
            node_tex_PBR.interpolation = "Closest"
            bpy.data.images[node_tex_PBR.image.name].colorspace_settings.name = "Non-Color"
            add_node_moving_texture(node_tex_PBR, nodes, links)
    return node_tex_normal, node_tex_PBR

def link_base_normal_PBR(node_tex_base, group_CI, links, node_C_PBR_Parser, node_tex_normal, node_tex_PBR):
    if node_tex_base != None:
        if "Base Color" in group_CI.inputs:
            links.new(node_tex_base.outputs["Color"], group_CI.inputs["Base Color"])
        if "Alpha" in group_CI.inputs:
            links.new(node_tex_base.outputs["Alpha"], group_CI.inputs["Alpha"])
    if node_tex_normal != None:
        links.new(node_tex_normal.outputs["Color"], node_C_PBR_Parser.inputs["Normal"])
        links.new(node_tex_normal.outputs["Alpha"], node_C_PBR_Parser.inputs["Normal Alpha"])
        if "Normal" in group_CI.inputs:
            links.new(node_tex_normal.outputs["Color"], group_CI.inputs["Normal"])
        if "Normal Alpha" in group_CI.inputs:
            links.new(node_tex_normal.outputs["Alpha"], group_CI.inputs["Normal Alpha"])
    if node_tex_PBR != None:
        links.new(node_tex_PBR.outputs["Color"], node_C_PBR_Parser.inputs["PBR"])
        links.new(node_tex_PBR.outputs["Alpha"], node_C_PBR_Parser.inputs["PBR Alpha"])
        if "PBR" in group_CI.inputs:
            links.new(node_tex_PBR.outputs["Color"], group_CI.inputs["PBR"])
        if "PBR Alpha" in group_CI.inputs:
            links.new(node_tex_PBR.outputs["Alpha"], group_CI.inputs["PBR Alpha"])

def add_Crafter_time(obj):
    if not "Crafter-time" in bpy.data.node_groups:
        with bpy.data.libraries.load(dir_blend_append, link=False) as (data_from, data_to):
            data_to.node_groups = ["Crafter-time"]
    # 检查是否已存在该节点修改器
    has_modifier = any(
        mod.type == 'NODES' and 
        mod.node_group == bpy.data.node_groups["Crafter-time"]
        for mod in obj.modifiers)

    if not has_modifier:
        # 添加几何节点修改器
        new_mod = obj.modifiers.new("Crafter-time", 'NODES')
        new_mod.node_group = bpy.data.node_groups["Crafter-time"]

def link_biome_tex(node_biomeTex, group_CI, links):
    if not node_biomeTex == None:
        for output in node_biomeTex.outputs:
            if output.name in group_CI.inputs:
                links.new(output, group_CI.inputs[output.name])

def reload_Undivided_Vsersions(context: bpy.types.Context,dir_versions):#刷新无版本隔离列表

        addon_prefs = context.preferences.addons[__addon_name__].preferences

        list_versions = os.listdir(dir_versions)
        addon_prefs.Undivided_Vsersions_List.clear()
        for version in list_versions:
            versionPath = os.path.join(dir_versions, version)
            undivided_version = addon_prefs.Undivided_Vsersions_List.add()
            undivided_version.name = versionPath
        if (len(addon_prefs.Undivided_Vsersions_List) - 1 < addon_prefs.Undivided_Vsersions_List_index) or (addon_prefs.Undivided_Vsersions_List_index < 0):
            addon_prefs.Undivided_Vsersions_List_index = 0
    
def node_moving_tex_info(node):
    info = [False,None,None,None]
    if node == None:
        return info
    if len(node.inputs["Vector"].links) >0:
        info[0] = True
        info[1] = node.inputs["Vector"].links[0].from_node.inputs["row"].default_value
        info[2] = node.inputs["Vector"].links[0].from_node.inputs["frametime"].default_value
        info[3] = node.inputs["Vector"].links[0].from_node.inputs["interpolate"].default_value

    return info

def creat_parallax_node(node_tex_base, node_tex_normal, iterations, smooth, info_moving_normal, nodes, links):
    # 创建框，方便清除
    node_frame = nodes.new(type="NodeFrame")
    location = [node_tex_base.location.x - 1000, node_tex_base.location.y]
    node_frame.location = location
    node_frame.label = "Crafter_Parallax"

    move = 190
    iterations = max(iterations, 1)
    node_final_depth = None
    input_lates = []

    while iterations > 0:
        iterations -= 1
        node_last = nodes.new("ShaderNodeGroup")
        node_last.node_tree = bpy.data.node_groups["CP-Steep_Steps_last"]
        node_last.location = location
        location[0] -= 1.5 * move# location
        node_last.parent = node_frame
        for input in input_lates:
            links.new(node_last.outputs["Current_Depth"], input)
        if node_final_depth == None:
            node_final_depth = node_last

        node_height = nodes.new("ShaderNodeTexImage")
        node_height.image = node_tex_normal.image
        node_height.location = location
        location[0] -= move# location
        node_height.parent = node_frame
        if smooth:
            node_height.interpolation = "Linear"
        else:
            node_height.interpolation = "Closest"
        links.new(node_height.outputs["Alpha"], node_last.inputs["Height"])

        node_first = nodes.new("ShaderNodeGroup")
        if info_moving_normal[0]:
            node_first.node_tree = bpy.data.node_groups["CP-Steep_Steps_first_moving"]
            node_first.inputs["row"].default_value = info_moving_normal[1]
            node_first.inputs["frametime"].default_value = info_moving_normal[2]
            node_first.inputs["interpolate"].default_value = info_moving_normal[3]
        else:
            node_first.node_tree = bpy.data.node_groups["CP-Steep_Steps_first"]
        links.new(node_first.outputs["Vector"], node_height.inputs["Vector"])
        node_first.location = location
        location[0] -= move# location
        node_first.parent = node_frame

        input_lates = [node_first.inputs["Current_Depth"],node_last.inputs["Current_Depth"]]

    return node_final_depth, node_frame

def create_parallax_final(node, node_final_depth, node_frame, info_moving, nodes, links):
    node_final = nodes.new("ShaderNodeGroup")
    if info_moving[0]:
        node_final.node_tree = bpy.data.node_groups["CP-Final_Parallax_moving"]
        node_final.inputs["row"].default_value = info_moving[1]
        node_final.inputs["frametime"].default_value = info_moving[2]
        node_final.inputs["interpolate"].default_value = info_moving[3]
    else:
        node_final.node_tree = bpy.data.node_groups["CP-Final_Parallax"]
    node_final.location = node.location.x - 600, node.location.y
    node_final.parent = node_frame

    links.new(node_final_depth.outputs["Current_Depth"], node_final.inputs["Depth"])
    links.new(node_final.outputs["UV"], node.inputs["Vector"])

    return node_final

def is_alpha_channel_all_one(image_node):
    """
    判断图像纹理节点的图像纹理的alpha通道是否全部为1。
    
    参数:
        image_node (ShaderNodeTexImage): 图像纹理节点对象。
        
    返回:
        bool: 如果所有alpha通道值都为1，则返回True；否则返回False。
    """
    if not image_node or image_node.type != 'TEX_IMAGE' or not image_node.image:
        return False  # 确保提供了有效的图像纹理节点
    
    image = image_node.image
    pixels = image.pixels[:]  # 获取像素数据（RGBA格式）

    for i in range(0, len(pixels), 4):
        alpha = pixels[i + 3]  # 提取alpha通道的值
        if alpha < 1.0 - 1e-6:  # 使用一个小的容差来处理浮点精度问题
            return False  # 发现非1的alpha值，直接返回False

    return True  # 所有alpha值都是1
