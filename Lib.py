import yaml
import xmltodict
#import xmldict_translate
import time

start_time = time.time()

#for i in range(100):
FILE = open('../Вторник.xml', 'r', encoding="utf-8")
file = FILE.read()

pyObj = xmltodict.parse(file)
#pyObj = xmldict_translate.xml2dict(file)
#print(pyObj)
yamlDoc = yaml.dump(pyObj, encoding=None, allow_unicode=True)
print(yamlDoc)
#print(f"Time past: {time.time() - start_time}")