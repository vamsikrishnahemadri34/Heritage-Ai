from pathlib import Path

files = {
    Path(r".\apps\web\components\explorer\ExplorerPage.tsx"): {
        "Ã—": "×",
        "â€¦": "…",
    },
    Path(r".\apps\web\components\explorer\HeritageDetailHero.tsx"): {
        "ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â·": "·",
    },
}

for path, replacements in files.items():
    text = path.read_text(encoding="utf-8")

    for old, new in replacements.items():
        if old not in text:
            print(f"WARNING: '{old}' not found in {path}")
            continue

        text = text.replace(old, new)

    path.write_text(text, encoding="utf-8")
    print(f"UPDATED: {path}")

print("ENCODING FIX COMPLETE")
