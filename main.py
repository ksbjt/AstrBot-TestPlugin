from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.event import MessageChain
import asyncio


@register("helloworld", "YourName", "一个简单的 Hello World 插件（含主动消息示例）", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.saved_umo = None  # 用于保存 unified_msg_origin（主动消息必须）

    async def initialize(self):
        """插件初始化（可选）"""
        pass

    # -------------------------------------------------------
    # ⭐ 保留你的原本 helloworld 指令，不做修改
    # -------------------------------------------------------
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令"""

        user_name = event.get_sender_name()
        message_str = event.message_str
        message_chain = event.get_messages()

        logger.info(message_chain)

        yield event.plain_result(
            f"Hello, {user_name}, 你发了 {message_str}!"
        )

    @filter.command("delayhello")
    async def delayhello(self, event: AstrMessageEvent):
        umo = event.unified_msg_origin
        logger.info(f"[delayhello] 保存的 UMO = {umo}")

        # 正常回复
        await event.send(f"消息已收到，我将在 5 秒后主动发送消息。")

        # 不使用 yield，避免上下文结束
        asyncio.create_task(self.delayed_push(umo))

    async def delayed_push(self, umo: str):
        await asyncio.sleep(5)

        chain = MessageChain().text("⏰ 这是 5 秒后的主动消息（SDK 版）")

        logger.info("[delayed_push] 开始主动推送消息")

        result = await self.context.send_message(umo, chain)

        logger.info(f"[delayed_push] 主动消息返回：{result}")

    async def terminate(self):
        """插件卸载时执行（可选）"""
        pass
