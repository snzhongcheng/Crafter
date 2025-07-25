from common.i18n.dictionary import preprocess_dictionary

dictionary = {
    "zh_CN": {
        "Plans":"方案",
        # ==========面板==========
            # ==========加载==========
                # ==========加载环境==========
        "Environment":"环境",
        "Load Environment":"加载环境",
            # ==========导入世界==========
        "Import World":"导入世界",
        "Import Editable Area":"导入可编辑区域",
        "Minecraft Saves":"Minecraft存档",
        "World path":"存档地址",
        "XYZ-1":"坐标1",
        "XYZ-2":"坐标2",
        "Point Cloud Mode":"点云模式",
        "History Worlds":"历史世界",
        "To use the history world settings":"使用历史世界设置",
        "Open WorldImporter folder":"打开WorldImporter文件夹",
        "Your world path is not in game folder,select jar.":"您的存档地址不在游戏文件夹中,选择jar文件",
        "Jar Path":"Jar路径",
        "Custom Mods":"自定义模组",
        "Mods Path":"模组路径",
        "Versions":"版本列表",
        "Resources List":"资源包列表",
        "Chunk Precision":"区块精度导出",
        "Keep Boundary":"保留边界",
        "Strict Surface Pruning":"严格剔除面",
        "Cull Cave":"剔除洞穴",
        "Export Light Block":"导出光源方块",
        "Only Export Light Block":"只导出光源方块",
        "Light Block Size":"光源方块大小",
        "Allow Double Face":"允许重叠面",
        "As Chunk":"分块",
        "Chunk Size":"分块大小",
        "Chunk Number to Release":"释放内存区块数",
        "Biome Colors":"群系着色",
        "Underwater LOD":"水下LOD",
        "List of Blocks not LOD":"不LOD方块列表",
        "Open no lod blocks folder":"打开不LOD方块文件夹",
        "Greedy Mesh":"面合并",
        "LOD Auto Center":"LOD自动中心",
        "LOD Center X":"LOD中心X",
        "LOD Center Z":"LOD中心Z",
        "Max LOD Level":"最大LOD等级",
        "No LOD Distance":"无LOD距离",
        "LOD1 Distance":"LOD1距离",
        "LOD2 Distance":"LOD2距离",
        "LOD3 Distance":"LOD3距离",
        "Game Resources":"游戏资源包",
            # ==========替换资源包==========
        "Replace Resources":"替换资源包",
        "Resources":"资源包预设",
        "Vanilla":"原版",
        "Open Resources Plans":"打开资源包预设列表文件夹",
        "Reload Resources Plans":"刷新资源预设列表",
        "Resource":"资源包",
        "Up resource's priority":"提高资源包优先级",
        "Down resource's priority":"降低资源包优先级",
        "Texture Interpolation":"纹理插值",
        "Texture interpolation method":"纹理插值类型",
        "Set Texture Interpolation":"设置纹理插值",
            # ==========加载材质==========
        "Load Materials":"加载材质",
        "Materials":"材质",
        "Parser":"解析器",
        "PBR Parser":"PBR解析器",
        "Mix Parser":"混合解析器",
        "Materials index":"材质索引",
        "Open Materials":"打开材质文件夹",
        "Reload Materials":"刷新材质列表",
        "Load Material":"加载材质",
        "Classification Basis":"材质分类依据",
        "default":"默认",
        "Open Classification Basis":"打开材质分类依据文件夹",
        "Reload Classification Basis":"刷新材质分类依据列表",
        "Crafter Materials Settings":"Crafter材质设置",
            # ==========导入物品==========
        "Minecraft Item":"Minecraft物品",
        # ==========操作介绍==========
            # ==========导入世界==========
        "Import world":"导入世界",
        "Import World":"导入世界",
        "History":"历史",
        "Area Selector":"坐标选择器",
        "Import the surface world":"导入表面世界",
        "Import the solid area":"导入实心区域",
        "Starting coordinates":"起始坐标",
        "Ending coordinates":"结束坐标",
        "Enable this option when reporting a bug and include the shell output content":"反馈bug时,请启用此项并附带shell输出的内容",
            # ==========加载材质==========
        "Parsed Normal Strength":"解析法向强度",
        "How to parse PBR texture(and normal texture)":"如何解析PBR贴图(以及法线贴图)",
        "(1-R)**2,G as F0,Emission in Alpha":"(1-R)**2,G为F0,Alpha为自发光",
        "(1-R)**2,G as Metallic,Emission in Alpha":"(1-R)**2,G为金属度,Alpha为自发光",
        "1-R,G as Metallic,Emission in B":"1-R,G为金属度,B为自发光",
        "1-R,G as Metallic,No Emission":"1-R,G为金属度,无自发光",
        "Load material":"加载材质",
        "Classification basis":"材质分类依据",
        "The Crafter-time node can provide the current second count to material nodes (dynamic textures and water flowing), but it will reduce the preview frame rate. It is recommended to remove it during previews and add it back before rendering":"Crafter-time节点能够为材质节点提供当前秒数(动态纹理、流动水),但会使预览帧数降低.建议在预览时移除,渲染前添加",
        "Load Parallax": "加载视差",
        "Remove Parallax": "移除视差",
        "Parallax Setting": "视差设置",
        "Iterations": "迭代次数",
            # ==========导入物品==========
        "Import Minecraft item":"导入Minecraft物品",
            # ==========其余功能==========
                # ==========资产==========
                "Asset":"资产",
                # ==========替换资源包==========
        "Replace resources,but can only replace textures with the same name":"替换资源包,但只能替换同名纹理",
        "Set texture interpolation":"设置纹理插值",
        "Custome Size":"自定义尺寸",
        # ==========节点接口==========
        "Normal Alpha":"法向Alpha",
        "Parsed Normal":"已解析法向",
        "Porosity":"孔隙率",
        # ==========提示==========
        "Path not found!":"路径未找到!",
        "It's not a jar file!":"这不是一个jar文件!",
        "It's not a folder!":"这不是一个文件夹!",
        "No Selected Environment!":"无选中环境!",
        "Can't find any versions!":"找不到任何版本!",
        "It's not a world path!":"这不是一个世界路径!",
        "Please set the save file into the Minecraft game folder!":"请将存档文件放入Minecraft游戏文件夹!",
        "WorldImporter didn't export obj!":"WorldImporter没有导出obj!",
        "Haven't history worlds":"无历史世界记录",
        "Import time: ":"导入用时: ",
        ", Material time: ":", 材质用时: ",
        ", Environment time: ":", 环境用时: ",
            # ==========UV==========
        "No active object found":"未找到活动对象",
        "Active object must be a mesh":"活动对象必须是网格模型",
        "Active object has no faces":"活动对象没有面数据",
        "No active UV map found":"未找到激活的UV贴图"
    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_HANS"] = dictionary["zh_CN"]
