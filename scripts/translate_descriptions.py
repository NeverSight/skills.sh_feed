#!/usr/bin/env python3
"""
批量翻译 description_en.txt 到 description_cn.txt

支持的翻译方式:
1. OpenAI API (推荐，翻译质量最高)
2. DeepL API (高质量翻译)
3. Google Translate (免费，使用 googletrans 库)

使用方法:
    # 使用 OpenAI (需要设置 OPENAI_API_KEY 环境变量)
    python translate_descriptions.py --provider openai
    
    # 使用 DeepL (需要设置 DEEPL_API_KEY 环境变量)
    python translate_descriptions.py --provider deepl
    
    # 使用免费的 Google Translate
    python translate_descriptions.py --provider google
    
    # 只翻译前 100 个文件 (测试用)
    python translate_descriptions.py --provider openai --limit 100
    
    # 从第 200 个文件开始翻译 (断点续传)
    python translate_descriptions.py --provider openai --skip 200
    
    # 使用并发加速
    python translate_descriptions.py --provider openai --workers 5
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Callable

# 基础目录
BASE_DIR = Path(__file__).parent.parent / "data" / "skills-md"
PROGRESS_FILE = Path(__file__).parent / ".translate_progress.json"


def find_all_en_files() -> list[Path]:
    """找到所有需要翻译的英文描述文件"""
    en_files = []
    for en_file in BASE_DIR.rglob("description_en.txt"):
        cn_file = en_file.parent / "description_cn.txt"
        # 只处理还没有中文翻译的文件
        if not cn_file.exists():
            en_files.append(en_file)
    return sorted(en_files)


def load_progress() -> set:
    """加载已完成的翻译进度"""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_progress(completed: set):
    """保存翻译进度"""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(list(completed), f)


# ============= 翻译提供者 =============

def translate_with_openai(text: str, api_key: str) -> str:
    """使用 OpenAI API 翻译"""
    try:
        from openai import OpenAI
    except ImportError:
        print("请安装 openai: pip install openai")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 使用较便宜的模型
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的技术文档翻译专家。请将以下英文技术描述翻译成简体中文。保持专业术语的准确性，翻译要简洁通顺。只输出翻译结果，不要添加任何解释。"
            },
            {
                "role": "user", 
                "content": text
            }
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()


def translate_with_deepl(text: str, api_key: str) -> str:
    """使用 DeepL API 翻译"""
    try:
        import deepl
    except ImportError:
        print("请安装 deepl: pip install deepl")
        sys.exit(1)
    
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang="ZH")
    return result.text


def translate_with_google(text: str, api_key: str = None) -> str:
    """使用 Google Translate (免费库) 翻译"""
    try:
        from googletrans import Translator
    except ImportError:
        print("请安装 googletrans: pip install googletrans==4.0.0-rc1")
        sys.exit(1)
    
    translator = Translator()
    # 添加重试逻辑
    for attempt in range(3):
        try:
            result = translator.translate(text, src='en', dest='zh-cn')
            return result.text
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
            else:
                raise e
    return text


def translate_with_ollama(text: str, api_key: str = None) -> str:
    """使用本地 Ollama 翻译 (免费，需要本地运行 Ollama)"""
    try:
        import requests
    except ImportError:
        print("请安装 requests: pip install requests")
        sys.exit(1)
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",  # 或其他支持中文的模型
            "prompt": f"请将以下英文技术描述翻译成简体中文，只输出翻译结果：\n\n{text}",
            "stream": False
        }
    )
    
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        raise Exception(f"Ollama API error: {response.status_code}")


# ============= 主翻译逻辑 =============

def translate_file(
    en_file: Path,
    translate_fn: Callable[[str, str], str],
    api_key: str,
    dry_run: bool = False
) -> tuple[Path, bool, str]:
    """翻译单个文件"""
    try:
        # 读取英文内容
        en_text = en_file.read_text(encoding="utf-8").strip()
        
        if not en_text:
            return en_file, False, "空文件"
        
        # 检查是否已经是中文（有些文件可能已经是中文了）
        if any('\u4e00' <= c <= '\u9fff' for c in en_text):
            # 如果已经包含大量中文，直接复制
            chinese_chars = sum(1 for c in en_text if '\u4e00' <= c <= '\u9fff')
            if chinese_chars / len(en_text) > 0.3:
                cn_text = en_text
            else:
                cn_text = translate_fn(en_text, api_key)
        else:
            # 翻译
            cn_text = translate_fn(en_text, api_key)
        
        # 写入中文文件
        cn_file = en_file.parent / "description_cn.txt"
        
        if not dry_run:
            cn_file.write_text(cn_text + "\n", encoding="utf-8")
        
        return en_file, True, cn_text[:50] + "..." if len(cn_text) > 50 else cn_text
        
    except Exception as e:
        return en_file, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="批量翻译 description_en.txt 到 description_cn.txt")
    parser.add_argument(
        "--provider", 
        choices=["openai", "deepl", "google", "ollama"],
        default="openai",
        help="翻译提供者 (默认: openai)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="限制翻译的文件数量 (0 表示全部)"
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="跳过前 N 个文件"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=3,
        help="并发工作线程数 (默认: 3)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示要翻译的文件，不实际翻译"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新翻译已存在的文件"
    )
    
    args = parser.parse_args()
    
    # 获取 API key
    api_key = None
    if args.provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("错误: 请设置 OPENAI_API_KEY 环境变量")
            print("export OPENAI_API_KEY='your-api-key'")
            sys.exit(1)
        translate_fn = translate_with_openai
    elif args.provider == "deepl":
        api_key = os.environ.get("DEEPL_API_KEY")
        if not api_key:
            print("错误: 请设置 DEEPL_API_KEY 环境变量")
            sys.exit(1)
        translate_fn = translate_with_deepl
    elif args.provider == "google":
        translate_fn = translate_with_google
        print("提示: 使用免费的 Google Translate，可能有速率限制")
    elif args.provider == "ollama":
        translate_fn = translate_with_ollama
        print("提示: 使用本地 Ollama，请确保 Ollama 正在运行")
    
    # 找到所有需要翻译的文件
    print("正在扫描文件...")
    
    if args.force:
        # 强制模式：找到所有英文文件
        en_files = list(BASE_DIR.rglob("description_en.txt"))
    else:
        # 只找没有翻译的文件
        en_files = find_all_en_files()
    
    en_files = sorted(en_files)
    
    # 应用 skip 和 limit
    if args.skip > 0:
        en_files = en_files[args.skip:]
    if args.limit > 0:
        en_files = en_files[:args.limit]
    
    total = len(en_files)
    print(f"找到 {total} 个文件需要翻译")
    
    if total == 0:
        print("没有需要翻译的文件")
        return
    
    if args.dry_run:
        print("\n[DRY RUN] 以下文件将被翻译:")
        for f in en_files[:20]:
            print(f"  - {f.relative_to(BASE_DIR)}")
        if total > 20:
            print(f"  ... 还有 {total - 20} 个文件")
        return
    
    # 开始翻译
    print(f"\n开始翻译 (使用 {args.provider}, {args.workers} 个工作线程)...")
    print("-" * 60)
    
    completed = 0
    failed = 0
    start_time = time.time()
    
    # 对于 Google Translate，减少并发以避免被封
    if args.provider == "google":
        args.workers = 1
    
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(translate_file, f, translate_fn, api_key): f 
            for f in en_files
        }
        
        for future in as_completed(futures):
            en_file, success, message = future.result()
            completed += 1
            
            if success:
                print(f"[{completed}/{total}] ✓ {en_file.parent.name}: {message}")
            else:
                failed += 1
                print(f"[{completed}/{total}] ✗ {en_file.parent.name}: {message}")
            
            # 显示进度
            if completed % 100 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed
                remaining = (total - completed) / rate if rate > 0 else 0
                print(f"\n--- 进度: {completed}/{total} ({completed/total*100:.1f}%), "
                      f"速率: {rate:.1f}/秒, 预计剩余: {remaining/60:.1f}分钟 ---\n")
            
            # 对于免费 API，添加延迟避免被封
            if args.provider == "google":
                time.sleep(0.5)
    
    # 完成统计
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"翻译完成!")
    print(f"  成功: {completed - failed}")
    print(f"  失败: {failed}")
    print(f"  耗时: {elapsed/60:.1f} 分钟")
    print(f"  速率: {completed/elapsed:.1f} 文件/秒")


if __name__ == "__main__":
    main()
