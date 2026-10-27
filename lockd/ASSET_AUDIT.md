# LOCKD image audit

Inventory generated from the JPEG files in this folder. The same records are available in [`asset-manifest.json`](./asset-manifest.json); regenerate it with `python tools/build_asset_manifest.py`.

## Findings

- 36 JPEG files are present and readable.
- SHA-256 grouping found 34 unique image files and 2 exact duplicate pairs.
- Duplicate pair 1: `WhatsApp Image 2026-10-27 at 23.34.58.jpeg` and `WhatsApp Image 2026-10-27 at 23.35.59 (1).jpeg`.
- Duplicate pair 2: `WhatsApp Image 2026-10-27 at 23.36.18.jpeg` and `WhatsApp Image 2026-10-27 at 23.36.20.jpeg`.
- Source dimensions range from 564–736 px wide and 491–1,318 px tall. Files are 33–221 KB. Originals remain in place; the page uses them directly.
- No corrupt or inaccessible image files were found in the supplied site folder.
- Image subjects were classified visually. Destination, model, property, ownership, availability, authenticity and rental details remain unverified unless confirmed from a separate source.

## Category curation

Counts below include the two duplicate file copies; the distinct-image count is in parentheses.

| Suggested category | Image files | Distinct images | Assignment |
| --- | ---: | ---: | --- |
| Stay | 7 | 6 | Apartment interiors, courtyard pool and modern homes |
| Drive | 14 | 13 | Luxury vehicles and performance-car imagery |
| Play | 2 | 2 | Console and gaming setup imagery |
| Technology | 4 | 4 | Burgundy smartphones; exact models unverified |
| Explore | 9 | 9 | Wildlife, savannah, coastal and landscape imagery |

## Used on the website

- Homepage hero: `WhatsApp Image 2026-10-27 at 23.36.06.jpeg` — pale SUV photo.
- Stay category: `WhatsApp Image 2026-10-27 at 23.34.59.jpeg` — compact loft interior.
- Drive category: `WhatsApp Image 2026-10-27 at 23.35.55.jpeg` — silver sedan in a studio.
- Play category: `WhatsApp Image 2026-10-27 at 23.34.41.jpeg` — console and controller by a television.
- Technology category: `WhatsApp Image 2026-10-27 at 23.35.00.jpeg` — burgundy smartphone.
- Explore category: `WhatsApp Image 2026-10-27 at 23.34.52.jpeg` — turquoise bay and cliffs.
- Combined-rental editorial section: `WhatsApp Image 2026-10-27 at 23.36.03.jpeg` — elephants at sunset.
- Closing editorial section: `WhatsApp Image 2026-10-27 at 23.36.00.jpeg` — garden courtyard pool.

These photos introduce categories and visual direction. They are not presented as available listings. The other 28 file entries remain in the source folder and are not placed on the initial page; that includes the duplicate copies.

## Review before publishing inventory

The imagery alone does not establish that an item, stay or experience is owned, available, authentic, located where it appears to be, or ready to rent. Match photos to approved inventory and confirm exact product/property details, location, prices, dates, included items and terms before publishing. The supplied images are at most 736 px wide, so avoid relying on large, high-density full-screen image placements without higher-resolution originals.

No backend, inventory feed, contact destination, payment provider or AI image service was present in the supplied folder. The bundle builder therefore creates a local draft only; it does not submit, check availability or reserve an item.
