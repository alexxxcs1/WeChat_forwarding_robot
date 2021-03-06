
import itchat, time
import re
#coding=utf8

COUNT = 0
PARENTWX=' '

print u'\u53d1\u9001\u0020\u0023\u0030\u0030\u0023\u0062\u0064\u0020\u7ed9\u673a\u5668\u4eba\u7ed1\u5b9a\u8f6c\u53d1\u8d26\u53f7\u0020\u000d\u000a\u53d1\u9001\u0020\u0023\u0030\u0030\u0023\u0071\u0075\u0069\u0074\u0065\u0020\u7ed9\u673a\u5668\u4eba\u89e3\u7ed1\u8f6c\u53d1\u8d26\u53f7\u0020'


@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def text_reply(msg):
    global COUNT
    global PARENTWX
    count=COUNT
    parentwx=PARENTWX
    
    if count==0:
	if msg['FromUserName']== itchat.search_friends()['UserName']:
                pass
	else:
		bdconsole=re.match(r'#00#bd',msg['Text'])
		if bdconsole:
			PARENTWX=msg['FromUserName']
			COUNT=1
			itchat.send(u'\u7ed1\u5b9a\u6210\u529f\uff0c\u6240\u6709\u4fe1\u606f\u90fd\u4f1a\u53d1\u9001\u5230\u8be5\u8d26\u53f7', toUserName=PARENTWX)
    else: 
    	sourcepackyalex = parentwx
    	myweixin=itchat.search_friends()
    	if msg['FromUserName']== myweixin['UserName']:
		pass
    	elif msg['FromUserName']== sourcepackyalex:
		quiteconsole=re.match(r'#00#quite',msg['Text'])
    		if quiteconsole:
        		COUNT=0
        		itchat.send(u'\u89e3\u9664\u7ed1\u5b9a\u6210\u529f\uff01', toUserName=PARENTWX)
        		PARENTWX=' '
		sendmsg = re.match('#(.*):(.*)',msg['Text'])
		if sendmsg:
			sendtouser=itchat.search_friends(name=sendmsg.group(1))
			if sendtouser:
				itchat.send(sendmsg.group(2), toUserName=sendtouser[0]['UserName'])
				itchat.send(u'\u6d88\u606f\u53d1\u9001\u6210\u529f', toUserName=sourcepackyalex)
			else:
				itchat.send(u'\u672a\u627e\u5230\u7528\u6237', toUserName=sourcepackyalex)
		 friendslist = re.match(r'#00#fl',msg['Text'])
		 if friendslist:
                        flist=''
                        for i in range(len(itchat.get_friends())):
                                flist=flist+"%s:%s(%s)\n" % (i,itchat.get_friends()[i]['NickName'],itchat.get_friends()[i]['RemarkName'])
                        itchat.send('%s' % (flist),toUserName=sourcepackyalex)
    	else:
    		fromuser=itchat.search_friends(userName=msg['FromUserName'])
    		itchat.send('%s: %s'%(fromuser['NickName'],msg['Text']), toUserName=sourcepackyalex)
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    global COUNT
    global PARENTWX
    count=COUNT
    parentwx=PARENTWX

    if count==0:
        pass
    else:
        myweixin=itchat.search_friends()
        if msg['FromUserName']== myweixin['UserName']:
                pass
        elif msg['FromUserName']== parentwx:
                pass
        else:
                fileDir = '%s%s'%(msg['Type'], int(time.time()))
                msg['Text'](fileDir)
                fromuser=itchat.search_friends(userName=msg['FromUserName'])
                itchat.send('%s received from %s'%(msg['Type'],fromuser['NickName']), toUserName=parentwx)
                itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), toUserName=parentwx)
#修改了图片类型的转发判定

#@itchat.msg_register('Friends')
#def add_friend(msg):
#    itchat.add_friend(**msg['Text'])
#    itchat.get_contract()
#    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register('Text', isGroupChat = True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s'%(msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()
