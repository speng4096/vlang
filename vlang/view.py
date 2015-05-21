from vlang.menu import Menu
from vlang.server import start
import time

class MainMenu(Menu):
    def tag(self):
        self.name = "计算器"

    def action(self):
        reply = yield self.makeMenu()
        yield self.autoJump(reply)

class Menu_1(Menu):
    def tag(self):
        self.name = "乘除法"
        
    def action(self):
        reply = yield self.makeMenu()
        yield self.autoJump(reply)

class Menu_2(Menu):
    def tag(self):
        self.name = "表达式计算"
        
    def action(self):
        yield "这个功能还没开发呢!", mainMenu

class Menu_1_1(Menu):
    def tag(self):
        self.name = "乘法"
        
    def action(self):
        try:
            reply = yield "请输入因数1:"       
            num1 = float(reply)
            
            reply = yield "请输入因数2:"
            num2 = float(reply)
            time.sleep(4)
            num = num1 * num2
            yield "{0} x {1} = {2}\n".format(num1, num2, num)
            
        except ValueError:  # 输入不是float型
            yield "输入错误,重新录入:\n", self.BUFFER
        
class Menu_1_2(Menu):
    def tag(self):
        self.name = "除法"

    def action(self):
        yield "请输入被除数:"
        while(True):
            try:
                num1 = float(self.reply)
                yield "请输入除数:"
                num2 = float(self.reply)
                
                while(True):
                    if num2 == 0:
                        yield "除数不能为0,请重新输入:"
                        num2 = float(self.reply)
                    else:
                        break
                
                break
                    
            except ValueError:  # 输入不是数字
                yield "输入不是数字,请重新输入被除数:"

        print("除法计算中")
        num3 = num1 / num2
        yield '''{0} ÷ {1} = {2}
退回主菜单输入0
继续乘法计算输入任意字符:'''.format(num1, num2, num3)
        if self.reply == "0":
            yield mainMenu
        
if __name__ == "__main__":
    mainMenu = MainMenu()
    mainMenu.add(Menu_1)
    mainMenu.add(Menu_2)
    mainMenu.Menu_1.add(Menu_1_1)
    mainMenu.Menu_1.add(Menu_1_2)

    settings = {"url" :"/weixin",
                      "token" : "CU342RIVA598BJ7OHEMGYDNWLKQT601Z",
                      "port" : 8080 }
    start(mainMenu, settings)
