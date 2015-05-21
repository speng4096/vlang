import time
class Send(): 
    def textMsg(self, content):
        template = """
    <xml>
    <ToUserName><![CDATA[{{ToUserName}}]]></ToUserName>
    <FromUserName><![CDATA[{{FromUserName}}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{Content}]]></Content>
    </xml>
    """
        args = {}
        args["CreateTime"] = int(time.time())
        args["Content"] = content
        return template.format(**args)