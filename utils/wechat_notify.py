# utils/wechat_notify.py
import os
import json
import requests
from datetime import datetime


def send_wechat_message(results):
    webhook_url = os.getenv("WECHAT_WEBHOOK")

    # 计算测试持续时间
    duration = results['end_time'] - results['start_time']

    # 构建Markdown内容
    markdown_content = f"""**自动化测试完成通知**
    > **测试概要**
    > 开始时间：{results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}
    > 持续时间：{duration.total_seconds():.2f}秒
    >
    > **测试结果**
    > ✅ 通过用例：{results['passed']}
    > ❌ 失败用例：{results['failed']}
    > 📊 通过率：{results['passed'] / results['total'] * 100:.2f}%
    >
    > **失败详情**
    > {get_failed_details(results['failed_cases'])}
    >
    > [查看完整报告](http://your-report-domain.com/report)
    """

    # 构造请求体
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": markdown_content
        }
    }

    # 发送请求
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
    except Exception as e:
        print(f"企业微信消息发送失败: {str(e)}")


def get_failed_details(failed_cases):
    if not failed_cases:
        return "无失败用例"
    details = []
    for idx, case in enumerate(failed_cases, 1):
        details.append(f"{idx}. `{case['name']}`\n   {case['error'][:100]}...")
    return "\n".join(details)



