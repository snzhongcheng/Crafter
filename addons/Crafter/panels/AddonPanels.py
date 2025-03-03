import bpy
import os

from ..config import __addon_name__
from ....common.i18n.i18n import i18n
from ....common.types.framework import reg_order
from ..__init__ import dir_resourcepacks_plans

@reg_order(0)#==========导入预设面板==========
class VIEW3D_PT_CrafterPlans(bpy.types.Panel):
    bl_label = "Plans"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Crafter"
    def draw(self, context: bpy.types.Context):
        
        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        # layout.label(text="此版本为测试版本，请勿用于已编")
        # layout.label(text="辑的工程或作品工程。")
        # layout.separator()
        # layout.label(text="可以使用的仅有 修改插值类型 和")
        # layout.label(text="加载材质 功能，其余功能请勿使")
        # layout.label(text="用，以免造成破坏。")
        # layout.separator()
        # layout.label(text="使用方法：在导出obj后将tex中")
        # layout.label(text="的纹理替换为材质包的纹理。")
        # layout.separator()
        # layout.label(text="制作预设请复制后修改，否则会被")
        # layout.label(text="覆盖。")
        # layout.separator()
        # layout.label(text="导入obj世界。")
        # layout.separator()
        # layout.label(text="在选择了全部世界后点击 加载材")
        # layout.label(text="质。")
        # layout.separator()
        # layout.label(text="如果 雨 值修改后没效果请重复上")
        # layout.label(text="一个操作。")
        # layout.separator()
        # layout.label(text="由于不知道岩浆的纹理如何映射，所")
        # layout.label(text="以岩浆材质是有问题的。")
        # layout.separator()
        # layout.label(text="如有问题请在群里联系 少年忠城。")



    @classmethod
    def poll(cls, context: bpy.types.Context):
            return context.preferences.addons[__addon_name__].preferences.Plans
    
@reg_order(1)#==========导入世界面板==========
class VIEW3D_PT_CrafterImportWorld(bpy.types.Panel):
    bl_label = "Import World"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Crafter"
    def draw(self, context: bpy.types.Context):
        
        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        layout.prop(addon_prefs, "World_Path")

        cul_XYZ = layout.column(align=True)
        row_XYZ1 = cul_XYZ.row()
        row_XYZ1.prop(addon_prefs, "XYZ_1")
        row_XYZ2 = cul_XYZ.row()
        row_XYZ2.prop(addon_prefs, "XYZ_2")
        
        row_setting = layout.row()
        row_setting.prop(addon_prefs, "Point_Cloud_Mode")
        row_setting.operator("crafter.history_worlds_panel",icon="TIME",text="")
        
        row_ImportWorld = layout.row()
        row_ImportWorld.operator("crafter.import_surface_world",text="Import World")
        if addon_prefs.Point_Cloud_Mode:
            row_ImportWorld.operator("crafter.import_solid_area",text="Import Editable Area")

    @classmethod
    def poll(cls, context: bpy.types.Context):
            return context.preferences.addons[__addon_name__].preferences.Import_World

#==========导入资源包列表==========
class VIEW3D_UL_CrafterResources(bpy.types.UIList):
     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {"DEFAULT","COMPACT"}:
            layout.label(text=item.name)

class VIEW3D_UL_CrafterResourcesInfo(bpy.types.UIList):
     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        addon_prefs = context.preferences.addons[__addon_name__].preferences
        dir_resourcepacks = os.path.join(dir_resourcepacks_plans, addon_prefs.Resources_Plans_List[addon_prefs.Resources_Plans_List_index].name)
        dir_resourcepack = os.path.join(dir_resourcepacks, item.name)
        
        if self.layout_type in {"DEFAULT","COMPACT"}:
            item_name = ""
            i = 0
            while i < len(item.name):
                if item.name[i] == "§":
                    i+=1
                elif item.name[i] == ".":
                    break
                elif item.name[i] != "!":
                    item_name += item.name[i]
                i+=1
            # if "pack.png" in os.listdir(dir_resourcepack):
            #     layout.label(text=item_name,icon="crafter_resources" + item.name)
            # else:
            #     layout.label(text=item_name)
            layout.label(text=item_name)

