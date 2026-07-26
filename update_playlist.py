#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures
import json
import re
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass, replace
from pathlib import Path

BASE = Path(__file__).resolve().parent
CFG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
UA = "Mozilla/5.0 IPTV-Curated/2.0"


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
    channels: list[Channel] = []
    pending = ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("#EXTINF:"):
            pending = line
        elif pending and line and not line.startswith("#"):
            channels.append(
                Channel(
                    extinf=pending,
                    url=line,
                    name=pending.rsplit(",", 1)[-1].strip(),
                    country=get_attr(pending, "tvg-country").upper(),
                    group=get_attr(pending, "group-title"),
                )
            )
            pending = ""
    return channels


def download_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def has_any(text: str, terms: list[str]) -> bool:
    folded = text.casefold()
    return any(term.casefold() in folded for term in terms)


def excluded(channel: Channel) -> bool:
    text = f"{channel.name} {channel.group} {channel.extinf}"
    return has_any(text, CFG["exclude_keywords"])


def live(channel: Channel) -> tuple[Channel, bool]:
    if not channel.url.lower().startswith(("http://", "https://")):
        return channel, False

    request = urllib.request.Request(
        channel.url,
        headers={
            "User-Agent": UA,
            "Accept": "*/*",
            "Range": "bytes=0-4095",
            "Connection": "close",
        },
    )
    try:
        with urllib.request.urlopen(
            request, timeout=CFG["timeout_seconds"]
        ) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "").lower()
            sample = response.read(4096)
            return channel, (
                status < 400
                and (
                    bool(sample)
                    or "mpegurl" in content_type
                    or content_type.startswith("video/")
                )
            )
    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        socket.timeout,
        TimeoutError,
        ConnectionError,
    ):
        return channel, False
    except Exception:
        return channel, False


def priority(channel: Channel, include: list[str]) -> tuple[int, str]:
    name = channel.name.casefold()
    for index, keyword in enumerate(include):
        if keyword.casefold() in name:
            return index, name
    return len(include) + 1, name


def change_group(channel: Channel, group_title: str) -> Channel:
    extinf = channel.extinf
    if re.search(r'group-title="[^"]*"', extinf):
        extinf = re.sub(
            r'group-title="[^"]*"',
            f'group-title="{group_title}"',
            extinf,
            count=1,
        )
    else:
        extinf = extinf.replace(",", f' group-title="{group_title}",', 1)
    return replace(channel, extinf=extinf, group=group_title)


def select_candidates(
    playlist_key: str,
    definition: dict,
    source_channels: dict[str, list[Channel]],
    all_channels: list[Channel],
) -> list[Channel]:
    include = definition.get("include", [])
    source_keys = definition.get("source_keys", [])

    if playlist_key == "favorites":
        pool = all_channels
        selected = [
            channel
            for channel in pool
            if has_any(channel.name, include) and not excluded(channel)
        ]
    else:
        pool: list[Channel] = []
        for source_key in source_keys:
            pool.extend(source_channels.get(source_key, []))

        if include:
            selected = [
                channel
                for channel in pool
                if has_any(channel.name, include) and not excluded(channel)
            ]
        else:
            selected = [channel for channel in pool if not excluded(channel)]

    unique: dict[str, Channel] = {}
    for channel in selected:
        unique.setdefault(channel.url, channel)

    return sorted(unique.values(), key=lambda item: priority(item, include))


def test_channels(candidates: list[Channel]) -> list[Channel]:
    active: list[Channel] = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=CFG["workers"]
    ) as pool:
        futures = [pool.submit(live, channel) for channel in candidates]
        for future in concurrent.futures.as_completed(futures):
            channel, ok = future.result()
            print(f"{'ACTIVE' if ok else 'FAILED'} | {channel.name}")
            if ok:
                active.append(channel)
    return active


def write_playlist(path: Path, channels: list[Channel]) -> None:
    lines = [
        '#EXTM3U url-tvg="https://iptv-org.github.io/epg/guides/id.xml"',
        "# Generated automatically by GitHub Actions.",
        f"# Active channels at last check: {len(channels)}",
    ]
    for channel in channels:
        lines.extend([channel.extinf, channel.url])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_channels: dict[str, list[Channel]] = {}
    all_channels: list[Channel] = []

    for key, url in CFG["sources"].items():
        print(f"Downloading {key}: {url}")
        try:
            channels = parse_m3u(download_text(url))
            source_channels[key] = channels
            all_channels.extend(channels)
            print(f"Loaded {len(channels)} entries")
        except Exception as exc:
            print(f"WARNING: failed to download {key}: {exc}")
            source_channels[key] = []

    generated: dict[str, list[Channel]] = {}

    for key, definition in CFG["playlists"].items():
        print(f"\nBuilding {key}")
        candidates = select_candidates(
            key, definition, source_channels, all_channels
        )
        print(f"Testing {len(candidates)} candidates")

        active = test_channels(candidates)
        active.sort(
            key=lambda item: priority(item, definition.get("include", []))
        )
        active = active[: definition["max_channels"]]
        active = [
            change_group(item, definition["group_title"])
            for item in active
        ]
        generated[key] = active
        write_playlist(BASE / definition["output"], active)
        print(f"Wrote {len(active)} channels to {definition['output']}")

    combined: list[Channel] = []
    seen_urls: set[str] = set()
    order = [
        "favorites", "indonesia", "news", "business",
        "documentary", "kids", "music"
    ]
    for key in order:
        for channel in generated.get(key, []):
            if channel.url not in seen_urls:
                combined.append(channel)
                seen_urls.add(channel.url)

    write_playlist(BASE / "playlist.m3u", combined)
    print(f"\nWrote {len(combined)} channels to playlist.m3u")


if __name__ == "__main__":
    main()
