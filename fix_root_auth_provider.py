from pathlib import Path

path = Path(r".\apps\web\app\layout.tsx")
text = path.read_text(encoding="utf-8")

if 'import { AuthProvider } from "@/providers/AuthProvider";' not in text:
    text = text.replace(
        'import Navbar from "@/components/layout/Navbar";',
        'import Navbar from "@/components/layout/Navbar";\nimport { AuthProvider } from "@/providers/AuthProvider";',
        1,
    )

old = '''      React.createElement(Navbar),
      children,
'''

new = '''      React.createElement(
        AuthProvider,
        null,
        React.createElement(Navbar),
        children,
      ),
'''

if old not in text:
    raise RuntimeError(
        "Expected Navbar/children block was not found. File was NOT modified."
    )

text = text.replace(old, new, 1)

path.write_text(text, encoding="utf-8")

print("AUTH PROVIDER ADDED TO ROOT LAYOUT")
