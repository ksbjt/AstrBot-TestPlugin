from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.event import MessageChain
import asyncio


@register("helloworld", "YourName", "一个 Hello World 插件（含主动消息函数）", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        pass

    # ⭐ 通用主动推送函数
    async def Print(self, umo: str, text: str):
        """向指定会话主动推送文本消息"""
        chain = MessageChain().message(text)
        result = await self.context.send_message(umo, chain)
        logger.info(f"[Print] 主动消息发送结果：{result}")
        return result


    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """helloworld 指令"""

        user_name = event.get_sender_name()
        message_str = event.message_str

        # 先正常回复
        yield event.plain_result(f"Hello, {user_name}, 你发了 {message_str}!")

        # 获取会话ID（必须）
        umo = event.unified_msg_origin

        # 5 秒后主动推送
        asyncio.create_task(self.delayed_push(umo))


    async def delayed_push(self, umo: str):
        """延迟主动推送"""
        await asyncio.sleep(5)

        # 调用我们刚写的通用函数
        await self.Print(umo, "⏰ 这是来自 Print() 的主动推送！")


    async def terminate(self):
        pass
