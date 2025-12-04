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

    # -------------------------------------------------------
    # ⭐ 新增 delayhello 指令：测试主动消息推送
    # -------------------------------------------------------
    @filter.command("delayhello")
    async def delayhello(self, event: AstrMessageEvent):
        """发送后 5 秒主动推送一条消息"""

        # 保存会话 ID（主动消息必须）
        self.saved_umo = event.unified_msg_origin

        user_name = event.get_sender_name()
        message_str = event.message_str
        logger.info(f"收到 delayhello 指令，来自：{user_name}")

        # 先回复用户
        yield event.plain_result(
            f"好的 {user_name}，我将在 5 秒后主动给你发一条消息！你刚刚说的是：{message_str}"
        )

        # 创建异步任务，不阻塞机器人
        asyncio.create_task(self.delay_task())

    # 实际执行延迟推送
    async def delay_task(self):
        await asyncio.sleep(5)

        if not self.saved_umo:
            logger.error("没有保存 unified_msg_origin，主动消息发送失败")
            return

        chain = MessageChain().text("⏰ 这是我 5 秒后的主动消息推送！")

        await self.context.send_message(self.saved_umo, chain)

        logger.info("主动消息发送成功！")

    async def terminate(self):
        """插件卸载时执行（可选）"""
        pass
