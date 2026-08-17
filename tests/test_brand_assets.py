from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "src" / "code2plain" / "web" / "static" / "brand"
INDEX = ROOT / "src" / "code2plain" / "web" / "index.html"


def test_brand_assets_exist():
    expected = {
        "code2plain-monogram.png",
        "code2plain-horizontal.png",
        "code2plain-wordmark.png",
        "code2plain-app-icon.png",
    }

    actual = {
        path.name
        for path in BRAND.iterdir()
        if path.is_file()
    }

    assert expected.issubset(actual)


def test_index_uses_code2plain_brand():
    text = INDEX.read_text(encoding="utf-8")

    assert "code2plain-monogram.png" in text
    assert "code2plain-wordmark.png" in text
    assert "code2plain-app-icon.png" in text
    assert "Code2Plain v1.1.2" in text