@reg_order(2)#==========导入资源包面板==========
class VIEW3D_PT_CrafterImportResources(bpy.types.Panel):
    bl_label = "Import Resources"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Crafter"
    def draw(self, context: bpy.types.Context):
        
        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        row_Plans_List = layout.row()
        row_Plans_List.template_list("VIEW3D_UL_CrafterResources", "", addon_prefs, "Resources_Plans_List", addon_prefs, "Resources_Plans_List_index", rows=1)
        col_Plans_List_ops = row_Plans_List.column()
        col_Plans_List_ops.operator("crafter.open_resources_plans",icon="FILE_FOLDER",text="")
        col_Plans_List_ops.operator("crafter.reload_all",icon="FILE_REFRESH",text="")

        if len(addon_prefs.Resources_List) > 0:
            row_Resources_List = layout.row()
            row_Resources_List.template_list("VIEW3D_UL_CrafterResourcesInfo", "", addon_prefs, "Resources_List", addon_prefs, "Resources_List_index", rows=1)
            if len(addon_prefs.Resources_List) > 1:
                col_Resources_List_ops = row_Resources_List.column(align=True)
                col_Resources_List_ops.operator("crafter.up_resource",icon="TRIA_UP",text="")
                col_Resources_List_ops.operator("crafter.down_resource",icon="TRIA_DOWN",text="")
            
        row_Import_Resources = layout.row()
        row_Import_Resources.operator("crafter.import_resources")
        
        # row_Texture_Interpolation = layout.row(align=True)
        # row_Texture_Interpolation.prop(addon_prefs,"Texture_Interpolation")
        # row_Texture_Interpolation.operator("crafter.set_texture_interpolation")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.preferences.addons[__addon_name__].preferences.Import_Resources

#==========加载材质列表==========
class VIEW3D_UL_CrafterMaterials(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {"DEFAULT","COMPACT"}:
            layout.label(text=item.name)

class VIEW3D_UL_CrafterClassificationBasis(bpy.types.UIList):
     def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {"DEFAULT","COMPACT"}:
            layout.label(text=item.name)

@reg_order(3)#==========加载材质面板==========
class VIEW3D_PT_Materials(bpy.types.Panel):
    bl_label = "Load Materials"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Crafter"

    def draw(self, context: bpy.types.Context):

        layout = self.layout
        addon_prefs = context.preferences.addons[__addon_name__].preferences

        layout.prop(context.scene, "Crafter_rain")

        row_PBR_Parser = layout.row()
        row_PBR_Parser.prop(addon_prefs, "PBR_Parser")

        row_Materials_List = layout.row()
        row_Materials_List.template_list("VIEW3D_UL_CrafterMaterials", "", addon_prefs, "Materials_List", addon_prefs, "Materials_List_index", rows=1)
        col_Materials_List_ops = row_Materials_List.column()
        col_Materials_List_ops.operator("crafter.open_materials",icon="FILE_FOLDER",text="")
        col_Materials_List_ops.operator("crafter.reload_all",icon="FILE_REFRESH",text="")

        row_ops = layout.row()
        row_ops.operator("crafter.load_material")

        row_Classification_Basis = layout.row()
        row_Classification_Basis.template_list("VIEW3D_UL_CrafterClassificationBasis", "", addon_prefs, "Classification_Basis_List", addon_prefs, "Classification_Basis_List_index", rows=1)
        row_Classification_Basis_ops = row_Classification_Basis.column()
        row_Classification_Basis_ops.operator("crafter.open_classification_basis",icon="FILE_FOLDER",text="")
        row_Classification_Basis_ops.operator("crafter.reload_all",icon="FILE_REFRESH",text="")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.preferences.addons[__addon_name__].preferences.Load_Materials
