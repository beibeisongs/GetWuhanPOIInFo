# encoding=utf-8
# Date: 2018-5-19
# Author: MUJZY


from urllib.parse import quote
from urllib import request
import json
import xlwt


# <Description>: 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):

    i = 1
    poilist = []

    while True:  # <Description>: 使用while 循环不断分页获取数据

        result = getpoi_page(cityname, keywords, i)
        result = json.loads(result)  # 将字符串转换为json

        if result['count'] == '0':
            break

        hand(poilist, result)

        i = i + 1

    return poilist


# <Description>: 数据写入excel
def write_to_excel(poilist, cityname, classfield):

    # <Description>: 一个Workbook对象，这就相当于创建了一个Excel文件
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(classfield, cell_overwrite_ok=True)

    # <Description>: 第一行(列标题)
    sheet.write(0, 0, 'id')
    sheet.write(0, 1, 'name')
    sheet.write(0, 2, 'location')
    sheet.write(0, 3, 'pname')
    sheet.write(0, 4, 'pcode')
    sheet.write(0, 5, 'cityname')
    sheet.write(0, 6, 'citycode')
    sheet.write(0, 7, 'adname')
    sheet.write(0, 8, 'adcode')
    sheet.write(0, 9, 'address')
    sheet.write(0, 10, 'type')
    # sheet.write(0, 11, 'boundary')

    for i in range(len(poilist)):

        """
        # <Description>: 根据poi 的id 获取边界数据
        bounstr = ''
        bounlist = getBounById(poilist[i]['id'])

        if (len(bounlist) > 1):
            bounstr = str(bounlist)
        """

        sheet.write(i + 1, 0, poilist[i]['id'])
        sheet.write(i + 1, 1, poilist[i]['name'])
        sheet.write(i + 1, 2, poilist[i]['location'])
        sheet.write(i + 1, 3, poilist[i]['pname'])
        sheet.write(i + 1, 4, poilist[i]['pcode'])
        sheet.write(i + 1, 5, poilist[i]['cityname'])
        sheet.write(i + 1, 6, poilist[i]['citycode'])
        sheet.write(i + 1, 7, poilist[i]['adname'])
        sheet.write(i + 1, 8, poilist[i]['adcode'])
        sheet.write(i + 1, 9, poilist[i]['address'])
        sheet.write(i + 1, 10, poilist[i]['type'])
        #　sheet.write(i + 1, 11, bounstr)

    book.save(r'd:\\' + cityname+ classfiled + '.xls')


# <Description>: 将返回的poi数据装入集合返回
def hand(poilist, result):

    # result = json.loads(result)  # <Description>: 将字符串转换为json

    pois = result['pois']

    for i in range(len(pois)):
        poilist.append(pois[i])


def getpoi_page(cityname, keywords, page):

    # <Sample>: 'http://restapi.amap.com/v3/place/text?key=9f99fc570ccaf6abc209780433d9f4c1&extensions=all&keywords=%E5%A4%A7%E5%AD%A6&city=%E6%AD%A6%E6%B1%89&citylimit=true&offset=25&page=1&output=json'
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'

    data = ''

    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')

    return data


# <Description>: 根据id 获取边界数据
def getBounById(id):

    req_url = poi_boundary_url + "?id=" + id

    with request.urlopen(req_url) as f:

        data = f.read()
        data = data.decode('utf-8')
        dataList = []
        datajson = json.loads(data)  # 将字符串转换为json
        datajson = datajson['data']
        datajson = datajson['spec']
        if len(datajson) == 1:
            return dataList
        if datajson.get('mining_shape') != None:
            datajson = datajson['mining_shape']
            shape = datajson['shape']
            dataArr = shape.split(';')

            for i in dataArr:
                innerList = []
                f1 = float(i.split(',')[0])
                innerList.append(float(i.split(',')[0]))
                innerList.append(float(i.split(',')[1]))
                dataList.append(innerList)

        return dataList


if __name__ == "__main__":

    amap_web_key = '9f99fc570ccaf6abc209780433d9f4c1'
    poi_search_url = "http://restapi.amap.com/v3/place/text"
    poi_boundary_url = "https://ditu.amap.com/detail/get/detail"

    cityname = "武汉"
    classfiled = "大学"

    classfileds = ['大学', '餐饮', '企业']

    for classfiled in classfileds:

        pois = getpois(cityname, classfiled)

        # <Description>: 将数据写入excel
        write_to_excel(pois, cityname, classfiled)
        print('写入成功')

    # <Description>: 根据获取到的poi 数据的id 获取边界数据
    # dataList = getBounById('B02F4027LY')
    # print(type(dataList))
    # print(str(dataList))