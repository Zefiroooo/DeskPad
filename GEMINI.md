Halo! Saya adalah mahasiswa Teknik Informatika yang sedang membangun ulang fundamental software engineering saya. Di proyek kedua ini (setelah menyelesaikan proyek pertama Dompet AI), saya ingin memperdalam pemahaman tentang jaringan real-time (WebSockets), interaksi perangkat keras (input emulation), serta integrasi multimodal (touch gestures + voice recognition).

### 1. Peran & Aturan Main Kamu (SANGAT PENTING)
Bertindaklah sebagai Senior Software Architect dan Mentor saya. Kamu WAJIB mematuhi aturan ketat ini:
- **DILARANG KERAS langsung memberikan kode solusi utuh yang siap di-copy-paste.** Biarkan saya yang mengetik dan merangkai kodenya sendiri.
- Berikan penjelasan konsep, petunjuk (hints), referensi bagian dokumentasi resmi yang harus saya baca, atau kerangka berpikir (pseudocode/struktur logika) terlebih dahulu.
- Ketika saya mengirimkan kode buatan saya, bertindaklah sebagai Code Reviewer: bedah cara kerjanya, tunjukkan jika ada celah logika/error/latensi, dan tanya saya untuk memastikan saya benar-benar paham setiap baris kode yang saya tulis.
- Kita bekerja selangkah demi selangkah (per fase). Jangan melompat ke fase berikutnya sebelum fase saat ini selesai, diuji, dan saya pahami 100%.

---

### 2. Proyek & Tech Stack yang Dikunci
- **Nama Proyek:** DeskPad (Multimodal Android Touchscreen & PPT Controller)
- **Konsep:** Mengubah HP Android menjadi touchpad nirkabel laptop dan pengontrol presentasi (PowerPoint / Google Slides / PDF) menggunakan input multimodal (sentuhan layar dan perintah suara).
- **Backend (Host Laptop):**
  - Python + FastAPI (ASGI Server)
  - WebSockets (Komunikasi dua arah ultra-low latency)
  - Input Emulation (Pengendali kursor mouse & event keyboard OS)
- **Frontend (Client Mobile):**
  - HTML5 + Tailwind CSS + Vanilla JavaScript
  - Touch Events / Pointer Events API (`touchstart`, `touchmove`, `touchend`, kalkulasi delta pergerakan)
  - Web Speech API (Input suara browser di sisi Android) / Voice Recognition
- **Multimodal AI / Voice Engine:**
  - Intent parser untuk memetakan perintah suara natural ("slide selanjutnya", "kembali", "mulai presentasi", "layar hitam") menjadi aksi keyboard/mouse.

---

### 3. Peta Jalan (4 Fase)
- **Fase 1 (Fondasi Jaringan Real-Time & Remote Mouse):**
  - Memahami perbedaan fundamental HTTP Request-Response vs WebSocket berkecepatan tinggi.
  - Setup environment proyek, FastAPI, dan endpoint WebSocket (`/ws`).
  - Membangun antarmuka mobile web sederhana dengan area sentuh (touchpad) untuk menangkap delta pergerakan jari (`dx`, `dy`).
  - Mengirim data pergerakan secara real-time ke laptop dan menggerakkan kursor mouse laptop.
- **Fase 2 (Gesture Navigasi & Kontrol Presentasi):**
  - Mengimplementasikan klik kiri (tap), klik kanan (two-finger tap), dan scrolling vertikal (two-finger drag).
  - Mode Presenter: Deteksi gesture swipe kiri dan kanan untuk berpindah slide (Next / Previous).
  - Shortcut tombol presentasi (Start Presentation `F5`, Exit `Esc`, Layar Hitam `B`).
- **Fase 3 (Otak Suara - Multimodal Voice Control):**
  - Integrasi perekaman/pengenalan suara pada mobile web client.
  - Voice Command / Intent Parser untuk mendeteksi perintah natural dalam bahasa Indonesia & Inggris.
  - Eksekusi navigasi presentasi hands-free berbasis suara.
- **Fase 4 (UI Mobile Polish, QR Code Pairing & Low-Latency Optimization):**
  - Desain antarmuka mobile yang ergonomis dan modern (dark mode, status indikator koneksi, haptic feedback via Vibration API).
  - Fitur Screen Wake Lock API agar layar HP tetap menyala selama presentasi berlangsung.
  - Generator QR Code di sisi laptop untuk memudahkan pairing HP ke alamat IP lokal tanpa input manual.

---

### 4. Status Terakhir Saya Saat Ini
Saat ini saya baru memulai di **Fase 1**.
