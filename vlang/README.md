# vLang 使用说明 #

vLang是一个基于模型的微信开发框架，遵循MIT协议发布。

# 安装

开发与测试环境: 
Ubuntu Kylin 15.04 64bit
Python 3.4
Tornado 4.1
> python3 setup.py install

# 入门 #

### 1. Hello World! ###

最简单的例程，对用户发送的所有消息，回复“Hello World！”

```python
from vlang.menu import Menu
from vlang.server import start

class MainMenu(Menu):
    def action(self):
        yield "Hello World"

# token需和微信后台填写一致
settings = {"url" :"/weixin",
                   "port" : 8080,
                   "token" : "WQif56gU" }
start(MainMenu(), settings)
```

### 2. 微信计算器 ###

+ 简易乘法计算器

```python
from vlang.menu import Menu
from vlang.server import start

class MainMenu(Menu):
    def action(self):
        num0 = yield "请输入因数1:"    #用户输入将保存在num0里.
        num1 = yield "请输入因数2:"
        num2 = float(num0) * float(num1)
        yield "计算结果:\n {0} x {1} = {2}".format(num0,num1,num2)

settings = {"url" :"/weixin",
                   "port" : 8080,
                   "token" : "WQif56gU" }
start(MainMenu(), settings)
```

+ 带有二级级菜单的四则运算器，能计算加减法，乘法。

```python
from vlang.menu import Menu
from vlang.server import start

class MainMenu(Menu):
    def tag(self):
        self.name = "计算器"
    def action(self):
        reply = yield self.makeMenu()  # 根据子菜单的名字，生成菜单列表
        yield self.autoJump(reply)  # 根据回复，跳转到对应菜单

class Menu_1(Menu):
    def tag(self):
        self.name = "加减法"
    def action(self):
        reply = yield self.makeMenu()
        yield self.autoJump(reply)

class Menu_1_1(Menu):
    def tag(self):
        self.name = "加法"
    def action(self):
        num0 = yield "请输入加数1:"
        num1 = yield "请输入加数2:"
        num2 = float(num0) + float(num1)
        yield "计算结果:\n {0} + {1} = {2}".format(num0, num1, num2) 

class Menu_1_2(Menu):
    def tag(self):
        self.name = "减法"
    def action(self):
        num0 = yield "请输入被减数:"
        num1 = yield "请输入减数:"
        num2 = float(num0) - float(num1)
        reply = yield '''计算结果:\n {0} - {1} = {2}
回复“ 0 ”可回到主菜单'''.format(num0, num1, num2) 
        if reply == "0" : yield MainMenu  # 跳转到指定菜单
        
class Menu_2(Menu):
    def tag(self):
        self.name = "乘法"
    def action(self):
        num0 = yield "请输入因数1:"
        num1 = yield "请输入因数2:"
        num2 = float(num0) * float(num1)
        yield "计算结果:\n {0} x {1} = {2}".format(num0, num1, num2)

# 链接菜单
menuTree = MainMenu()  # 新建一个菜单树
menuTree.add(Menu_1)  # 链接一级菜单
menuTree.add(Menu_2)
menuTree.Menu_1.add(Menu_1_1)  # 链接二级菜单
menuTree.Menu_1.add(Menu_1_2)

# 设置并启动服务器
settings = {"url" :"/weixin",
                   "port" : 8080,
                   "token" : "WQif56gU" }
start(menuTree, settings)
```

# Menu #

在vLang中，微信项目是由一个个菜单链接而构成的， 本节将详细介绍vLang中菜单的结构，链接，启动。

### 结构 ###

菜单是继承自vlang.menu.Menu的类，并需重载其action()方法，用来接收，处理，回复微信消息。
在多级菜单中，还需重载tag()方法，用以保存一些设置，目前仅有self.name这一项，用以指定菜单的名字。

```python
from vlang.menu import Menu

class MainMenu(Menu):
    def tag(self):
        #用以保存本菜单的设置。
        self.name = "主菜单"
    
    def action(self):
        #当收到用户消息时，vLang会调用对应菜单的action()，并传入用户消息。
        pass
        
```

### 链接 ###

为了简化开发，vLang支持多级菜单。菜单与其子菜单的链接使用add(Menu)。
在上文 *四则运算器* 一例中，

```python
menuTree = MainMenu()    #新建一个菜单树，必须为Menu类的实例。
menuTree.add(Menu_1)     #链接一级菜单
menuTree.add(Menu_2)
menuTree.Menu_1.add(Menu_1_1) #链接二级菜单
menuTree.Menu_1.add(Menu_1_2)
```

### 启动 ###

```python
vlang.server.start(menuTree, settings)
```
其中,
menuTree是Menu类的实例，如果有多级菜单，启动前需先链接菜单。
settings是一个包含许多设置的字典
```python
settings = {"url" :"/weixin",            
                   "port" : 8080,        #默认为 80 端口
                   "ip":"127.0.0.1",     #默认为"" , 绑定所有地址,
                   "token" : "WQif56gU"，#在微信公众号官网设置的token
                   "work" : "WQif56gU"}  #可同时服务的用户数量，也是线程数量，默认为10

```

# yield！ #
Python中 *yield* 关键字具有神奇的魔力。
vLang中，yield用于: *回复/接收消息*，*跳转菜单*

### 回复 ###

+ **给用户发送消息：**

```python
yield "您好，欢迎光临！"
```

+ **给用户发送消息，并得到回复：**

```python
reply = yield "请输入用户名："
```

+ **缓存一段话，暂不发给用户，程序将继续执行至下一个yield语句处。一般用于缓存一段错误信息：**

```python
def action(self):
    while(True):
        try:
            reply = yield "请输入整数："
            num = int(reply)
            break
        except ValueError:
            yield "您输入的不是整数，请重试\n", self.BUFFER  # 缓存一段话，后面添加个self.buffer即可。        
```

如果用户输入了"haha"，int(reply)将抛出ValueError异常
程序实际回复：
>您输入的不是整数，请重试
>请输入整数：

可缓存多段文本，当程序继续执行到没有self.buffer的yield语句时，vLang才会将缓存区文本发送给用户。

### 跳转 ###
以 *入门* 小节中，*四则运算器* 为例。

+ **跳转到另一个菜单：**

```python
yield Menu_1_2
```

能够传入Menu，或者Menu的实例。
例如，跳转到主菜单可以这样写：

```python
yield MainMenu
```

也可以这样写：

```python
yield menuTree
```

+ **跳转到现行菜单的开始点：**

```python
yield self
```

特别的，如果没有显式指定下一个菜单，当action() 执行完后，默认跳转到现行菜单的开始点。

+ **跳转到父菜单：**
```python
yield self.baseMenu
```


+ **当然，跳转菜单的同时也能给用户回复消息，也缓存一段信息：**

```python
yield "充值失败！", MainMenu , self.buffer
```

不过，上面的三个参数得 **按顺序** 写。其原型是：(String , Menu , self.buffer)

# 版本 #
目前版本为 0.2.1 ，是开源的第一个版本。

* 下个版本中，将会有如下**改进**：
    
    * autoJump() 支持模糊匹配
    * 加入日志模块
    * 加入消息加解密功能
    * 支持多媒体消息，如语音，图片，图文，地理位置等

* 未来版本中，可能有如下**改进**：

    * 在80端口处提供一个管理员网页，方便设置，管理
    * 提供幸运大转盘，刮刮卡等等常见活动
    * 接入 其他开源项目，以支持中文分词和情感分析
    * ……
    * 非常期待您的建议！

# 关于 #
**谢谢您的耐心阅读！**