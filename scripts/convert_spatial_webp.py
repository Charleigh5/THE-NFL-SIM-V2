import os
import sys
from pathlib import Path
from PIL import Image

def convert_spatial_assets():
    repo_root = Path(__file__).resolve().parent.parent
    spatial_dir = repo_root / "frontend" / "public" / "assets" / "spatial"

    if not spatial_dir.exists():
        print(f"Error: Directory not found: {spatial_dir}", file=sys.stderr)
        sys.exit(1)

    jpg_files = sorted(list(spatial_dir.glob("*.jpg")))
    if not jpg_files:
        print(f"No .jpg files found in {spatial_dir}")
        return

    print(f"Found {len(jpg_files)} .jpg files in {spatial_dir}\n")
    print(f"{'Filename':<45} | {'Original (KB)':<14} | {'WebP (KB)':<12} | {'Savings':<10}")
    print("-" * 88)

    total_orig_bytes = 0
    total_webp_bytes = 0

    for jpg_path in jpg_files:
        webp_path = jpg_path.with_suffix(".webp")
        orig_size = jpg_path.stat().st_size
        total_orig_bytes += orig_size

        with Image.open(jpg_path) as img:
            if img.mode in ("RGBA", "LA"):
                img.save(webp_path, "WEBP", quality=85)
            else:
                img_rgb = img.convert("RGB")
                img_rgb.save(webp_path, "WEBP", quality=85)

        webp_size = webp_path.stat().st_size
        total_webp_bytes += webp_size

        savings_pct = ((orig_size - webp_size) / orig_size) * 100
        print(
            f"{jpg_path.name:<45} | "
            f"{orig_size / 1024:>11.2f} KB | "
            f"{webp_size / 1024:>9.2f} KB | "
            f"{savings_pct:>8.2f}%"
        )

    print("-" * 88)
    overall_savings_pct = ((total_orig_bytes - total_webp_bytes) / total_orig_bytes) * 100
    print(
        f"{'TOTAL':<45} | "
        f"{total_orig_bytes / 1024:>11.2f} KB | "
        f"{total_webp_bytes / 1024:>9.2f} KB | "
        f"{overall_savings_pct:>8.2f}%\n"
    )
    print(f"Original total: {total_orig_bytes:,} bytes ({total_orig_bytes / (1024 * 1024):.2f} MB)")
    print(f"New WebP total: {total_webp_bytes:,} bytes ({total_webp_bytes / (1024 * 1024):.2f} MB)")
    print(f"Total storage reduction: {(total_orig_bytes - total_webp_bytes):,} bytes ({((total_orig_bytes - total_webp_bytes) / (1024 * 1024)):.2f} MB saved, {overall_savings_pct:.2f}% reduction)")

if __name__ == "__main__":
    convert_spatial_assets()
