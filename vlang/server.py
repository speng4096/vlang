import tornado.web
import tornado.ioloop
import hashlib
from vlang.parser import parserRaw
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

maxWorks = 10
# 启动服务器
def start(mainMenu, settings):
    global maxWorks
    maxWorks = settings.get('maxWorks', 10)
    application = tornado.web.Application(
        handlers=[(settings['url'], Server, {"mainMenu":mainMenu, "token":settings['token']})])
    application.listen(settings.get('port', 80), settings.get('ip', ''))
    tornado.ioloop.IOLoop.instance().start()

class Server(tornado.web.RequestHandler):
    def initialize(self, mainMenu, token):
        self.mainMenu = mainMenu
        self.token = token
        
    def get(self):
        signature = self.get_argument("signature")
        timeStamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        
        # 数据校验,微信接入
        if not self.checkSignature(signature, timeStamp, nonce):
            pass
            # log.warning("非法GET数据包,来自:" + self.request.remote_ip)
        else:
            echostr = self.get_argument("echostr", "default")
            if echostr != "default":
                self.write(echostr)
                # log.info("收到微信验证请求.")
    
    global maxWorks            
    executor = ThreadPoolExecutor(maxWorks)  # 并发数量
    @tornado.gen.coroutine
    def post(self):
        signature = self.get_argument("signature")
        timeStamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")

        # 数据校验
        if not self.checkSignature(signature, timeStamp, nonce):
            # log.warning("非法POST数据包,来自:" + self.request.remote_ip)
            return
        
        # 处理数据
        rawXML = self.request.body.decode('utf-8')
        w = yield self.parser(rawXML)
        if w:
            self.write(w)
            
    @run_on_executor        
    def parser(self, rawXML):
        tmp = parserRaw(rawXML, self.mainMenu)
        return tmp

    def checkSignature(self, signature, timeStamp, nonce):
        token = self.token
        tmp = [token, timeStamp, nonce]
        tmp.sort()
        raw = ''.join(tmp).encode()
        sha1Str = hashlib.sha1(raw).hexdigest()
        return sha1Str == signature



