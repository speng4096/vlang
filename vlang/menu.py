from vlang.message import Send

# 为了方面扩展，独立出Module模块，后面加入功能
class Module(Send):
    class BUFFER():
        pass
    
class Menu(Module):
    def __init__(self):
        self.name = ""
        self.subMenus = []
        self.nextMenu = None
        self.tag()
        self.baseMenu = self  # 默认父菜单是自己,这会在链接菜单时被修改
           
    def add(self, subMenu):
        new = subMenu()
        self.subMenus.append(new)
        new.baseMenu = self
        setattr(self, subMenu.__name__, new)
    
    def action(self):
        '''用户进入菜单后的动作'''
        pass
        
    def tag(self):
        '''对菜单的设置,包括name等等'''
        pass
    
    def makeMenu(self):
        '''返回已格式化的菜单'''
        menuList = self.getSubMenusName()
        menuStr = self.name + "\n"
        f = "{0}:{1};\n"
        for index, name  in enumerate(menuList):
            menuStr += f.format(index + 1, name)   
        menuStr += "请回复数字:\n"        
        return menuStr    
        
    def autoJump(self, reply):
        '''根据用户回复,跳转菜单,暂是只支持数字,后面可加入模糊匹配
        :失败重新打印菜单'''
        try:
            index = int(reply) - 1  # 菜单从1开始,列表从0开始
            return self.getSubMenus()[index]
        except (IndexError, ValueError):
            return "没有这个菜单\n\n", self, self.BUFFER
            
    def getSubMenus(self):
        '''返回list,包含本菜单下的的直系子菜单的引用'''
        return self.subMenus
    
    def getSubMenusName(self):
        '''返回list,包含本菜单下的的直系子菜单的名称'''
        return [m.name for m in self.subMenus]
    
    
    def getSubMenusRec(self):
        '''递归寻找子菜单,返回list,包含所有子菜单的引用'''
        return self._getSubMenusRec(self.subMenus)
        
    def getSubMenusNameRec(self):
        '''递归寻找子菜单,返回list,包含所有子菜单的名称'''
        return self._getSubMenusNameRec(self.subMenus)

    def _getSubMenusNameRec(self, subMenus):
        '''递归寻找子菜单'''
        tmp = []
        for m in subMenus:
            if m.subMenus:
                tmp.append(self._getSubMenusNameRec(m.subMenus))
            else:
                tmp.append(m.name)
        return tmp
        
    def _getSubMenusRec(self, subMenus):
        '''递归寻找子菜单'''
        tmp = []
        for m in subMenus:
            if m.subMenus:
                tmp.append(self._getSubMenusRec(m.subMenus))
            else:
                tmp.append(m)
        return tmp
    
    def _getListRec(self, arr):
        lit = []
        for i in arr:
            if isinstance(i, list):
                lit += self._getListRec(i)
            else:
                lit += [i]
        return lit
    
    def getMenuTable(self):
        tmp = self._getListRec(self.getSubMenusRec())
        tmp += [self]
        tmp = {i.__class__.__name__:i for i in tmp}
        return tmp
