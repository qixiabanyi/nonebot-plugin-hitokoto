import httpx
from nonebot import get_bot, logger, on_command
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot_plugin_apscheduler import scheduler

hitokoto_matcher = on_command("一言", aliases={"一句"},priority=0,block=False)

@hitokoto_matcher.handle()
async def hitokoto(matcher: Matcher, args: Message = CommandArg()):
    if args:
        return
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=h")
    if response.is_error:
        logger.error("获取一言失败")
        return
    data = response.json()
    msg = data["hitokoto"]
    add = ""
    if works := data["from"]:
        add += f"《{works}》"
    if from_who := data["from_who"]:
        add += f"{from_who}"
    if add:
        msg += f"\n——{add}"
    await matcher.finish(msg)

async def send_hitokoto():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=h")
    if response.is_error:
        logger.error("获取一言失败")
        return
    data = response.json()
    msg = data["hitokoto"]
    add = ""
    if works := data["from"]:
        add += f"《{works}》"
    if from_who := data["from_who"]:
        add += f"{from_who}"
    if add:
        msg += f"\n——{add}"
    # 假设你想要发送到特定的群组或用户，你需要获取bot的实例并发送消息
    bot= get_bot()
    await bot.send_group_msg(group_id=group_id, message=msg)
if scheduler:
    scheduler.add_job(send_hitokoto, 'cron', hour=12, id='send_hitokoto')
