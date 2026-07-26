#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import json
import re
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

BASE = Path(__file__).resolve().parent
CFG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
UA = "Mozilla/5.0 IPTV-Curated-Checker/1.0"

@dataclass(frozen=True)
class Channel:
    extinf: str
    url: str
    name: str
    country: str
    group: str

def get_attr(extinf: str, key: str) -> str:
    match = re.search(rf'{re.escape(key)}="([^"]*)"', extinf, flags=re.I)
    return match.group(1).strip() if match else ""

def parse_m3u(text: str) -> list[Channel]:
    result: list[Channel] = []
    pending = ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF:"):
            pending = line
        elif pending and line and not line.startswith("#"):
            result.append(Channel(
                extinf=pending,
                url=line,
                name=pending.rsplit(",", 1)[-1].strip(),
                country=get_attr(pending, "tvg-country").upper(),
                group=get_attr(pending, "group-title"),
            ))
            pending = ""
    return result

def download_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")

def contains(value: str, terms: list[str]) -> bool:
    folded = value.casefold()
    return any(term.casefold() in folded for term in terms)

def allowed(channel: Channel) -> bool:
    text = f"{channel.name} {channel.group} {channel.extinf}"
    if contains(text, CFG["exclude_keywords"]):
        return False
    if channel.country == "ID" or "indonesia" in text.casefold():
        return True
    return contains(channel.name, CFG["international_allowlist"])

def priority(channel: Channel) -> tuple[int, str]:
    folded = channel.name.casefold()
    for index, keyword in enumerate(CFG["preferred_channels"]):
        if keyword.casefold() in folded:
            return index, folded
    return len(CFG["preferred_channels"]) + 1, folded

def check_stream(channel: Channel) -> tuple[Channel, bool]:
    if not channel.url.lower().startswith(("http://", "https://")):
        return channel, False
    request = urllib.request.Request(channel.url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Range": "bytes=0-4095",
        "Connection": "close",
    })
    try:
        with urllib.request.urlopen(request, timeout=CFG["timeout_seconds"]) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "").lower()
            sample = response.read(4096)
            ok = status < 400 and (bool(sample) or "mpegurl" in content_type or content_type.startswith("video/"))
            return channel, ok
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError):
        return channel, False
    except Exception:
        return channel, False

def normalise_extinf(channel: Channel) -> str:
    extinf = channel.extinf
    if 'group-title="' not in extinf:
        group = "Indonesia" if channel.country == "ID" or "indonesia" in extinf.casefold() else "International"
        extinf = extinf.replace(",", f' group-title="{group}",', 1)
    return extinf

def main() -> None:
    gathered: list[Channel] = []
    for source in CFG["sources"]:
        print(f"Downloading: {source}")
        try:
            gathered.extend(parse_m3u(download_text(source)))
        except Exception as exc:
            print(f"WARNING: {source}: {exc}")

    unique: dict[str, Channel] = {}
    for channel in gathered:
        if allowed(channel):
            unique.setdefault(channel.url, channel)

    candidates = sorted(unique.values(), key=priority)
    print(f"Testing {len(candidates)} candidate streams...")
    active: list[Channel] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=CFG["workers"]) as pool:
        futures = [pool.submit(check_stream, item) for item in candidates]
        for future in concurrent.futures.as_completed(futures):
            channel, ok = future.result()
            print(f"{'ACTIVE' if ok else 'FAILED'}: {channel.name}")
            if ok:
                active.append(channel)

    active.sort(key=priority)
    active = active[:CFG["max_channels"]]
    lines = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id.xml"',
        "# Generated automatically by GitHub Actions.",
        f"# Active channels at last check: {len(active)}",
    ]
    for channel in active:
        lines.extend([normalise_extinf(channel), channel.url])

    (BASE / "playlist.m3u").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Saved {len(active)} channels to playlist.m3u")

if __name__ == "__main__":
    main()
