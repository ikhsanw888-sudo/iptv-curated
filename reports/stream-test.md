# IPTV Stream Test Report

- Total: **52**
- PASS: **40**
- REVIEW: **2**
- FAIL: **10**

> Pengujian dilakukan dari GitHub Actions, bukan dari jaringan STB di Indonesia. Hasil REVIEW dapat disebabkan geo-blocking, kebutuhan header khusus, atau pembatasan CDN.

| Result | Channel | Category | HTTP | Response | Detail |
|---|---|---|---:|---:|---|
| PASS | Metro TV | Indonesia | 200 | 1917 ms | Manifest dan segmen media dapat diakses |
| PASS | TVRI Nasional | Indonesia | 200 | 1065 ms | Manifest dan segmen media dapat diakses |
| FAIL | CNBC Indonesia | Indonesia | 404 | 822 ms | URL tidak ditemukan (HTTP 404) |
| REVIEW | BeritaSatu | Indonesia | 403 | 708 ms | Akses dibatasi atau kemungkinan geo-block: HTTP 403: Forbidden |
| FAIL | TVRI Sport | Indonesia | 404 | 1083 ms | URL tidak ditemukan (HTTP 404) |
| PASS | TVRI World | Indonesia | 200 | 801 ms | Manifest dan segmen media dapat diakses |
| PASS | Rajawali TV (RTV) | Indonesia | 200 | 4555 ms | Manifest dan segmen media dapat diakses |
| PASS | Garuda TV | Indonesia | 200 | 1433 ms | Manifest dan segmen media dapat diakses |
| PASS | FIFA+ | Football & Sports | 200 | 365 ms | Manifest dan segmen media dapat diakses |
| REVIEW | CBS Sports Golazo | Football & Sports | 500 | 442 ms | Server sedang bermasalah: HTTP 500: Domain Not Found |
| PASS | SportsGrid | Football & Sports | 200 | 334 ms | Manifest dan segmen media dapat diakses |
| PASS | beIN SPORTS Xtra | Football & Sports | 200 | 240 ms | Manifest dan segmen media dapat diakses |
| PASS | Red Bull TV | Football & Sports | 200 | 316 ms | Manifest dan segmen media dapat diakses |
| PASS | CBS Sports HQ | Football & Sports | 200 | 805 ms | Manifest dan segmen media dapat diakses |
| FAIL | FUEL TV | Football & Sports | 404 | 115 ms | URL tidak ditemukan (HTTP 404) |
| PASS | Fight Network | Football & Sports | 200 | 317 ms | Manifest dan segmen media dapat diakses |
| PASS | World Poker Tour | Football & Sports | 200 | 137 ms | Manifest dan segmen media dapat diakses |
| FAIL | EDGEsport | Football & Sports | 0 | 103 ms | [Errno -2] Name or service not known |
| FAIL | Al Jazeera English | World News | 0 | 159 ms | [Errno -2] Name or service not known |
| FAIL | France 24 English | World News | 200 | 282 ms | Master playlist terbuka, tetapi variant gagal: HTTP 400: Bad Request |
| FAIL | NHK World-Japan | World News | 404 | 1480 ms | URL tidak ditemukan (HTTP 404) |
| PASS | DW English | World News | 200 | 208 ms | Manifest dan segmen media dapat diakses |
| PASS | BBC News North America | World News | 200 | 809 ms | Manifest dan segmen media dapat diakses |
| PASS | CNA | World News | 200 | 338 ms | Manifest dan segmen media dapat diakses |
| PASS | TRT World | World News | 200 | 301 ms | Manifest dan segmen media dapat diakses |
| PASS | ABC News Live | World News | 200 | 797 ms | Manifest dan segmen media dapat diakses |
| PASS | Sky News | World News | 200 | 861 ms | Manifest dan segmen media dapat diakses |
| PASS | Euronews English | World News | 200 | 572 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN English | World News | 200 | 389 ms | Manifest dan segmen media dapat diakses |
| PASS | i24NEWS English | World News | 200 | 422 ms | Manifest dan segmen media dapat diakses |
| PASS | Arirang TV | World News | 200 | 1218 ms | Manifest dan segmen media dapat diakses |
| PASS | France 24 Arabic | World News | 200 | 568 ms | Manifest dan segmen media dapat diakses |
| PASS | CBS News 24/7 | World News | 200 | 714 ms | Manifest dan segmen media dapat diakses |
| PASS | Bloomberg Television US | Business | 200 | 272 ms | Manifest dan segmen media dapat diakses |
| PASS | Yahoo! Finance | Business | 200 | 232 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN Global Biz | Business | 200 | 206 ms | Manifest dan segmen media dapat diakses |
| FAIL | NASA Live (Legacy Feed) | Documentary | 404 | 186 ms | URL tidak ditemukan (HTTP 404) |
| PASS | Smithsonian Channel Selects | Documentary | 200 | 764 ms | Manifest dan segmen media dapat diakses |
| PASS | Love Nature | Documentary | 200 | 743 ms | Manifest dan segmen media dapat diakses |
| PASS | CGTN Documentary | Documentary | 200 | 376 ms | Manifest dan segmen media dapat diakses |
| FAIL | Docurama | Documentary | 0 | 172 ms | [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1010) |
| PASS | Wonder | Documentary | 200 | 178 ms | Manifest dan segmen media dapat diakses |
| PASS | PBS Nature | Documentary | 200 | 178 ms | Manifest dan segmen media dapat diakses |
| PASS | MagellanTV Now | Documentary | 200 | 441 ms | Manifest dan segmen media dapat diakses |
| PASS | PBS Kids | Kids | 200 | 355 ms | Manifest dan segmen media dapat diakses |
| PASS | Moonbug | Kids | 200 | 184 ms | Manifest dan segmen media dapat diakses |
| FAIL | Kidoodle.TV | Kids | 200 | 190 ms | Respons dapat diakses, tetapi bukan manifest HLS #EXTM3U (Content-Type: application/vnd.apple.mpegurl) |
| PASS | Biznet Kids | Kids | 200 | 1690 ms | Manifest dan segmen media dapat diakses |
| PASS | Vevo Pop | Music | 200 | 534 ms | Manifest dan segmen media dapat diakses |
| PASS | Vevo Country | Music | 200 | 822 ms | Manifest dan segmen media dapat diakses |
| PASS | Stingray Remember the 80s | Music | 200 | 311 ms | Manifest dan segmen media dapat diakses |
| PASS | Stingray Greatest Hits | Music | 200 | 320 ms | Manifest dan segmen media dapat diakses |
