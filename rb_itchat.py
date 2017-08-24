import itchat, time
import re
#coding=utf8

COUNT = 0
PARENTWX=' '

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
    	else:
    		fromuser=itchat.search_friends(userName=msg['FromUserName'])
    		itchat.send('%s: %s'%(fromuser['NickName'],msg['Text']), toUserName=sourcepackyalex)
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    sourcepackyalex = itchat.search_friends(name=u'\u62d4\u5200\u556a')
    myweixin=itchat.search_friends()
    if msg['FromUserName']== myweixin['UserName']:
        pass
    elif msg['FromUserName']== sourcepackyalex[0]['UserName']:
        pass
    else:
    	fileDir = '%s%s'%(msg['Type'], int(time.time()))
    	msg['Text'](fileDir)
    	fromuser=itchat.search_friends(userName=msg['FromUserName'])
    	itchat.send('%s received from %s'%(msg['Type'],fromuser['NickName']), toUserName=sourcepackyalex[0]['UserName'])
    	itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), toUserName=sourcepackyalex[0]['UserName'])

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
