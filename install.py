#!/usr/bin/env python3
"""
Termux-Package Installer
Author: SoraDev-ID
Description: Tools instalasi perintah dan package Termux untuk pemula.
Repo: https://github.com/SoraDev-ID/Termux-Package
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path

# Lokasi direktori file script
BASE_DIR = Path(__file__).resolve().parent
PACKAGES_FILE = BASE_DIR / "packages.txt"
REQUIREMENTS_FILE = BASE_DIR / "requirements.txt"

# Kode warna ANSI untuk styling terminal
C_RESET = "\033[0m"
C_BOLD = "\033[1m"
C_GREEN = "\033[92m"
C_CYAN = "\033[96m"
C_BLUE = "\033[94m"
C_YELLOW = "\033[93m"
C_RED = "\033[91m"
C_DIM = "\033[90m"


def clear_screen():
    """Membersihkan layar terminal."""
    os.system("clear" if os.name != "nt" else "cls")


def show_banner():
    """
    Menampilkan banner SoraDev-ID.
    Mencoba memakai toilet + lolcat jika sudah terpasang di sistem,
    atau menggunakan fallback ASCII banner bawaan yang ringan & elegan.
    """
    clear_screen()
    has_toilet = shutil.which("toilet") is not None
    has_lolcat = shutil.which("lolcat") is not None

    if has_toilet and has_lolcat:
        try:
            # Gunakan toilet + lolcat jika tersedia di sistem
            p1 = subprocess.Popen(["toilet", "-f", "standard", "SoraDev-ID"], stdout=subprocess.PIPE)
            subprocess.run(["lolcat"], stdin=p1.stdout)
            p1.stdout.close()
            p1.wait()
            print(f"{C_CYAN}{C_BOLD}   [ TOOLS INSTALL PERINTAH TERMUX BUAT PEMULA ]{C_RESET}\n")
            return
        except Exception:
            pass  # Fallback ke ASCII banner di bawah jika terjadi kendala pipa

    # ASCII Banner Fallback (berfungsi di semua instalasi Termux baru)
    ascii_art = r"""
  ____                  ____                 ___ ____  
 / ___|  ___  _ __ __ _|  _ \  _____   __   |_ _|  _ \ 
 \___ \ / _ \| '__/ _` | | | |/ _ \ \ / /____| || | | |
  ___) | (_) | | | (_| | |_| |  __/\ V /_____| || |_| |
 |____/ \___/|_|  \__,_|____/ \___| \_/     |___|____/ 
"""
    banner_text = (
        f"{C_CYAN}{C_BOLD}{ascii_art}{C_RESET}\n"
        f"{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}\n"
        f" {C_BOLD}Author     :{C_RESET} SoraDev-ID\n"
        f" {C_BOLD}Deskripsi  :{C_RESET} Tools Instalasi Package Termux Buat Pemula\n"
        f" {C_BOLD}Repository :{C_RESET} https://github.com/SoraDev-ID/Termux-Package\n"
        f"{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}\n"
    )
    print(banner_text)


def load_list_from_file(file_path: Path) -> list:
    """
    Membaca daftar package dari file teks.
    Mengabaikan baris kosong dan baris komentar (#).
    """
    if not file_path.exists():
        print(f"{C_YELLOW}[!] File {file_path.name} tidak ditemukan.{C_RESET}")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        packages = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]
    return packages


def get_pkg_manager() -> str:
    """Mendeteksi package manager utama (pkg di Termux, atau apt-get)."""
    if shutil.which("pkg"):
        return "pkg"
    elif shutil.which("apt-get"):
        return "apt-get"
    elif shutil.which("apt"):
        return "apt"
    return "pkg"


def update_system():
    """Menjalankan pembaruan repository package Termux."""
    pkg_mgr = get_pkg_manager()
    print(f"\n{C_CYAN}➜ Memperbarui index repository ({pkg_mgr} update)...{C_RESET}")
    try:
        subprocess.run([pkg_mgr, "update", "-y"], check=False)
    except Exception as e:
        print(f"{C_RED}[!] Gagal menjalankan {pkg_mgr} update: {e}{C_RESET}")


def install_system_packages():
    """
    Membaca packages.txt dan menginstal package sistem satu per satu.
    Jika satu package gagal, proses tetap lanjut ke package berikutnya.
    """
    packages = load_list_from_file(PACKAGES_FILE)
    if not packages:
        print(f"{C_YELLOW}[!] Tidak ada package sistem di dalam {PACKAGES_FILE.name}{C_RESET}")
        return

    pkg_mgr = get_pkg_manager()
    print(f"\n{C_BOLD}{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}")
    print(f"{C_BOLD}Memulai Instalasi Package Sistem ({len(packages)} item){C_RESET}")
    print(f"{C_BOLD}{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}\n")

    success = 0
    failed = []

    for idx, pkg in enumerate(packages, start=1):
        print(f"[{idx}/{len(packages)}] Menginstal {C_BOLD}{pkg}{C_RESET}...", end=" ", flush=True)
        try:
            cmd = [pkg_mgr, "install", "-y", pkg]
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"{C_GREEN}[✓ OK]{C_RESET}")
                success += 1
            else:
                print(f"{C_RED}[✗ GAGAL]{C_RESET}")
                failed.append(pkg)
        except Exception as e:
            print(f"{C_RED}[✗ ERROR: {e}]{C_RESET}")
            failed.append(pkg)

    # Ringkasan hasil instalasi sistem
    print(f"\n{C_CYAN}Ringkasan Package Sistem:{C_RESET}")
    print(f"  • Berhasil : {C_GREEN}{success}{C_RESET} package")
    if failed:
        print(f"  • Gagal    : {C_RED}{len(failed)}{C_RESET} ({', '.join(failed)})")
    else:
        print(f"  • Gagal    : {C_GREEN}0{C_RESET}")


def install_python_packages():
    """
    Membaca requirements.txt dan menginstal library Python via pip.
    Memastikan pip terpasang terlebih dahulu, lalu menginstal modul satu per satu.
    """
    reqs = load_list_from_file(REQUIREMENTS_FILE)
    if not reqs:
        print(f"{C_YELLOW}[!] Tidak ada modul di dalam {REQUIREMENTS_FILE.name}{C_RESET}")
        return

    # Pastikan pip terpasang
    if not shutil.which("pip"):
        print(f"{C_YELLOW}➜ Memasang pip terlebih dahulu...{C_RESET}")
        pkg_mgr = get_pkg_manager()
        subprocess.run([pkg_mgr, "install", "-y", "python"], check=False)

    print(f"\n{C_BOLD}{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}")
    print(f"{C_BOLD}Memulai Instalasi Modul Python / Pip ({len(reqs)} item){C_RESET}")
    print(f"{C_BOLD}{C_BLUE}══════════════════════════════════════════════════════════════{C_RESET}\n")

    success = 0
    failed = []

    for idx, module in enumerate(reqs, start=1):
        print(f"[{idx}/{len(reqs)}] Menginstal {C_BOLD}{module}{C_RESET}...", end=" ", flush=True)
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade", module]
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                print(f"{C_GREEN}[✓ OK]{C_RESET}")
                success += 1
            else:
                print(f"{C_RED}[✗ GAGAL]{C_RESET}")
                failed.append(module)
        except Exception as e:
            print(f"{C_RED}[✗ ERROR: {e}]{C_RESET}")
            failed.append(module)

    # Ringkasan hasil instalasi pip
    print(f"\n{C_CYAN}Ringkasan Modul Python:{C_RESET}")
    print(f"  • Berhasil : {C_GREEN}{success}{C_RESET} modul")
    if failed:
        print(f"  • Gagal    : {C_RED}{len(failed)}{C_RESET} ({', '.join(failed)})")
    else:
        print(f"  • Gagal    : {C_GREEN}0{C_RESET}")


def show_menu():
    """Menampilkan pilihan menu utama."""
    print(f"""
{C_BOLD}PILIHAN MENU:{C_RESET}
 {C_CYAN}[1]{C_RESET} Install Python & Pip Packages ({REQUIREMENTS_FILE.name})
 {C_CYAN}[2]{C_RESET} Install Semua Package (Update + Sistem + Python)
 {C_CYAN}[3]{C_RESET} Tampilkan Banner Saja
 {C_RED}[0]{C_RESET} Keluar
""")


def main():
    """Fungsi utama program."""
    while True:
        show_banner()
        show_menu()
        try:
            choice = input(f"{C_YELLOW}Pilih opsi [0-3]: {C_RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{C_CYAN}Terima kasih telah menggunakan Termux-Package! Sampai jumpa.{C_RESET}")
            break

        if choice == "1":
            install_python_packages()
            input(f"\n{C_DIM}Tekan [Enter] untuk kembali ke menu...{C_RESET}")
        elif choice == "2":
            update_system()
            install_system_packages()
            install_python_packages()
            input(f"\n{C_DIM}Tekan [Enter] untuk kembali ke menu...{C_RESET}")
        elif choice == "3":
            # Hanya menampilkan banner lalu menunggu interaksi
            input(f"\n{C_DIM}Tekan [Enter] untuk kembali ke menu...{C_RESET}")
        elif choice == "0":
            print(f"\n{C_GREEN}Terima kasih telah menggunakan Termux-Package! Sampai jumpa.{C_RESET}\n")
            break
        else:
            print(f"\n{C_RED}[!] Pilihan tidak valid. Silakan pilih 0, 1, 2, atau 3.{C_RESET}")
            input(f"{C_DIM}Tekan [Enter] untuk mencoba lagi...{C_RESET}")


if __name__ == "__main__":
    main()
