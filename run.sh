#!/bin/bash

# 1. Pindah secara dinamis ke folder tempat skrip ini berada (Portabel di semua komputer)
cd "$(dirname "$0")"

# 2. Jika di-klik ganda dari File Manager (tanpa terminal), buka terminal yang tersedia di OS user
if [ ! -t 0 ]; then
    for term in konsole gnome-terminal ptyxis xfce4-terminal alacritty kitty xterm; do
        if command -v "$term" &> /dev/null; then
            SCRIPT_PATH="$(realpath "$0")"
            exec "$term" -e bash "$SCRIPT_PATH"
        fi
    done
fi

# 3. Fitur "Zero Setup": Jika user baru clone dan belum punya venv, buatkan otomatis!
if [ ! -d "venv" ]; then
    echo "Environment belum ditemukan. Menyiapkan DeskPad untuk pertama kali..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 4. Jalankan aplikasi
python main.py