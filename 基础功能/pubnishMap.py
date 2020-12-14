# -*- coding: utf-8 -*-
import arcpy, os

# 将指定目录下所有的.mxd文档发布为地图服务
# folder：包含mxd文档的文件夹路径
# serviceDir：服务目录URL，例如http://localhost/arcgis/rest/services
# serviceFolder：服务所在文件夹，如果为空，则表示根目录
def PublishAll(folder, serviceDir, serviceFolder):
    print "检查文件夹路径……"
    if os.path.isdir(folder) == False:
        print "输入的文件夹路径无效！"
        return
    print "遍历文件夹……"
    files = os.listdir(folder)
    for f in files:
        if f.endswith(".mxd"):
            mxdPath = os.path.join(folder, f)
            print "publishing: " + f
            PublishMxd(mxdPath, serviceDir, serviceFolder)
        else:
            continue


# 将mxd文档发布为服务：1.将mxd转为msd；2.分析msd；3.发布msd
def PublishMxd(mxdPath, serviceDir, serviceFolder):
    # 检查mxd和msd文件是否存在
    print "检查文件路径……"
    if os.path.exists(mxdPath) == False:
        print "指定路径的mxd文档不存在！"
        return

    # 打开mxd文档
    try:
        print "正在打开mxd文档……"
        mxd = arcpy.mapping.MapDocument(mxdPath)
    except Exception, e:
        print "open mxd error: ", e
        return
    else:
        print "mxd文档打开成功……"

    # 获取默认的数据框
    print "正在读取mxd文档默认数据框……"
    df = ""
    try:
        frames = arcpy.mapping.ListDataFrames(mxd, "图层")
        if len(frames) == 0:
            frames = arcpy.mapping.ListDataFrames(mxd, "Layers")
        df = frames[0]
    except Exception, e:
        print "读取mxd文档默认数据框失败：", e
        return
    #测试mxd文档是否正常
    brknlist = arcpy.mapping.ListBrokenDataSources(mxd)
    if not len(brknlist) == 0:
        print "文档状态不正常，跳过发布"
        return
    # 构造msd文档名称
    msdPath = mxdPath.replace(".mxd", ".msd")
    # 将mxd转为msd
    print "正在将mxd文档转换为msd文档……"
    arcpy.mapping.ConvertToMSD(mxd, msdPath, df, "NORMAL", "NORMAL")
    # 分析msd
    print "正在分析文档……"
    analysis = arcpy.mapping.AnalyzeForMSD(mxd)
    # 列出分析结果信息
    for key in ('messages', 'warnings', 'errors'):
        print "----" + key.upper() + "---"
        vars = analysis[key]
        for ((message, code), layerlist) in vars.iteritems():
            print "    ", message, " (CODE %i)" % code
            print "       applies to:",
            for layer in layerlist:
                print layer.name,
            print

    # 获取服务器信息
    serviceName = os.path.basename(msdPath).replace(".msd", "")
    serverName = serviceDir.split("/")[2]
    try:
        # 发布msd
        print "正在发布服务……"
        arcpy.mapping.PublishMSDToServer(msdPath, serviceDir, serverName, serviceName, serviceFolder, ["WMS", "KML"])
    except Exception, e:
        print "发布服务失败：", e
    else:
        print "服务发布成功！"

if __name__=="__main__":
    PublishAll(u"E:\李润华\部署文件准备\惠州图片", "http://localhost:6080/arcgis/rest/services", "autoUP")