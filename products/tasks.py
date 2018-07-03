from beenquickServer.demo import app
from lxml import etree
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
r = redis.Redis(connection_pool=pool)

@app.task
def xmlParser(file_path):
    print(file_path)
    parser = etree.XMLParser(load_dtd=True)
    tree = etree.parse(file_path,parser)
    root = tree.getroot()
    for field1 in root:
        tempDir = {}
        moveId = ''
        for field2 in field1:
            if field2.tag == 'id':
                moveId = field2.text
            if field2.tag == 'format':
                tempDir['format'] = field2.text
            if field2.tag == 'type':
                tempDir['type'] = field2.text
            if field2.tag == 'year':
                tempDir['year'] = field2.text
        print(moveId, tempDir)
        if moveId != '' and tempDir != {}:
            r.hmset('move'+moveId,tempDir)
            print('---------------------')
            print(r.hmget('move'+moveId,'type'))
    return 'ok'
