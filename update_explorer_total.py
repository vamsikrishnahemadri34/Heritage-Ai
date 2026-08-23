from pathlib import Path

path = Path(r".\apps\web\components\explorer\ExplorerPage.tsx")
text = path.read_text(encoding="utf-8")

text = text.replace(
    '  const [totalPages, setTotalPages] = useState(0);',
    '  const [totalPages, setTotalPages] = useState(0);\n  const [totalSites, setTotalSites] = useState(0);'
)

text = text.replace(
    '  const dataTotalLabel =\n    sites.length === 1\n      ? "1 heritage site found"\n      : `${sites.length} heritage sites found`;',
    '  const dataTotalLabel =\n    totalSites === 1\n      ? "1 heritage site found"\n      : `${totalSites} heritage sites found`;'
)

text = text.replace(
    '      setTotalPages(data.total_pages);',
    '      setTotalPages(data.total_pages);\n          setTotalSites(data.total);'
)

path.write_text(text, encoding="utf-8")

print("ExplorerPage.tsx updated successfully.")
