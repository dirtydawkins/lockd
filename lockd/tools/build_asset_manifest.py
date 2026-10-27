"""Regenerate LOCKD's image inventory from the JPEGs in the site root."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, UnidentifiedImageError


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "asset-manifest.json"

# Descriptions are limited to what is visible in the supplied image. They do not
# establish ownership, rental availability, precise model, destination, or terms.
NOTES = {
    "WhatsApp Image 2026-10-27 at 23.34.40.jpeg": ("Television, PlayStation console and controllers in a living room", "play", "gaming category introduction", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.41 (1).jpeg": ("Wildlife crossing a river with safari vehicles in the distance", "explore", "experience editorial / possible listing only after review", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.41.jpeg": ("PlayStation console and controller beside a television", "play", "gaming category introduction", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.45.jpeg": ("Giraffe in grassland with a safari vehicle", "explore", "experience editorial / possible listing only after review", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.46.jpeg": ("Hot-air balloons and safari vehicles before sunrise", "explore", "experience editorial / possible listing only after review", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.49.jpeg": ("Wildlife herd across open grassland with a safari vehicle", "explore", "experience editorial / possible listing only after review", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.51.jpeg": ("White coastal buildings framed by rock and bright blue water", "explore", "destination imagery; location unverified", "medium"),
    "WhatsApp Image 2026-10-27 at 23.34.52.jpeg": ("Turquoise bay beneath green coastal cliffs with small boats", "explore", "experience category card", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.53 (1).jpeg": ("Grey performance SUV displayed in a showroom", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.53.jpeg": ("Snow-capped mountain above savannah wildlife and a safari vehicle", "explore", "destination imagery; location unverified", "medium"),
    "WhatsApp Image 2026-10-27 at 23.34.56.jpeg": ("Dark burgundy luxury SUV outside a modern building", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.58.jpeg": ("Compact apartment interior with bed, sofa and kitchenette", "stay", "property imagery; listing details unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.34.59.jpeg": ("Compact modern loft with mezzanine bedroom and living area", "stay", "stay category card", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.00.jpeg": ("Burgundy smartphone shown in one hand", "tech", "technology category card; product model unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.03.jpeg": ("Burgundy smartphone inside a retail box", "tech", "technology imagery; product model and authenticity unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.32.jpeg": ("Two burgundy smartphones shown from the back", "tech", "technology imagery; models unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.41.jpeg": ("Burgundy smartphone and matching retail box", "tech", "technology imagery; product model and authenticity unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.55.jpeg": ("Silver luxury sedan in a dark studio", "drive", "drive category card; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.58.jpeg": ("Two-tone luxury sedan inside a showroom", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.59 (1).jpeg": ("Exact copy of the compact apartment interior in 23.34.58", "stay", "duplicate source; retain original for audit", "high"),
    "WhatsApp Image 2026-10-27 at 23.35.59.jpeg": ("Bedroom and lounge in a warmly lit apartment", "stay", "property imagery; listing details unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.00.jpeg": ("Private courtyard pool surrounded by dense greenery", "stay", "stay editorial image", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.02.jpeg": ("Acacia tree silhouetted against a warm savannah sunset", "explore", "landscape editorial; destination unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.03.jpeg": ("Elephants beneath an acacia tree at sunset", "explore", "package editorial image; destination unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.04.jpeg": ("Contemporary dark two-storey home with a lit garden", "stay", "property imagery; property and listing details unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.05.jpeg": ("Contemporary dark home with landscaped garden", "stay", "property imagery; property and listing details unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.06.jpeg": ("Pale luxury SUV beneath palm trees on a clear day", "drive", "homepage hero; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.07.jpeg": ("Close view of a red performance car in the rain", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.10.jpeg": ("Black and turquoise customized luxury SUV in a studio", "drive", "vehicle imagery; custom styling and model unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.13.jpeg": ("Black customized luxury SUV shown from front and rear", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.14.jpeg": ("Angular silver customized SUV on an urban street", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.17.jpeg": ("Dark grey electric sedan displayed at an indoor event", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.18.jpeg": ("Black customized SUV in a dark studio", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.20.jpeg": ("Exact copy of the black customized SUV in 23.36.18", "drive", "duplicate source; retain original for audit", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.21 (1).jpeg": ("Red performance coupe seen from the front through foliage", "drive", "vehicle imagery; exact model and availability unverified", "high"),
    "WhatsApp Image 2026-10-27 at 23.36.21.jpeg": ("Red performance coupe seen from the rear in a wooded setting", "drive", "vehicle imagery; exact model and availability unverified", "high"),
}

USED = {
    "WhatsApp Image 2026-10-27 at 23.36.06.jpeg": "Homepage hero",
    "WhatsApp Image 2026-10-27 at 23.34.59.jpeg": "Stay category card",
    "WhatsApp Image 2026-10-27 at 23.35.55.jpeg": "Drive category card",
    "WhatsApp Image 2026-10-27 at 23.34.41.jpeg": "Play category card",
    "WhatsApp Image 2026-10-27 at 23.35.00.jpeg": "Technology category card",
    "WhatsApp Image 2026-10-27 at 23.34.52.jpeg": "Explore category card",
    "WhatsApp Image 2026-10-27 at 23.36.03.jpeg": "Combined rental editorial section",
    "WhatsApp Image 2026-10-27 at 23.36.00.jpeg": "Closing editorial section",
}


def main() -> None:
    paths = sorted(ROOT.glob("WhatsApp Image 2026-10-27*.jpeg"), key=lambda path: path.name)
    digest_groups: dict[str, list[Path]] = defaultdict(list)
    records = []

    for path in paths:
        try:
            with Image.open(path) as image:
                image.verify()
            with Image.open(path) as image:
                width, height = image.size
                image_format = image.format or "JPEG"
        except (OSError, UnidentifiedImageError) as error:
            records.append({"original_filename": path.name, "status": "unreadable", "error": str(error)})
            continue

        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        digest_groups[digest].append(path)
        subject, category, role, confidence = NOTES.get(
            path.name,
            ("Unclassified supplied image", "unclassified", "requires review", "low"),
        )
        records.append({
            "asset_id": "lockd-" + path.stem.replace("WhatsApp Image 2026-10-27 at ", "").replace(".", "").replace(" ", "-").replace("(", "").replace(")", ""),
            "original_filename": path.name,
            "source_path": "./" + path.name,
            "format": image_format,
            "dimensions_px": {"width": width, "height": height},
            "aspect_ratio": round(width / height, 4),
            "file_size_bytes": path.stat().st_size,
            "sha256": digest,
            "visible_subject": subject,
            "suggested_category": category,
            "classification_confidence": confidence,
            "visual_role": role,
            "quality_assessment": "Clear supplied image; judge crop at its final placement. Source alone does not verify a rental listing.",
            "duplicate_status": "pending hash grouping",
            "used_on_site": path.name in USED,
            "site_placement": USED.get(path.name),
            "human_review_required_before_listing": True,
        })

    by_name = {record.get("original_filename"): record for record in records}
    duplicate_groups = []
    for number, (digest, group) in enumerate(digest_groups.items(), start=1):
        if len(group) < 2:
            by_name[group[0].name]["duplicate_status"] = "unique file"
            continue
        group_id = f"exact-{number:02d}"
        primary = group[0]
        duplicate_groups.append({"group_id": group_id, "sha256": digest, "files": [item.name for item in group], "primary_file": primary.name})
        by_name[primary.name]["duplicate_status"] = f"primary file in {group_id}"
        for duplicate in group[1:]:
            by_name[duplicate.name]["duplicate_status"] = f"exact duplicate of {primary.name} ({group_id})"

    manifest = {
        "project": "LOCKD",
        "generated_by": "tools/build_asset_manifest.py",
        "source_directory": ".",
        "assets_discovered": len(paths),
        "duplicate_groups": duplicate_groups,
        "assets": records,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.name}: {len(records)} assets, {len(duplicate_groups)} exact duplicate groups.")


if __name__ == "__main__":
    main()
