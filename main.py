from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.event import MessageChain
import asyncio


@register("helloworld", "YourName", "一个简单的 Hello World 插件（含主动消息）", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        pass

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令"""

        user_name = event.get_sender_name()
        message_str = event.message_str
        logger.info(event.get_messages())

        # 先回复用户（你的原功能）
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!")

        # 取出 unified_msg_origin（主动消息必须）
        umo = event.unified_msg_origin
        logger.info(f"[helloworld] 保存的 unified_msg_origin = {umo}")

        # 在后台启动 5 秒后主动推送任务
        asyncio.create_task(self.delayed_push(umo))


    async def delayed_push(self, umo: str):
        """5 秒后主动推送消息"""
        await asyncio.sleep(5)

        logger.info("[delayed_push] 任务开始执行，准备主动发送消息")

        # 正确构造 MessageChain（官方推荐写法）
        chain = MessageChain().message("⏰ 这是 5 秒后的主动消息！")

        # 主动推送消息
        result = await self.context.send_message(umo, chain)

        logger.info(f"[delayed_push] 主动消息发送结果：{result}")


    async def terminate(self):
        pass
