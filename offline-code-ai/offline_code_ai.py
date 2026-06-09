#!/usr/bin/env python3
"""
Small offline-first coding assistant client for local Ollama models.

It uses only Python's standard library so it can run without pip installs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys
import textwrap
import urllib.error
import urllib.request
from typing import Any


DEFAULT_CONFIG = {
    "model": "qwen2.5-coder:7b",
    "ollama_url": "http://127.0.0.1:11434/api/chat",
    "temperature": 0.2,
    "max_context_chars": 12000,
    "history_file": "chat_history.md",
}

SYSTEM_PROMPT = """\
You are an offline coding assistant for a university programming test.
Answer in Japanese unless the user asks otherwise.
Focus on correct, simple, readable code.
Prefer standard libraries and explain the important idea briefly.
If the prompt is ambiguous, state one reasonable assumption and continue.
Do not invent unavailable packages, web links, or online-only steps.
When giving code, include a short usage example when helpful.
"""


def load_config(path: pathlib.Path | None) -> dict[str, Any]:
    config = dict(DEFAULT_CONFIG)
    if path is None:
        default_path = pathlib.Path("config.json")
        path = default_path if default_path.exists() else None
    if path is not None and path.exists():
        with path.open("r", encoding="utf-8") as f:
            loaded = json.load(f)
        config.update(loaded)
    return config


def read_text_file(path: pathlib.Path, limit: int) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > limit:
        return text[:limit] + "\n\n[context truncated]\n"
    return text


def build_context(paths: list[pathlib.Path], limit: int) -> str:
    chunks: list[str] = []
    remaining = limit
    for path in paths:
        if remaining <= 0:
            break
        if not path.exists():
            chunks.append(f"\n[missing context file: {path}]\n")
            continue
        text = read_text_file(path, remaining)
        remaining -= len(text)
        chunks.append(f"\n--- context: {path} ---\n{text}\n")
    return "".join(chunks)


def ask_ollama(
    *,
    url: str,
    model: str,
    user_prompt: str,
    context: str,
    temperature: float,
) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if context.strip():
        messages.append(
            {
                "role": "user",
                "content": "Use this local reference material when relevant:\n" + context,
            }
        )
    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"temperature": temperature},
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Ollamaに接続できませんでした。別のPowerShellで `ollama serve` を起動し、"
            "モデルを事前に `ollama pull ...` で取得済みか確認してください。"
        ) from exc

    result = json.loads(body)
    return result.get("message", {}).get("content", "").strip()


def save_history(path: pathlib.Path, prompt: str, answer: str) -> None:
    timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = f"\n\n## {timestamp}\n\n### Prompt\n\n{prompt}\n\n### Answer\n\n{answer}\n"
    with path.open("a", encoding="utf-8") as f:
        f.write(block)


def print_answer(answer: str) -> None:
    print()
    print(answer)
    print()


def interactive_loop(config: dict[str, Any], context: str) -> None:
    print("Offline Code AI")
    print("終了: /exit  履歴保存: chat_history.md")
    print()

    while True:
        try:
            prompt = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if not prompt:
            continue
        if prompt.lower() in {"/exit", "exit", "quit", "/quit"}:
            return

        answer = ask_ollama(
            url=config["ollama_url"],
            model=config["model"],
            user_prompt=prompt,
            context=context,
            temperature=float(config["temperature"]),
        )
        print_answer(answer)
        save_history(pathlib.Path(config["history_file"]), prompt, answer)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Offline coding assistant client for local Ollama models."
    )
    parser.add_argument("--ask", help="Ask one question and exit.")
    parser.add_argument("--explain", type=pathlib.Path, help="Explain a source file.")
    parser.add_argument("--context", nargs="*", type=pathlib.Path, default=[])
    parser.add_argument("--config", type=pathlib.Path)
    parser.add_argument("--model")
    parser.add_argument("--url", dest="ollama_url")
    parser.add_argument("--temperature", type=float)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(args.config)
    for key in ("model", "ollama_url", "temperature"):
        value = getattr(args, key, None)
        if value is not None:
            config[key] = value

    context = build_context(args.context, int(config["max_context_chars"]))

    if args.explain:
        source = read_text_file(args.explain, int(config["max_context_chars"]))
        prompt = textwrap.dedent(
            f"""\
            次のコードを説明し、バグや改善点があれば短く指摘してください。

            File: {args.explain}

            ```text
            {source}
            ```
            """
        )
    else:
        prompt = args.ask

    try:
        if prompt:
            answer = ask_ollama(
                url=config["ollama_url"],
                model=config["model"],
                user_prompt=prompt,
                context=context,
                temperature=float(config["temperature"]),
            )
            print_answer(answer)
            save_history(pathlib.Path(config["history_file"]), prompt, answer)
        else:
            interactive_loop(config, context)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
