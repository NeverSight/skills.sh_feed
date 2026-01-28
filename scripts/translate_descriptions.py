#!/usr/bin/env python3
"""
批量翻译 description_en.txt 到 description_cn.txt (使用免费 Google Translate)

使用方法:
    # 翻译所有缺失的中文描述
    python translate_descriptions.py
    
    # 只翻译前 100 个文件 (测试用)
    python translate_descriptions.py --limit 100
    
    # 从第 200 个文件开始翻译 (断点续传)
    python translate_descriptions.py --skip 200
    
    # 测试模式
    python translate_descriptions.py --dry-run
"""

import sys
import time
import argparse
from pathlib import Path

# 基础目录
BASE_DIR = Path(__file__).parent.parent / "data" / "skills-md"


def find_all_en_files() -> list[Path]:
    """找到所有需要翻译的英文描述文件"""
    en_files = []
    for en_file in BASE_DIR.rglob("description_en.txt"):
        cn_file = en_file.parent / "description_cn.txt"
        # 只处理还没有中文翻译的文件
        if not cn_file.exists():
            en_files.append(en_file)
    return sorted(en_files)


def translate_with_google(text: str) -> str:
    """使用 Google Translate (免费) 翻译"""
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("请安装 deep-translator: pip install deep-translator")
        sys.exit(1)
    
    translator = GoogleTranslator(source='en', target='zh-CN')
    # 添加重试逻辑
    for attempt in range(3):
        try:
            result = translator.translate(text)
            return result
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                raise e
    return text


# ============= 主翻译逻辑 =============

def translate_file(en_file: Path, dry_run: bool = False) -> tuple[Path, bool, str]:
    """翻译单个文件"""
    try:
        # 读取英文内容
        en_text = en_file.read_text(encoding="utf-8").strip()
        
        if not en_text:
            return en_file, False, "空文件"
        
        # 检查是否已经是中文（有些文件可能已经是中文了）
        chinese_chars = sum(1 for c in en_text if '\u4e00' <= c <= '\u9fff')
        if len(en_text) > 0 and chinese_chars / len(en_text) > 0.3:
            cn_text = en_text  # 已经是中文，直接复制
        else:
            cn_text = translate_with_google(en_text)
        
        # 写入中文文件
        cn_file = en_file.parent / "description_cn.txt"
        
        if not dry_run:
            cn_file.write_text(cn_text + "\n", encoding="utf-8")
        
        return en_file, True, cn_text[:50] + "..." if len(cn_text) > 50 else cn_text
        
    except Exception as e:
        return en_file, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="批量翻译 description_en.txt 到 description_cn.txt (Google Translate)")
    parser.add_argument("--limit", type=int, default=0, help="限制翻译的文件数量 (0 表示全部)")
    parser.add_argument("--skip", type=int, default=0, help="跳过前 N 个文件")
    parser.add_argument("--dry-run", action="store_true", help="只显示要翻译的文件，不实际翻译")
    parser.add_argument("--force", action="store_true", help="强制重新翻译已存在的文件")
    
    args = parser.parse_args()
    
    # 找到所有需要翻译的文件
    print("正在扫描文件...")
    
    if args.force:
        en_files = list(BASE_DIR.rglob("description_en.txt"))
    else:
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
    print(f"\n开始翻译 (使用 Google Translate)...")
    print("-" * 60)
    
    completed = 0
    failed = 0
    start_time = time.time()
    
    for en_file in en_files:
        en_file, success, message = translate_file(en_file)
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
        
        # 添加延迟避免被封
        time.sleep(0.3)
    
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
