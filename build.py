import csv
from pathlib import Path
from urllib.parse import urlparse


INPUT_FILE = Path("channels.csv")
OUTPUT_FILE = Path("tv.m3u")


def clean(value: str | None) -> str:
    """Membersihkan spasi dan karakter yang dapat merusak format M3U."""
    if value is None:
        return ""

    return (
        str(value)
        .strip()
        .replace("\r", " ")
        .replace("\n", " ")
        .replace('"', "'")
    )


def is_valid_url(url: str) -> bool:
    """Memastikan URL menggunakan HTTP atau HTTPS."""
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def read_channels() -> list[dict]:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"{INPUT_FILE} tidak ditemukan.")

    channels = []

    with INPUT_FILE.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {
            "name",
            "category",
            "url",
            "priority",
            "status",
        }

        available_columns = set(reader.fieldnames or [])
        missing_columns = required_columns - available_columns

        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"Kolom CSV belum lengkap: {missing}")

        for row_number, row in enumerate(reader, start=2):
            name = clean(row.get("name"))
            category = clean(row.get("category"))
            url = clean(row.get("url"))
            status = clean(row.get("status")).lower()

            # Hanya channel berstatus active yang dimasukkan.
            if status != "active":
                continue

            if not name or not url:
                print(
                    f"Baris {row_number} dilewati: "
                    "nama atau URL kosong."
                )
                continue

            if not is_valid_url(url):
                print(
                    f"Baris {row_number} dilewati: "
                    f"URL tidak valid untuk {name}."
                )
                continue

            try:
                priority = int(clean(row.get("priority")) or 999)
            except ValueError:
                priority = 999

            channels.append(
                {
                    "name": name,
                    "category": category or "Other",
                    "url": url,
                    "priority": priority,
                }
            )

    channels.sort(
        key=lambda channel: (
            channel["priority"],
            channel["category"].lower(),
            channel["name"].lower(),
        )
    )

    return channels


def build_playlist(channels: list[dict]) -> None:
    lines = ["#EXTM3U"]

    for channel in channels:
        # Format dibuat sederhana agar kompatibel dengan STB lama.
        lines.append(
            '#EXTINF:-1 '
            f'group-title="{channel["category"]}",'
            f'{channel["name"]}'
        )
        lines.append(channel["url"])

    OUTPUT_FILE.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    channels = read_channels()
    build_playlist(channels)

    print(f"Berhasil membuat: {OUTPUT_FILE}")
    print(f"Jumlah channel aktif: {len(channels)}")


if __name__ == "__main__":
    main()
