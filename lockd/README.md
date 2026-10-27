# LOCKD site

An editorial, responsive static front end for LOCKD, built around the supplied image library.

## Preview

Open `index.html` directly, or run a local server from this folder:

```powershell
python -m http.server 8765
```

Then open `http://127.0.0.1:8765/`.

## Current behavior

- Category cards add a rental line to a local bundle draft.
- The idea finder uses local keyword matching to suggest a category; it is not an AI service or live inventory search.
- Bundle lines support item descriptions, quantities and accessories; the bundle also captures dates, delivery or collection, and location.
- The price summary counts items, units and the selected period, while clearly showing that verified rates are not connected.
- Bundle drafts are stored in the browser on this device and can be copied. They are not sent to LOCKD.
- No item prices, listings, availability, booking, payment, contact destination or admin access are configured.
- The supplied photos are used as category and editorial inspiration, not as proof of available inventory.
- The separate `owners.html` page describes the intended owner journey. Secure owner registration, listing submission, verification, booking management and payouts are not connected; its support email is an enquiry path, not an online application.

See [`ASSET_AUDIT.md`](./ASSET_AUDIT.md) and [`asset-manifest.json`](./asset-manifest.json) for image curation and duplicate findings. Regenerating the manifest requires Python and Pillow (`python tools/build_asset_manifest.py`).
