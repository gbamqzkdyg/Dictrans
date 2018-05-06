#coding=utf8
import hashlib
import urllib.parse
import http.client
import random
import json
from tkinter import *

appKey = '1d53b43d03832210'
secretKey ='IRdK4iR6vIVaDgXcKrw53P15uGhUwREU' # 有道云Key

def useAPI(word, i): # word为待查词语或者句子，i=0返回翻译结果（一定存在），i=1时返回查词结果（只有word为单词时存在）
	httpClient = None
	myurl ='/api'
	fromLang = 'auto' # 'EN'
	toLang = 'auto' # 'zh-CHS'
	salt = random.randint(1, 65536) # 随机数salt
	sign = (appKey+word+str(salt)+secretKey).encode('utf-8') # 按照API文档生成sign原文
	m1 = hashlib.md5()
	m1.update(sign)
	sign = m1.hexdigest() # 按照API文档生成sign摘要
	myurl =	myurl + '?appKey=' + appKey + '&q=' + urllib.parse.quote(word) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign #生成HttpGet的URL
	result = "" # 结果字符串
	try: # 建立连接，获取数据
		httpClient= http.client.HTTPConnection('openapi.youdao.com')
		httpClient.request('GET', myurl)
		# response是HTTPResponse对象
		response = httpClient.getresponse()
		data = json.loads(response.read()) # 读取json数据
		if(i == 1):
			result = str("".join(data['translation'])) # 返回翻译结果
		else :
			try:
				result = str("".join(data['basic']['explains'])) # 返回查词结果
			except Exception:
				result = str("".join(data['basic']))
	except Exception as e:
		result = 'Error'
	finally:
		if	httpClient:
			httpClient.close() # 断开连接
		return result

# 将结果全部复制到剪切板
def copyAll(root,text):
	root.clipboard_clear()
	root.clipboard_append(text)

def main():
	# 根窗口设置
	root = Tk();
	root.title("Dictrans")
	root.iconbitmap('transdict.ico')
	root.geometry('300x200+500+200')
	# 输入框设置为Entry
	e = Entry()
	e.pack()
	# 结果框设置为Message
	m = Message(aspect = 150, width = 150)
	# 查询函数，mode表示查询模式，0为查词，1为翻译
	def search(mode):
		m.pack_forget()
		m['text'] = useAPI(e.get(), mode)
		m.pack()
	# 放置按钮
	b1 = Button(text = '查词', command = lambda:search(0)).pack()
	b2 = Button(text = '翻译', command = lambda:search(1)).pack()
	b3 = Button(root, text='复制到剪贴板', command = lambda : copyAll(root,m['text']), relief = "raised").pack()
	# 输入框右键菜单设置
	def paste():
		e.event_generate('<<Paste>>')
	def copy():
		e.event_generate('<<Copy>>')
	def cut():
		e.event_generate('<<Cut>>')
	rightMenu = Menu(root, tearoff = 0)
	rightMenu.add_command(label = "粘贴", command = paste)
	rightMenu.add_separator()
	rightMenu.add_command(label = "复制", command = copy)
	rightMenu.add_command(label = "剪切", command = cut)
	# 输入框绑定右键
	def rightClick(event):
		rightMenu.post(event.x_root, event.y_root)
	e.bind("<Button-3>", rightClick)
	# 执行
	root.mainloop()
		
main()