import json
import requests
import logging

logger = logging.getLogger(__name__)

class WebhookSender:
    def __init__(self, webhook_url: str):
        """初始化 Webhook 发送器"""
        self.webhook_url = webhook_url

    def send_daily_report(self, title: str, summary: dict) -> bool:
        """发送每日爬取合并通知摘要"""
        try:
            # Assembly of text links
            success_games = summary.get("success_games", [])
            failed_games = summary.get("failed_games", [])
            
            success_text = "\n".join([f"• [{g['title']}]({g['url'].replace('bearclicker.net', 'bearclicker-ebon.vercel.app')})" for g in success_games]) if success_games else "无"
            failed_text = "\n".join([f"• {g}" for g in failed_games]) if failed_games else "无"
            
            # Assembly of the card elements
            card = {
                "config": {"wide_screen_mode": True},
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": "blue" if not failed_games else "yellow"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {"tag": "lark_md", "content": f"**今日共上线 {len(success_games)} 个游戏**\n---\n**成功列表:**\n{success_text}\n\n**失败或跳过:**\n{failed_text}"}
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {"tag": "plain_text", "content": f"IndexNow 推送状态: {'✅ 成功' if summary.get('indexnow_status') is True else ('❌ 失败' if summary.get('indexnow_status') is False else '⚪ 无数据不需要推送')}"}
                        ]
                    }
                ]
            }

            payload = {
                "msg_type": "interactive",
                "card": card
            }

            return self._send_payload(payload)

        except Exception as e:
            logger.error(f"发送飞书消息异常: {str(e)}")
            return False

    def _send_payload(self, payload: dict) -> bool:
        """底层方法：发送消息到飞书 Webhook"""
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("StatusCode") == 0 or result.get("code") == 0:
                logger.info("飞书消息发送成功")
                return True
            else:
                logger.error(f"飞书消息发送失败: {result}")
                return False
        except Exception as e:
            logger.error(f"发送消息异常: {str(e)}")
            return False

def create_webhook_sender(config_path: str = "config.json") -> WebhookSender:
    import os
    # if feishu_webhook_url environment variable exists, prefer it
    env_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if env_url:
        return WebhookSender(env_url)
        
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        webhook_config = config.get('webhook', {})
        if not webhook_config.get('url'):
            return None
            
        return WebhookSender(webhook_config['url'])
    except Exception:
        return None

if __name__ == "__main__":
    # Test Payload Builder
    sender = WebhookSender("https://open.feishu.cn/open-apis/bot/v2/hook/dummy")
    print("Test Payload structure created successfully.")
