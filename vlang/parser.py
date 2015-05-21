from xml.etree import ElementTree as ET
from vlang.user import User

userTable = {}

def parserRaw(rawXML, mainMenu):
    '''把微信发来的xml格式的消息,解析成dict格式,方便在python中操作'''
    '''将消息传递给对应的User实例处理'''
    if not rawXML:
        return
    message = dict((child.tag, child.text) for child in ET.fromstring(rawXML))
    
    # 根据微信ID寻找user实例,如果没有实例就new一个
    openID = message['FromUserName']
    if openID not in userTable:
        userTable[openID] = User(mainMenu)

    userTable[openID].buffer = ""
    return userTable[openID].handle(message)
