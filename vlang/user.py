import vlang.menu
from builtins import isinstance

class User():
    def __init__(self, mainMenu):
        self.mainMenu = mainMenu
        self.currentMenu = mainMenu
        self.jump = True
        self.buffer = ""
        self.gen = None

    def handle(self, message):
        # 生成器
        if self.jump or self.gen == None:
            self.gen = self.currentMenu.action()
            self.new = True  # 生成器是否未被使用
            self.jump = False
        
        # 运行生成器
        try:
            if self.new:
                value = self.gen.__next__()
                self.new = False
            else:
                value = self.gen.send(message["Content"])

        except StopIteration:
            value = self.currentMenu  # 生成器用完,默认从头开始
        
        # 所有的值都保存在list里
        if not isinstance(value, tuple):
            value = [value, ]
        else:
            value = list(value)  
        
        valueType = list(value)  # 深拷贝一份list版本
        
        # 如果返回值有Menu的实例,valueType中替换成py.menu.Menu
        # 如果返回值有Menu的子类,valueType中替换为py.menu.Menu
        #    value中替换为Menu的实例
        # 如果返回值有str的实例,valueType中替换成str类
        for index, tmp in enumerate(valueType):
            if isinstance(tmp, vlang.menu.Menu):
                valueType[index] = vlang.menu.Menu
                continue
                
            if tmp.__class__ == type:
                if tmp.__bases__:
                    if tmp.__bases__[0] == vlang.menu.Menu:
                        valueType[index] = vlang.menu.Menu
                        value[index] = self.mainMenu.getMenuTable()[value[index].__name__]
#                         print("处理一个Menu子类返回情况")
                        continue
                
            if isinstance(tmp, str):
                valueType[index] = str
                continue
        
        lastMenu = self.currentMenu
        # 判断返回类型
        if valueType == [str, vlang.menu.Menu, vlang.menu.Menu.BUFFER]:
            self.currentMenu = value[1]
            self.jump = True
            self.buffer += value[0]
            
        elif valueType == [str, ]:
            self.buffer += value[0]
            
        elif valueType == [str, vlang.menu.Menu]:
            self.currentMenu = value[1]
            self.jump = True
            self.buffer += value[0]
            
        elif valueType == [str, vlang.menu.Menu.BUFFER]:
            self.buffer += value[0]
        
        elif valueType == [vlang.menu.Menu, ]:
            self.currentMenu = value[0]
            self.jump = True
            return self.handle(message)  # 下一个菜单的执行结果
       
        else:
            print("yield 格式错误")
        
        # 返回给上层的write()
        if str not in valueType: #没有回复文本
            return None
        
        #  有buffer的情况
        if vlang.menu.Menu.BUFFER in valueType: #缓存文本，不输出
            self.jump = False
            return self.handle(message)  # 下一个菜单的执行结果
        
        # 填充发送方账号和接收方账号
        args = {}
        args["ToUserName"] = message["FromUserName"]
        args["FromUserName"] = message["ToUserName"]
        tmp = lastMenu.textMsg(self.buffer)
        tmp = tmp.format(**args)
        return tmp
