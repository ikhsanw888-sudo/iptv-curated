# IPTV Curated Playlist

Playlist IPTV ringkas untuk STB, dibangun otomatis dari playlist publik iptv-org dan disaring berdasarkan negara, kategori, serta respons URL.

## URL playlist untuk STB

```text
https://raw.githubusercontent.com/ikhsanw888-sudo/iptv-curated/main/playlist.m3u
```

## Menjalankan pembaruan

Buka **Actions → Update IPTV playlist → Run workflow**.

Workflow juga dijadwalkan berjalan setiap hari sekitar pukul 03.15 WIB.

## Mengubah pilihan channel

Edit `config.json`, kemudian jalankan workflow kembali.

> Stream yang merespons dari GitHub Actions belum tentu dapat dimainkan dari semua jaringan atau perangkat karena pembatasan wilayah, ISP, codec, dan perubahan URL dari penyedia.
