import csv
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

INPUT_FILE = Path("channels.csv")
REPORT_DIR = Path("reports")
CSV_REPORT = REPORT_DIR / "stream-test.csv"
MD_REPORT = REPORT_DIR / "stream-test.md"

TIMEOUT_SECONDS = 12
MAX_WORKERS = 8
MAX_MANIFEST_BYTES = 512_000
MAX_SEGMENT_BYTES = 64_000

HEADERS = {
    "User-Agent": "VLC/3.0.20 LibVLC/3.0.20",
    "Accept": (
        "application/vnd.apple.mpegurl,"
        "application/x-mpegURL,"
        "video/mp2t,"
        "*/*"
    ),
}


def clean(value: str | None) -> str:
    return str(value or "").strip()


def fetch(url: str, max_bytes: int) -> dict:
    request = Request(url, headers=HEADERS)
    started = time.monotonic()

    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            data = response.read(max_bytes)
            elapsed_ms = round((time.monotonic() - started) * 1000)
            return {
                "ok": True,
                "code": getattr(response, "status", 200),
                "content_type": response.headers.get("Content-Type", ""),
                "effective_url": response.geturl(),
                "data": data,
                "elapsed_ms": elapsed_ms,
                "error": "",
            }

    except HTTPError as exc:
        elapsed_ms = round((time.monotonic() - started) * 1000)
        return {
            "ok": False,
            "code": exc.code,
            "content_type": exc.headers.get("Content-Type", "") if exc.headers else "",
            "effective_url": exc.geturl() or url,
            "data": b"",
            "elapsed_ms": elapsed_ms,
            "error": f"HTTP {exc.code}: {exc.reason}",
        }

    except (URLError, TimeoutError, socket.timeout) as exc:
        elapsed_ms = round((time.monotonic() - started) * 1000)
        reason = getattr(exc, "reason", exc)
        return {
            "ok": False,
            "code": 0,
            "content_type": "",
            "effective_url": url,
            "data": b"",
            "elapsed_ms": elapsed_ms,
            "error": str(reason),
        }

    except Exception as exc:
        elapsed_ms = round((time.monotonic() - started) * 1000)
        return {
            "ok": False,
            "code": 0,
            "content_type": "",
            "effective_url": url,
            "data": b"",
            "elapsed_ms": elapsed_ms,
            "error": f"{type(exc).__name__}: {exc}",
        }


def decode_manifest(data: bytes) -> str:
    return data.decode("utf-8-sig", errors="replace")


def is_hls_manifest(text: str) -> bool:
    return text.lstrip().startswith("#EXTM3U")


def first_uri(text: str) -> str | None:
    for line in text.splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            return value
    return None


def is_master_manifest(text: str) -> bool:
    return "#EXT-X-STREAM-INF" in text


def classify_http_failure(code: int, error: str) -> tuple[str, str]:
    if code in {401, 403, 451}:
        return "REVIEW", f"Akses dibatasi atau kemungkinan geo-block: {error}"
    if code == 404:
        return "FAIL", "URL tidak ditemukan (HTTP 404)"
    if code >= 500:
        return "REVIEW", f"Server sedang bermasalah: {error}"
    return "FAIL", error or f"HTTP {code}"


