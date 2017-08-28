
# 微信转发小机器人 

这个机器人是基于 itchat 开发的一个小玩具[itchat链接](https://github.com/littlecodersh/ItChat "呵呵，有趣")   

Python练手用的，原理是基于Itchat的网页微信接口来获取消息，判断消息来源转发给另一个微信号。

本来是写给自己用的，所以转发的账号都写死了，后来发现可以通过绑定账号的方式来转发消息

代码比较简单，就不写注释了，只写一下操作方式。

首先你需要一个联网的计算机（我的树莓派还在快递的路上，等到了就放进树莓派里），或者服务器
(我买的阿里云服务器，但是把代码放上去后itchat返回错误，是SSL的问题，我千方百计搞定了SSL认证了https,结果还是那个错误，干脆就部署在本地虚拟机了)

然后你需要一台不用的手机，只要能登微信就好。

将我的代码放在你的服务器或计算机上，然后执行它，会提示你扫描二维码
（我这里的代码是返回一张二维码图片，如果是终端不能显示图片的可以去itchat里有个设置终端生成字符二维码的）

然后手机上确认登录，这时候拿你常用的微信号给这个机器人发送一个绑定消息

`#00#bd` 

(本来想设置成*#06#的，但是match匹配的时候*是敏感字符。这个梗可能只有上了年纪的人才懂哈哈哈哈哈)

接下来就等别人给你机器人发消息啦

解除绑定使用已绑定的微信号给 机器人发送

`#00#quite`

就可以解除绑定。

当你的机器人收到别人的消息，会带着对方的姓名转发给你的常用号。

如果你要回复，可以给机器人发送 

`#你的好友姓名:你要说的话` 

来回复。

就是这样，很简单！

如果以后还有什么有趣的功能我再加入！

添加了获取好友列表功能: 

`#00#fl`


## 详细教程 第一步:安装itchat

该机器人是基于itchat的微信接口的，所以第一步是安装Itchat，在终端内输入

`pip intstall itchat`

(假定你安装了pip，如果没有，Linux 用户就install个pip,这玩意儿还在CentOS上还不能直接yum install pip,你可以上网百度下怎么安装，反正也就几行命令的事 )

安装好之后你就可以愉快的运行我的小机器人了！

`骗你的`

## 详细教程 第二步:配置环境

什么！还要配置环境？？！不然呢，你以为一个Python就无敌了吗。

如果你你不想听我废话！直接拉到最后，可以看具体改的地方！

下面我开始记录我的修改心路历程！

大部分人运行小机器人的时候可能会发现，哇塞，出错了！

SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:579)

我的这个教程就是为了解决这个问题，其他问题都是小问题，这个是个大问题！因为我搞了好久查了好多资料，都没找到具体的办法。

这个问题主要是SSL安全验证的问题，为了解决这个问题，我特意去认证了一个SSL证书，搞了个https，结果还是错误

`FUCK`

后面发现大部分SSL错误的网上都有一个还凑合的答案，就和电脑坏了就重启一样，那就是绕过SSL安全验证

这时候就需要改itchat的代码了

第一个错误是这样的:

`Traceback (most recent call last):
  File "/usr/lib/python2.7/site-packages/itchat/utils.py", line 125, in test_connect
    r = requests.get(config.BASE_URL)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 72, in get
    return request('get', url, params=params, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 58, in request
    return session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 513, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 623, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 514, in send
    raise SSLError(e, request=request)
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:579)
You can't get access to internet or wechat domain, so exit.`

这时候你就需要修改itchat里的utils.py了

 `vi /usr/lib/python2.7/site-packages/itchat/utils.py`
 
 切换到utils.py的125行，你会发现一个
 
  `r = requests.get(config.BASE_URL)`
  
  你需要把它改成
  
 `r = requests.get(config.BASE_URL,verify=False)`
 
 接下来再运行小机器人
 
 还是错误！

 `FUCK`
 
 错误如下:
 
 `/usr/lib/python2.7/site-packages/urllib3/connectionpool.py:852: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
Getting uuid of QR code.
Traceback (most recent call last):
  File "./ichatrb.py", line 29, in <module>
    itchat.auto_login(enableCmdQR=True)
  File "/usr/lib/python2.7/site-packages/itchat/components/register.py", line 36, in auto_login
    loginCallback=loginCallback, exitCallback=exitCallback)
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 45, in login
    while not self.get_QRuuid():
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 102, in get_QRuuid
    r = self.s.get(url, params=params, headers=headers)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 526, in get
    return self.request('GET', url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 513, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 623, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 514, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:579)`

第一行的提醒不用管，最后来处理

现在看第四行

login.py的102行，获取二维码ID失败，也是把

`r = self.s.get(url, params=params, headers=headers)`

改为

`r = self.s.get(url, params=params, headers=headers, verify=False)`

然后运行，我们就get了一个很丑的二维码

![](http://packy.club/QR.png)  

需要调一下二维码的宽度，具体可以看itchat的文档

https://itchat.readthedocs.io/zh/latest/

根据你自己的情况修改好之后，可以得到一个漂亮的二维码。

有时候不能扫二维码是因为你需要把数值改成负的

扫完二维码你会发现，又错误了！！

`Traceback (most recent call last):
  File "./ichatrb.py", line 29, in <module>
    itchat.auto_login(enableCmdQR=-2)
  File "/usr/lib/python2.7/site-packages/itchat/components/register.py", line 36, in auto_login
    loginCallback=loginCallback, exitCallback=exitCallback)
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 53, in login
    status = self.check_login()
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 137, in check_login
    if process_login_info(self, r.text):
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 155, in process_login_info
    r = core.s.get(core.loginInfo['url'], headers=headers, allow_redirects=False)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 526, in get
    return self.request('GET', url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 513, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 623, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 514, in send
    raise SSLError(e, request=request)
requests.exceptions.SSLError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:579)`

继续修改login.py

`vi /usr/lib/python2.7/site-packages/itchat/components/login.py`

废话不多直接跳到133行

`r = self.s.get(url, params=params, headers=headers)`

改成你懂的

`r = self.s.get(url, params=params, headers=headers , verify=False)`

还是错误，继续改

`vi /usr/lib/python2.7/site-packages/itchat/components/login.py`

跳到155

`r = core.s.get(core.loginInfo['url'], headers=headers, allow_redirects=False)`

改成

`r = core.s.get(core.loginInfo['url'], headers=headers, allow_redirects=False,verify=False)`

终于登录成功了

可是过一会儿一直跳错误

`Traceback (most recent call last):
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 244, in maintain_loop
    i = sync_check(self)
  File "/usr/lib/python2.7/site-packages/itchat/components/login.py", line 303, in sync_check
    if not isinstance(e.args[0].args[1], BadStatusLine):
IndexError: tuple index out of range`

获取不到资料啊

继续改 `vi /usr/lib/python2.7/site-packages/itchat/components/login.py`

300行

` r = self.s.get(url, params=params, headers=headers, timeout=config.TIMEOUT)`

改成

` r = self.s.get(url, params=params, headers=headers, timeout=config.TIMEOUT,verify=False)`

改完之后登录！登录成功！！！

然后发现别人一发消息你就错误崩溃！

是的还需要改  login.py 的331行

`r = self.s.post(url, data=json.dumps(data), headers=headers, timeout=config.TIMEOUT)`

改成

`r = self.s.post(url, data=json.dumps(data), headers=headers, timeout=config.TIMEOUT,verify=False)`

添加了获取好友列表后，又发现会错误的地方

login.py 的90行

`r = core.s.get(url, headers=headers).json()`

改成

`r = core.s.get(url, headers=headers,verify=False).json()`

图片类信息无法通过安全验证，需要改 

`vi /usr/lib/python2.7/site-packages/itchat/components/messages.py`

439行的

`return requests.post(url, files=files, headers=headers)`

改为

`return requests.post(url, files=files, headers=headers,verify=False)`

# 总结一下，八个需要改的地方

`utils.py 125行`

`login.py 90行`

`login.py 102行`

`login.py 133行`

`login.py 155行`

`login.py 300行`

`login.py 331行`

`messages.py 419行`

这八个地方只要添加上`verify=False`就OK了，但是会有提示SSL安全警告提示

在我的机器人代码的顶部 然后添加如下代码：

`import requests`

`from requests.packages.urllib3.exceptions import InsecureRequestWarning`

`requests.packages.urllib3.disable_warnings(InsecureRequestWarning)`

如果有其他地方可能我暂时还没遇到错误

完美！！

## 吐槽一下

写这种东西比写毕业论文的乱七八糟分析一大堆写出一个辣鸡程序来爽多了！

