# IPTV Stream Test Report

- Total: **52**
- PASS: **46**
- REVIEW: **0**
- FAIL: **6**

> Pengujian dilakukan dari GitHub Actions, bukan dari jaringan STB di Indonesia. Hasil REVIEW dapat disebabkan geo-blocking, kebutuhan header khusus, atau pembatasan CDN.

| Result | Channel | Category | HTTP | Response | Detail |
|---|---|---|---:|---:|---|
| PASS | Metro TV | Indonesia | 200 | 1842 ms | Manifest dan segmen media dapat diakses |
| PASS | TVRI Nasional | Indonesia | 200 | 931 ms | Manifest dan segmen media dapat diakses |
| FAIL | CNBC Indonesia | Indonesia | 0 | 792 ms | RemoteDisconnected: Remote end closed connection without response |
| FAIL | BeritaSatu | Indonesia | 0 | 264 ms | [Errno -2] Name or service not known |
| PASS | UEFA Champions League | Indonesia | 200 | 963 ms | Manifest dan segmen media dapat diakses |
| PASS | TVRI World | Indonesia | 200 | 958 ms | Manifest dan segmen media dapat diakses |
| PASS | Rajawali TV (RTV) | Indonesia | 200 | 526 ms | Manifest dan segmen media dapat diakses |
| PASS | Garuda TV | Indonesia | 200 | 1385 ms | Manifest dan segmen media dapat diakses |
| PASS | FIFA+ | Football & Sports | 200 | 386 ms | Manifest dan segmen media dapat diakses |
| PASS | CBS Sports Golazo Network | Football & Sports | 200 | 3269 ms | Manifest dan segmen media dapat diakses |
| PASS | SportsGrid | Football & Sports | 200 | 333 ms | Manifest dan segmen media dapat diakses |
| PASS | beIN SPORTS Xtra | Football & Sports | 200 | 273 ms | Manifest dan segmen media dapat diakses |
| PASS | Red Bull TV | Football & Sports | 200 | 228 ms | Manifest dan segmen media dapat diakses |
| PASS | CBS Sports HQ | Football & Sports | 200 | 3117 ms | Manifest dan segmen media dapat diakses |
| PASS | FUEL TV | Football & Sports | 200 | 318 ms | Manifest dan segmen media dapat diakses |
| PASS | Fight Network | Football & Sports | 200 | 278 ms | Manifest dan segmen media dapat diakses |
| PASS | World Poker Tour | Football & Sports | 200 | 404 ms | Manifest dan segmen media dapat diakses |
| PASS | Xtreme Outdoor by HISTORY | Football & Sports | 200 | 792 ms | Manifest dan segmen media dapat diakses |
| FAIL | Al Jazeera English | World News | 404 | 195 ms | URL tidak ditemukan (HTTP 404) |
| PASS | France 24 English | World News | 200 | 303 ms | Manifest dan segmen media dapat diakses |
| FAIL | NHK World-Japan | World News | 404 | 1615 ms | URL tidak ditemukan (HTTP 404) |
| PASS | DW English | World News | 200 | 256 ms | Manifest dan segmen media dapat diakses |
| PASS | BBC News North America | World News | 200 | 787 ms | Manifest dan segmen media dapat diakses |
| PASS | CNA | World News | 200 | 332 ms | Manifest dan segmen media dapat diakses |
| PASS | TRT World | World News | 200 | 519 ms | Manifest dan segmen media dapat diakses |
| PASS | ABC News Live | World News | 200 | 782 ms | Manifest dan segmen media dapat diakses |
| PASS | Sky News | World News | 200 | 837 ms | Manifest dan segmen media dapat diakses |
| PASS | Euronews English | World News | 200 | 582 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN English | World News | 200 | 388 ms | Manifest dan segmen media dapat diakses |
| PASS | i24NEWS English | World News | 200 | 437 ms | Manifest dan segmen media dapat diakses |
| PASS | Arirang TV | World News | 200 | 1092 ms | Manifest dan segmen media dapat diakses |
| PASS | France 24 Arabic | World News | 200 | 467 ms | Manifest dan segmen media dapat diakses |
| PASS | CBS News 24/7 | World News | 200 | 805 ms | Manifest dan segmen media dapat diakses |
| PASS | Bloomberg Television US | Business | 200 | 363 ms | Manifest dan segmen media dapat diakses |
| PASS | Yahoo! Finance | Business | 200 | 271 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN Global Biz | Business | 200 | 226 ms | Manifest dan segmen media dapat diakses |
| FAIL | NASA TV Media | Documentary | 200 | 166 ms | Master playlist terbuka, tetapi variant gagal: URL tidak ditemukan (HTTP 404) |
| PASS | Smithsonian Channel Selects | Documentary | 200 | 779 ms | Manifest dan segmen media dapat diakses |
| PASS | Love Nature | Documentary | 200 | 835 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN Documentary | Documentary | 200 | 380 ms | Manifest dan segmen media dapat diakses |
| FAIL | Docurama | Documentary | 0 | 387 ms | [Errno -2] Name or service not known |
| PASS | Wonder | Documentary | 200 | 284 ms | Manifest dan segmen media dapat diakses |
| PASS | PBS Nature | Documentary | 200 | 125 ms | Manifest dan segmen media dapat diakses |
| PASS | MagellanTV Now | Documentary | 200 | 335 ms | Manifest dan segmen media dapat diakses |
| PASS | PBS Kids | Kids | 200 | 364 ms | Manifest dan segmen media dapat diakses |
| PASS | Moonbug | Kids | 200 | 170 ms | Manifest dan segmen media dapat diakses |
| PASS | Kartoon Channel | Kids | 200 | 758 ms | Manifest dan segmen media dapat diakses |
| PASS | Biznet Kids | Kids | 200 | 1545 ms | Manifest dan segmen media dapat diakses |
| PASS | Vevo Pop | Music | 200 | 493 ms | Manifest dan segmen media dapat diakses |
| PASS | Vevo Country | Music | 200 | 869 ms | Manifest dan segmen media dapat diakses |
| PASS | Stingray Remember the 80s | Music | 200 | 232 ms | Manifest dan segmen media dapat diakses |
| PASS | Stingray Greatest Hits | Music | 200 | 134 ms | Manifest dan segmen media dapat diakses |
