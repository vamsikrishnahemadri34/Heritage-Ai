from pathlib import Path

path = Path(r".\apps\web\components\explorer\ExplorerPage.tsx")
text = path.read_text(encoding="utf-8")

old = """const [currentPage, setCurrentPage] = useState(1);
const [totalPages, setTotalPages] = useState(0);"""

new = """  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [totalSites, setTotalSites] = useState(0);"""

if old not in text:
    raise RuntimeError("Expected state block was not found. File was NOT modified.")

text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")

print("FIX APPLIED: totalSites state added.")
