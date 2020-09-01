from osgeo import gdal, gdalconst
from osgeo import ogr
import os
import glob
"""样本矢量转样本栅格，并与训练影像宽高维度一致"""

def main(rasterfile, shpFile, data_dir, saved_file_name):
    dataset = gdal.Open(rasterfile, gdalconst.GA_ReadOnly)

    geo_transform = dataset.GetGeoTransform()
    # GetGeoTransform返回6个值，使用下边的关系式将像素映射到地理参考坐标空间
    # Xgeo = GT(0) + Xpixel*GT(1) + Yline*GT(2)
    # Ygeo = GT(3) + Xpixel*GT(4) + Yline*GT(5)
    # 对于北方超上的图，gt(2) and gt(4) are zero.
    # gt(1) pixel width.; gt(5) pixel height; g(0),gt(3):图像左上角位置。

    cols = dataset.RasterXSize  # 列数
    rows = dataset.RasterYSize  # 行数

    x_min = geo_transform[0]
    y_min = geo_transform[3]
    pixel_width = geo_transform[1]

    shp = ogr.Open(shpFile, 0)
    m_layer = shp.GetLayerByIndex(0)
    target_ds = gdal.GetDriverByName('GTiff').Create(os.path.join(data_dir, saved_file_name), xsize=cols, ysize=rows,
                                                     bands=1,
                                                     eType=gdal.GDT_Byte)
    target_ds.SetGeoTransform(geo_transform)
    target_ds.SetProjection(dataset.GetProjection())

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(0)
    band.FlushCache()
    gdal.RasterizeLayer(target_ds, [1], m_layer, options=["ATTRIBUTE=val"])  # 根据shp字段给栅格像元赋值
    gdal.RasterizeLayer(target_ds, [1], m_layer) # 多边形内像元值的全是255
    del dataset
    del target_ds
    shp.Release()


if __name__ == "__main__":
    # 参考raster文件路径
    # base_dir_tif = r"D:\Agriculture\Project\安岳_lemon\安岳_lemon\raster\train"
    # rasterfile = "E:\Agriculture\Project\安康烟草\南郑区哨兵影像\label\\train1.tif"  # 原影像
    # 要转成raster的shape文件。

    # file_dir = r"D:\Agriculture\Project\xinjiang\awati_county\train_raster"
    # file_re = "*_2.tif"
    # files = glob.glob(os.path.join(file_dir, file_re))
    files = [r"F:\DTHS2\2019.6S2\train_raster\T49RFM_20200512T030551_10m_C1.tif"]
    # files = os.listdir(file_dir)
    print(files)

    # file_name = "longtai_train.tif"
    # rasterfile = os.path.join(base_dir_tif, file_name)
    # print(rasterfile)
    # base_dir_shp = r"D:\Agriculture\Project\xinjiang\awati_county\label"
    base_dir_shp = r"F:\DTHS2\2019.6S2\train_raster"
    shpfilename = "tiff2shp.shp"
    #
    shpFile = os.path.join(base_dir_shp, shpfilename)
    print(shpFile)
    # # raster输出路径
    save_dir = r"F:\DTHS2\2019.6S2\label_raster"
    # save_dir = r"D:\Agriculture\Project\xinjiang\awati_county\label_raster"
    # # raster输出文件名
    # # saved_file_name = "longtai_train.tif"
    # file_name =
    for rasterfile in files:
        file_name = rasterfile.split(os.sep)[-1]
        main(rasterfile, shpFile, save_dir, file_name)
