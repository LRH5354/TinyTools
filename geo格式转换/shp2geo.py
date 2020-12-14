# coding=utf-8
import shapefile
import json
import codecs
import datetime
from Bloch import load, save

def dateCoverToStr(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
def Shp2JSON(filename,shp_encoding='utf-8',json_encoding='utf-8'):
    # '''
    # :这个函数用于将shp文件转换为GeoJSON文件
    # :param filename: shp文件对应的文件名（去除文件拓展名）
    # :return:
    # '''
    # '''创建shp IO连接'''
    reader = shapefile.Reader(filename,encoding=shp_encoding)
    # '''提取所有field部分内容'''
    fields = reader.fields[1:]
    # '''提取所有field的名称'''
    field_names = [field[0] for field in fields]
    # '''初始化要素列表'''
    buffer = []
    for sr in reader.shapeRecords():
        # '''提取每一个矢量对象对应的属性值'''
        record = sr.record
        # '''属性转换为列表'''
        record = [r.decode('gb2312','ignore') if isinstance(r, bytes)
                  else r for r in record]
        # '''对齐属性与对应数值的键值对'''
        atr = dict(zip(field_names, record))
        # '''获取当前矢量对象的类型及矢量信息'''
        geom = sr.shape.__geo_interface__
        # '''向要素列表追加新对象'''
        buffer.append(dict(type="Feature",
                           geometry=geom,
                           properties=atr))
    # '''写出GeoJSON文件'''
    geoJson={"type":"FeatureCollection","features":buffer}
    geojson = codecs.open(filename + "-geo.json","w", encoding=json_encoding)
    geojson.write(json.dumps(geoJson,default=dateCoverToStr)+ '\n')
    geojson.close()
    print('转换成功！')
    # Load a data file into a Datasource instance.
    datasrc = load(r'E:\智慧惠州\splitFeature_地级市\440000000000.shp-geo.json')

    # Simplify the geometry.
    datasrc.simplify(500)

    # # Save it out to a new shapefile.
    # Bloch.save(datasrc, 'output1.shp')

    # This will throw an error, because 250 < 500.
    datasrc.simplify(250)

    # Simplify the geometry more.
    datasrc.simplify(1000)

    # Save it out to a new GeoJSON file.
    save(datasrc, 'output2.json')

if __name__ == '__main__':
    import os
    os.chdir(r'E:\智慧惠州\splitFeature_地级市')
    Shp2JSON(filename='440000000000.shp',
             shp_encoding='utf-8',
             json_encoding='utf-8')