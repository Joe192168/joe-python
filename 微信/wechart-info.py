#!/usr/bin/python 
#coding: utf-8
encodeing='utf-8'

import itchat,datetime
from itchat.content import TEXT

class WeChat(object):
	def get_all_info_from_wechat(self):
		try:
			itchat.auto_login(enableCmdQR = False)
			#获取群
			roomslist = itchat.get_chatrooms()
			#群名称
			itchat.dump_login_status() # 显示所有的群聊信息，默认是返回保存到通讯录中的群聊
			myroom=itchat.search_chatrooms(name=u'老板，阔乐，加冰！') #群聊名称
			gsq=itchat.update_chatroom(myroom[0]['UserName'], detailedMember=True)

			print(gsq)
		except Exception as e:
			print(e)

if __name__ == '__main__':
	obj = WeChat()
	obj.get_all_info_from_wechat()