def test_channel(row: dict) -> dict:
    name = clean(row.get("name"))
    url = clean(row.get("url"))
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    result = {
        "name": name,
        "category": clean(row.get("category")),
        "tier": clean(row.get("tier")),
        "url": url,
        "result": "FAIL",
        "http_code": 0,
        "response_ms": 0,
        "detail": "",
        "effective_url": url,
        "checked_at_utc": checked_at,
    }

    manifest_response = fetch(url, MAX_MANIFEST_BYTES)
    result["http_code"] = manifest_response["code"]
    result["response_ms"] = manifest_response["elapsed_ms"]
    result["effective_url"] = manifest_response["effective_url"]

    if not manifest_response["ok"]:
        status, detail = classify_http_failure(
            manifest_response["code"],
            manifest_response["error"],
        )
        result["result"] = status
        result["detail"] = detail
        return result

    manifest_text = decode_manifest(manifest_response["data"])

    if not is_hls_manifest(manifest_text):
        result["detail"] = (
            "Respons dapat diakses, tetapi bukan manifest HLS #EXTM3U "
            f"(Content-Type: {manifest_response['content_type'] or 'tidak diketahui'})"
        )
        return result

    media_manifest_text = manifest_text
    media_manifest_url = manifest_response["effective_url"]

    if is_master_manifest(manifest_text):
        variant_uri = first_uri(manifest_text)
        if not variant_uri:
            result["result"] = "REVIEW"
            result["detail"] = "Master playlist terbuka, tetapi tidak memiliki variant URI"
            return result

        variant_url = urljoin(manifest_response["effective_url"], variant_uri)
        variant_response = fetch(variant_url, MAX_MANIFEST_BYTES)

        if not variant_response["ok"]:
            status, detail = classify_http_failure(
                variant_response["code"],
                variant_response["error"],
            )
            result["result"] = status
            result["detail"] = f"Master playlist terbuka, tetapi variant gagal: {detail}"
            return result

        media_manifest_text = decode_manifest(variant_response["data"])
        media_manifest_url = variant_response["effective_url"]

        if not is_hls_manifest(media_manifest_text):
            result["detail"] = "Variant yang dirujuk bukan manifest HLS"
            return result

    segment_uri = first_uri(media_manifest_text)

    if not segment_uri:
        result["result"] = "REVIEW"
        result["detail"] = "Manifest HLS terbuka, tetapi segmen media belum ditemukan"
        return result

    segment_url = urljoin(media_manifest_url, segment_uri)
    segment_response = fetch(segment_url, MAX_SEGMENT_BYTES)

    if not segment_response["ok"]:
        status, detail = classify_http_failure(
            segment_response["code"],
            segment_response["error"],
        )
        result["result"] = status
        result["detail"] = f"Manifest terbuka, tetapi segmen media gagal: {detail}"
        return result

    if not segment_response["data"]:
        result["result"] = "REVIEW"
        result["detail"] = "Segmen media merespons tetapi kosong"
        return result

    result["result"] = "PASS"
    result["detail"] = "Manifest dan segmen media dapat diakses"
    return result


def read_channels() -> list[dict]:
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_reports(results: list[dict]) -> None:
    REPORT_DIR.mkdir(exist_ok=True)

    fields = [
        "name",
        "category",
        "tier",
        "result",
        "http_code",
        "response_ms",
        "detail",
        "url",
        "effective_url",
        "checked_at_utc",
    ]

    with CSV_REPORT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    counts = {
        status: sum(item["result"] == status for item in results)
        for status in ("PASS", "REVIEW", "FAIL")
    }

    lines = [
        "# IPTV Stream Test Report",
        "",
        f"- Total: **{len(results)}**",
        f"- PASS: **{counts['PASS']}**",
        f"- REVIEW: **{counts['REVIEW']}**",
        f"- FAIL: **{counts['FAIL']}**",
        "",
        "> Pengujian dilakukan dari GitHub Actions, bukan dari jaringan STB di Indonesia. "
        "Hasil REVIEW dapat disebabkan geo-blocking, kebutuhan header khusus, atau pembatasan CDN.",
        "",
        "| Result | Channel | Category | HTTP | Response | Detail |",
        "|---|---|---|---:|---:|---|",
    ]

    for item in results:
        detail = item["detail"].replace("|", "/")
        lines.append(
            f"| {item['result']} | {item['name']} | {item['category']} | "
            f"{item['http_code']} | {item['response_ms']} ms | {detail} |"
        )

    MD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    channels = read_channels()
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_map = {
            executor.submit(test_channel, row): row
            for row in channels
        }

        for completed, future in enumerate(as_completed(future_map), start=1):
            row = future_map[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {
                    "name": clean(row.get("name")),
                    "category": clean(row.get("category")),
                    "tier": clean(row.get("tier")),
                    "url": clean(row.get("url")),
                    "result": "FAIL",
                    "http_code": 0,
                    "response_ms": 0,
                    "detail": f"Tester error: {type(exc).__name__}: {exc}",
                    "effective_url": clean(row.get("url")),
                    "checked_at_utc": datetime.now(timezone.utc).isoformat(
                        timespec="seconds"
                    ),
                }

            results.append(result)
            print(
                f"[{completed:02d}/{len(channels)}] "
                f"{result['result']}: {result['name']} — {result['detail']}"
            )

    priority = {
        clean(row.get("name")): int(clean(row.get("priority")) or 999)
        for row in channels
    }
    results.sort(key=lambda item: priority.get(item["name"], 999))

    write_reports(results)

    pass_count = sum(item["result"] == "PASS" for item in results)
    review_count = sum(item["result"] == "REVIEW" for item in results)
    fail_count = sum(item["result"] == "FAIL" for item in results)

    print()
    print(f"PASS   : {pass_count}")
    print(f"REVIEW : {review_count}")
    print(f"FAIL   : {fail_count}")
    print(f"Report : {MD_REPORT}")


if __name__ == "__main__":
    main()
