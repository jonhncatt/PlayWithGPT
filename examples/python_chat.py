"""使用 OpenAI Python SDK 构建一个简单的命令行聊天机器人。"""

from __future__ import annotations

import os
import sys
from typing import List

from openai import OpenAI


SYSTEM_PROMPT = "You are a helpful assistant that answers in Chinese when possible."
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def build_messages(history: List[dict], user_input: str) -> List[dict]:
    """拼接系统提示与历史消息，生成新的消息列表。"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        *history,
        {"role": "user", "content": user_input},
    ]


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("请先设置 OPENAI_API_KEY 环境变量")

    client = OpenAI(api_key=api_key)
    history: List[dict] = []

    print("🤖 输入内容，按 Ctrl+C 退出。")

    try:
        while True:
            user_input = input("你：").strip()
            if not user_input:
                continue

            messages = build_messages(history, user_input)
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
            )

            answer = response.choices[0].message.content
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": answer})

            print(f"GPT：{answer}\n")
    except KeyboardInterrupt:
        print("\n会话结束，感谢使用 PlayWithGPT！")
        sys.exit(0)


if __name__ == "__main__":
    main()
