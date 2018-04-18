import paramiko
from tkinter import filedialog
import tkinter as tk
import os.path

class SSHConnection:
  host=None
  port=None
  username=None
  pwd=None
  __transport=None

  def __init__(self,host,port,username,pwd):
    self.host=host
    self.port=port
    self.username=username
    self.pwd=pwd

  def connect(self):
    transport=paramiko.Transport((self.host,self.port))
    transport.connect(username=self.username,password=self.pwd)
    self.__transport=transport

  def close(self):
    self.__transport.close()

  def cmd(self,cmd):
    ssh=paramiko.SSHClient()
    ssh._transport=self.__transport
    stdin,stdout,stderr=ssh.exec_command(cmd)  #执行命令
    result=stdout.read()   #获取命令结果
    #print(str(result,encoding='utf-8'))
    return str(result,encoding='utf-8')

  def upload(self):
    root=tk.Tk()
    root.withdraw()
    try:
      local_path=filedialog.askopenfilename(title='请选择上传文件')
      filename=os.path.basename(local_path)
      sftp=paramiko.SFTPClient.from_transport(self.__transport)   #连接
      sftp.put(local_path,'/home/libou/upload/'+filename)   #上传文件
      print('上传成功')
    except:
      print('上传中断')

  def download(self):
    try:
      result=self.cmd('ls upload')
      file=[]
      file=result.split('\n')
      print('Please choose one file to download:')
      for i in range(len(file)-1):
        print(i+1,' '+file[i])
      num=int(input())
      sftp=paramiko.SFTPClient.from_transport(self.__transport)
      root=tk.Tk()
      root.withdraw()
      directory=filedialog.askdirectory(title='请选择保存位置')
      sftp.get('upload/'+file[num-1],directory+'/'+file[num-1])
      print('下载完成')
    except:
      print('下载中断')

  def find(self):
    result=self.cmd('ls upload')
    file=[]
    file=result.split('\n')
    print('Please choose one file to download:')
    for i in range(len(file)-1):
      print(i+1,' '+file[i])

  def delete(self):
    while True:
      result=self.cmd('ls upload')
      file=[]
      file=result.split('\n')
      print('Please choose one file to delete:')
      for i in range(len(file)-1):
        print(i+1,' '+file[i])
      num=input()
      if num=='exit':
        break
      num=int(num)
      str='rm '+file[num-1]
      self.cmd('rm upload/'+file[num-1])
      print('删除成功')
    
ssh=SSHConnection('123.206.95.20',22,'libou','AGE-1normal')
ssh.connect()
while True:
  a=input("you wanna upload(u) or download(d) or delete or find?")
  if a=='u':
    ssh.upload()
  elif a=='d':
    ssh.download()
  elif a=='delete':
    ssh.delete()
  elif a=='find':
    ssh.find()
  else:
    ssh.close()
    break