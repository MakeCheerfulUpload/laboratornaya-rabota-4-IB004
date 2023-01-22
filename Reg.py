import re
import time
start_time = time.time()

class Object:
    def __init__(self, name, nestingLevel):
        self.name = name
        self.nestingLevel = nestingLevel
        self.content = ""
        self.isMeaning = True

def stackFindFirstFromEnd(nesting):
    global objectStack
    for i in range (len(objectStack)-1, 0-1, -1):
        obj = objectStack[i]
        if obj.nestingLevel == nesting:
            return obj
    print("NOT_FIND_SUCH_OBJECT_EXCEPTION")

#add reg
def getTagNameWithAttribute(str):
    match = re.findall(r"(.+?)\>", str)
    #print(match[0])
    return match[0]

#add reg
def attributeHandler(tagContent):
    global objectStack
    global curNesting
    for i in range(1, len(tagContent)):
        print(tagContent[i])
        attList = re.findall(r"[\w\"]+[^=]", tagContent[i])
        #print('reg:', attList)
        obj = Object(attList[0], curNesting)
        obj.content = attList[1]
        objectStack.append(obj)

def openTagHadler(tagName, tagContent):
    global objectStack
    global curNesting
    global content

    obj = Object(tagName, curNesting)
    objectStack.append(obj)
    if curNesting != 0:
        parentObj = stackFindFirstFromEnd(curNesting - 1)
        parentObj.isMeaning = False
    curNesting += 1
    content = ""
    attributeHandler(tagContent)

def closeTagHandler(tagName, tagContent):
    global curNesting
    global content

    curNesting -= 1
    obj = stackFindFirstFromEnd(curNesting)
    if tagName == '/' + obj.name:
        if obj.isMeaning and len(tagContent) == 1:
            obj.content = content
        elif obj.isMeaning and len(tagContent) > 1:
            pass
        elif not (obj.isMeaning) and len(tagContent) > 1:
            pass
        content = ""
    else:
        print("INVALID_XML_TAG_EXCEPTION")

#add reg
def tagHandler():
    global CursorPosition

    tagNameWithAttribute = getTagNameWithAttribute(file[CursorPosition + 1:])
    tagContent = re.findall(r"[\w=.\"/]+", tagNameWithAttribute)
    #print(tagNameWithAttribute)
    #print(tagContent)
    tagName = tagContent[0]
    if re.match(r"/", tagNameWithAttribute):
        closeTagHandler(tagName, tagContent)
    elif re.match(r"\?xml", tagNameWithAttribute):
        pass
    else:
        openTagHadler(tagName, tagContent)
    CursorPosition += len(tagNameWithAttribute) + 1

def fileOut():
    global file
    print()
    print("FILE:")
    print(file)
    print()

def simpleOut():
    global objectStack
    print()
    print("SIMPLE OUT:")
    for obj in objectStack:
        print(obj.nestingLevel, obj.name, ":", obj.content)
    print()

def YAMLOut():
    global objectStack
    writeSpaces = True
    print()
    print("YAML OUT:")
    l = [0] * 10
    isWriteListing = [False]*10
    for i in range(len(objectStack)):
        obj = objectStack[i]

        for j in range(i+1, len(objectStack)):
            nextObj = objectStack[j]
            if nextObj.nestingLevel < obj.nestingLevel:
                break
            if nextObj.nestingLevel > obj.nestingLevel:
                continue
            if (nextObj.name == obj.name) and not(isWriteListing[obj.nestingLevel]):
                l[obj.nestingLevel] += 1
            else:
                break

        #spaces
        newLine = True
        str = ""
        if writeSpaces:
            str += "  " * (obj.nestingLevel)
        writeSpaces = True


        #name or -
        if l[obj.nestingLevel] == 0:
            str += obj.name + ": "
        else:
            if not(isWriteListing[obj.nestingLevel]):
                str += obj.name + ": "
                isWriteListing[obj.nestingLevel] = True
                l[obj.nestingLevel] += 1
                if obj.content != "":
                    str += "\n" + ("  " * (obj.nestingLevel)) + "  - "
                if obj.content == "":
                    str += "\n" + ("  " * (obj.nestingLevel)) + "- "
                    newLine = False
                    writeSpaces = False

            else:
                if obj.content != "":
                    str += "  - "
                else:
                    if (i+1<len(objectStack)) and objectStack[i+1].nestingLevel > obj.nestingLevel:
                        str += "- " #переход на новую строку (кроме после заголовка)
                        newLine = False
                        writeSpaces = False
                    else:
                        str += "- " #обработка пцстых значений тэгов



            l[obj.nestingLevel] -= 1
            if l[obj.nestingLevel] == 0:
                isWriteListing[obj.nestingLevel] = False

        #content
        str += obj.content

        #print it
        if newLine:
            print(str)
        else:
            print(str, end='')

    print()



#for i in range(100):
FILE = open('../Вторник.xml', 'r', encoding="utf-8")
file = FILE.read()

CursorPosition = 0
objectStack = []
curNesting = 0
content = ""

while CursorPosition < len(file):
    curSymb = file[CursorPosition]
    if curSymb == '<':
        tagHandler()
    else:
        content += curSymb
    CursorPosition += 1

#fileOut()
#simpleOut()
YAMLOut()
#print(f"Time past: {time.time() - start_time}")