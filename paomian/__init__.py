# coding=utf-8
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message
import random,numpy
import os

Casepaomian = on_command("我要吃泡面")
Addpaomian = on_command("买泡面")

@Casepaomian.handle()
async def _(event:GroupMessageEvent,args :Message = CommandArg()):
   with open("D:/zhenxun_bot-main/Cplugins/paomian/List.txt","r+",encoding="utf-8") as ReadList:
      ReadList.seek(0)
      ReadResult = ReadList.read().split("\n")
      CType = ReadResult[random.randint(0,len(ReadResult)-1)]
   with open(("D:/zhenxun_bot-main/Cplugins/paomian/"+CType+".txt"),"r+",encoding="utf-8") as ReadList:
      ReadList.seek(0)
      ReadResult = ReadList.read().split("\n")
      PType = ReadResult[random.randint(0,len(ReadResult)-1)]
   await Casepaomian.finish("今天的泡面是"+CType+PType)

@Addpaomian.handle()
async def _(event:GrouspMessageEvent,args:Message=CommandArg()):
   with open(("D:/zhenxun_bot-main/Cplugins/paomian/List.txt"),"a+",encoding="utf-8") as CReadList:
      CReadList.seek(0)
      CReadResult = CReadList.read().split("\n")
      CType = str(args).split(" ")#获取参数
      CReadList.writelines(+CType[0]+"\n")#如果没有就写入LIST文件
      with open(("D:/zhenxun_bot-main/Cplugins/paomian/"+CType[0]+".txt"),"a+",encoding="utf-8") as PReadList:
         PReadList.seek(0)
         PReadResult = PReadList.read().split("\n")
         PReadList.writelines(CType[1]+"\n")
         await Addpaomian.finish("添加成功")
