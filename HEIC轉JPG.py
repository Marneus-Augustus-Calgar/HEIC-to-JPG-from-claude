"""HEIC 轉 JPG 工具

用法:
    python heic2jpg.py                      # 轉換目前資料夾內所有 HEIC
    python heic2jpg.py 照片.heic            # 轉換單一檔案
    python heic2jpg.py 資料夾 -r            # 遞迴轉換資料夾(含子資料夾)
    python heic2jpg.py 資料夾 -o 輸出資料夾 -q 90

需先安裝:
    pip install pillow pillow-heif
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
    from pillow_heif import register_heif_opener
except ImportError:
    sys.exit("缺少套件,請先執行: pip install pillow pillow-heif")

register_heif_opener()

HEIC_EXTS = {".heic", ".heif"}


def find_heic(path: Path, recursive: bool):
    if path.is_file():
        return [path] if path.suffix.lower() in HEIC_EXTS else []
    pattern = "**/*" if recursive else "*"
    return sorted(p for p in path.glob(pattern) if p.is_file() and p.suffix.lower() in HEIC_EXTS)


def convert(src: Path, dst: Path, quality: int, overwrite: bool) -> str:
    if dst.exists() and not overwrite:
        return "略過(已存在)"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as img:
        exif = img.info.get("exif")
        icc = img.info.get("icc_profile")
        rgb = img.convert("RGB")
        kwargs = {"quality": quality, "optimize": True}
        if exif:
            kwargs["exif"] = exif
        if icc:
            kwargs["icc_profile"] = icc
        rgb.save(dst, "JPEG", **kwargs)
    return "完成"


def main():
    # 打包成 exe 時的拖放行為:沒拖檔案就顯示說明,有失敗才停住視窗
    frozen = getattr(sys, "frozen", False)
    if frozen and len(sys.argv) == 1:
        print("請把 HEIC 檔案或資料夾拖到這個 exe 上進行轉換。")
        input("\n按 Enter 關閉...")
        return
    if frozen:
        sys.argv.insert(1, "-r")

    parser = argparse.ArgumentParser(description="HEIC 轉 JPG")
    parser.add_argument("inputs", nargs="*", default=["."], help="HEIC 檔案或資料夾(預設: 目前資料夾)")
    parser.add_argument("-o", "--output", help="輸出資料夾(預設: 與原檔同一位置)")
    parser.add_argument("-q", "--quality", type=int, default=95, help="JPG 品質 1-100(預設 95)")
    parser.add_argument("-r", "--recursive", action="store_true", help="包含子資料夾")
    parser.add_argument("-f", "--overwrite", action="store_true", help="覆寫已存在的 JPG")
    parser.add_argument("--delete", action="store_true", help="轉換成功後刪除原始 HEIC")
    args = parser.parse_args()

    out_dir = Path(args.output) if args.output else None
    ok = fail = skip = 0

    for raw in args.inputs:
        base = Path(raw)
        if not base.exists():
            print(f"[找不到] {base}")
            fail += 1
            continue
        files = find_heic(base, args.recursive)
        if not files:
            print(f"[無 HEIC] {base}")
        for src in files:
            if out_dir:
                rel = src.relative_to(base) if base.is_dir() else Path(src.name)
                dst = (out_dir / rel).with_suffix(".jpg")
            else:
                dst = src.with_suffix(".jpg")
            try:
                status = convert(src, dst, args.quality, args.overwrite)
                print(f"[{status}] {src} -> {dst}")
                if status == "完成":
                    ok += 1
                    if args.delete:
                        src.unlink()
                else:
                    skip += 1
            except Exception as e:
                print(f"[失敗] {src}: {e}")
                fail += 1

    print(f"\n成功 {ok} / 略過 {skip} / 失敗 {fail}")
    if frozen and fail:
        input("\n按 Enter 關閉...")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
