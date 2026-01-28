#!/usr/bin/env python3
"""
Batch translate description_en.txt to description_cn.txt (using free Google Translate)

Usage:
    # Translate all missing Chinese descriptions
    python translate_descriptions.py
    
    # Only translate first 100 files (for testing)
    python translate_descriptions.py --limit 100
    
    # Start translation from file 200 (resume from checkpoint)
    python translate_descriptions.py --skip 200
    
    # Test mode
    python translate_descriptions.py --dry-run
"""

import sys
import time
import argparse
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent / "data" / "skills-md"


def find_all_en_files() -> list[Path]:
    """Find all English description files that need translation"""
    en_files = []
    for en_file in BASE_DIR.rglob("description_en.txt"):
        cn_file = en_file.parent / "description_cn.txt"
        # Only process files that don't have Chinese translation yet
        if not cn_file.exists():
            en_files.append(en_file)
    return sorted(en_files)


def translate_with_google(text: str) -> str:
    """Translate using Google Translate (free)"""
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Please install deep-translator: pip install deep-translator")
        sys.exit(1)
    
    translator = GoogleTranslator(source='en', target='zh-CN')
    # Add retry logic
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


# ============= Main translation logic =============

def translate_file(en_file: Path, dry_run: bool = False) -> tuple[Path, bool, str]:
    """Translate a single file"""
    try:
        # Read English content
        en_text = en_file.read_text(encoding="utf-8").strip()
        
        if not en_text:
            return en_file, False, "Empty file"
        
        # Check if content is already Chinese (some files may already be in Chinese)
        chinese_chars = sum(1 for c in en_text if '\u4e00' <= c <= '\u9fff')
        if len(en_text) > 0 and chinese_chars / len(en_text) > 0.3:
            cn_text = en_text  # Already Chinese, copy directly
        else:
            cn_text = translate_with_google(en_text)
        
        # Write Chinese file
        cn_file = en_file.parent / "description_cn.txt"
        
        if not dry_run:
            cn_file.write_text(cn_text + "\n", encoding="utf-8")
        
        return en_file, True, cn_text[:50] + "..." if len(cn_text) > 50 else cn_text
        
    except Exception as e:
        return en_file, False, str(e)


def main():
    parser = argparse.ArgumentParser(description="Batch translate description_en.txt to description_cn.txt (Google Translate)")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of files to translate (0 for all)")
    parser.add_argument("--skip", type=int, default=0, help="Skip first N files")
    parser.add_argument("--dry-run", action="store_true", help="Only show files to be translated, don't actually translate")
    parser.add_argument("--force", action="store_true", help="Force re-translate existing files")
    
    args = parser.parse_args()
    
    # Find all files that need translation
    print("Scanning files...")
    
    if args.force:
        en_files = list(BASE_DIR.rglob("description_en.txt"))
    else:
        en_files = find_all_en_files()
    
    en_files = sorted(en_files)
    
    # Apply skip and limit
    if args.skip > 0:
        en_files = en_files[args.skip:]
    if args.limit > 0:
        en_files = en_files[:args.limit]
    
    total = len(en_files)
    print(f"Found {total} files to translate")
    
    if total == 0:
        print("No files need translation")
        return
    
    if args.dry_run:
        print("\n[DRY RUN] The following files will be translated:")
        for f in en_files[:20]:
            print(f"  - {f.relative_to(BASE_DIR)}")
        if total > 20:
            print(f"  ... and {total - 20} more files")
        return
    
    # Start translation
    print(f"\nStarting translation (using Google Translate)...")
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
        
        # Show progress
        if completed % 100 == 0:
            elapsed = time.time() - start_time
            rate = completed / elapsed
            remaining = (total - completed) / rate if rate > 0 else 0
            print(f"\n--- Progress: {completed}/{total} ({completed/total*100:.1f}%), "
                  f"Rate: {rate:.1f}/sec, Estimated remaining: {remaining/60:.1f} min ---\n")
        
        # Add delay to avoid rate limiting
        time.sleep(0.3)
    
    # Final statistics
    elapsed = time.time() - start_time
    print("\n" + "=" * 60)
    print(f"Translation completed!")
    print(f"  Success: {completed - failed}")
    print(f"  Failed: {failed}")
    print(f"  Time: {elapsed/60:.1f} min")
    print(f"  Rate: {completed/elapsed:.1f} files/sec")


if __name__ == "__main__":
    main()
