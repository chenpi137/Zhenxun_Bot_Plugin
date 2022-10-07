from argparse import SUPPRESS
from models.bag_user import BagUser
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import GroupMessageEvent,Message
from nonebot.params import CommandArg
from services.db_context import db
from nonebot.permission import SUPERUSER

__zx_plugin_name__ = "PYPY"
__plugin_type__ = ("商店",)
__plugin_version__ = 0.1
__plugin_author__ = "CHNEPI"
__plugin_usage__ = """
usage：
    PY交易
    指令：
        转账 at 金额
        增加金币 at 金额[管理员可用]
""".strip()
__plugin_version__ = 0.1
__plugin_author__ = "CN_CHENPI"

SendGolds = on_command("转账")
SetGolds = on_command("增加金币",permission=SUPERUSER)

@SendGolds.handle()
async def _(event :GroupMessageEvent,args :Message = CommandArg()):
    para = str(args).split(" ")#获取参数
    temp = para[0].split("qq=")
    async with db.transaction():
        try:
            UserID = int(temp[1].strip("]"))
            Gold = int(para[1])
        except:
            await SendGolds.finish("参数出错")
        SendUserGold = await BagUser.get_gold(event.user_id,event.group_id)
        if(SendUserGold < Gold):
                await SendGolds.finish("余额不足,您的余额为"+str(SendUserGold))
        else:
            if(Gold < 0):
                await BagUser.spend_gold(event.user_id,event.group_id,100)
                await SendGolds.finish("反向转账是吧！"+"\n你的金额-100！！！！！！！")
            else:
                await BagUser.add_gold(UserID,event.group_id,Gold)
                await BagUser.spend_gold(event.user_id,event.group_id,Gold)
                UserGold = await BagUser.get_gold(UserID,event.group_id)
                SendUserGold = await BagUser.get_gold(event.user_id,event.group_id)
    await SendGolds.finish("交易成功\n转帐方ID:"+str(event.user_id)+"\n收款方ID:"+str(UserID)+"\n交易金额"+str(Gold)+"\n转账方余额"+str(SendUserGold)+"\n收款方余额"+str(UserGold))

@SetGolds.handle()
async def _(event :GroupMessageEvent,args :Message = CommandArg()):
    para = str(args).split(" ")#获取参数
    temp = para[0].split("qq=")
    async with db.transaction():
        try:
            UserID = int(temp[1].strip("]"))
            Gold = int(para[1])
        except:
            await SendGolds.finish("参数出错")
        SendUserGold = await BagUser.get_gold(event.user_id,event.group_id)
        await BagUser.add_gold(UserID,event.group_id,Gold)
        UserGold = await BagUser.get_gold(UserID,event.group_id)
        SendUserGold = await BagUser.get_gold(event.user_id,event.group_id)
    await SendGolds.finish("交易成功\n转帐方ID:"+str(event.user_id)+"\n收款方ID:"+str(UserID)+"\n交易金额"+str(Gold)+"\n转账方余额"+str(SendUserGold)+"\n收款方余额"+str(UserGold))