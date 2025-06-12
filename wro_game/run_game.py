#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để chạy WRO Game Practice
Tạo virtual environment, cài đặt dependencies và khởi chạy game
"""

import sys
import subprocess
import os
import venv

def create_virtual_environment():
    """Tạo virtual environment nếu chưa có"""
    venv_path = os.path.join(os.getcwd(), 'venv')

    if not os.path.exists(venv_path):
        print("🔧 Đang tạo virtual environment...")
        try:
            venv.create(venv_path, with_pip=True)
            print("✅ Đã tạo virtual environment thành công!")
        except Exception as e:
            print(f"❌ Lỗi khi tạo virtual environment: {e}")
            return False
    else:
        print("✅ Virtual environment đã tồn tại")

    return True

def get_venv_python():
    """Lấy đường dẫn python trong virtual environment"""
    venv_path = os.path.join(os.getcwd(), 'venv')

    if os.name == 'nt':  # Windows
        python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
    else:  # macOS/Linux
        python_path = os.path.join(venv_path, 'bin', 'python')

    return python_path

def install_dependencies():
    """Cài đặt dependencies trong virtual environment"""
    python_path = get_venv_python()

    if not os.path.exists(python_path):
        print("❌ Không tìm thấy Python trong virtual environment")
        return False

    print("🔧 Đang cài đặt dependencies...")
    try:
        # Upgrade pip trước
        subprocess.check_call([python_path, '-m', 'pip', 'install', '--upgrade', 'pip'])

        # Cài đặt từ requirements.txt
        subprocess.check_call([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Đã cài đặt thành công tất cả dependencies!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi cài đặt dependencies: {e}")
        return False

def check_dependencies():
    """Kiểm tra dependencies đã được cài đặt chưa"""
    python_path = get_venv_python()
    required_packages = ['pygame', 'pillow', 'numpy']

    for package in required_packages:
        try:
            result = subprocess.run([python_path, '-c', f'import {package}'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} đã được cài đặt")
            else:
                print(f"❌ {package} chưa được cài đặt")
                return False
        except Exception as e:
            print(f"❌ Lỗi khi kiểm tra {package}: {e}")
            return False

    return True

def run_game():
    """Chạy game trong virtual environment"""
    python_path = get_venv_python()

    print("\n🚀 Đang khởi động game...")
    try:
        # Chạy game trong virtual environment
        subprocess.run([python_path, 'main.py'])
    except Exception as e:
        print(f"❌ Lỗi khi chạy game: {e}")
        print("\nVui lòng kiểm tra:")
        print("1. Tất cả file game có đầy đủ không")
        print("2. Dependencies đã được cài đặt đúng chưa")
        print("3. Có lỗi trong code không")
        input("\nNhấn Enter để thoát...")

def main():
    """Hàm main"""
    print("🤖 WRO Game Practice - Launcher")
    print("=" * 40)

    # Kiểm tra Python version
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên để chạy game")
        print(f"Phiên bản hiện tại: {sys.version}")
        input("\nNhấn Enter để thoát...")
        return

    print(f"✅ Python version: {sys.version.split()[0]}")

    # Tạo virtual environment
    print("\n🔧 Chuẩn bị môi trường...")
    if not create_virtual_environment():
        input("\nNhấn Enter để thoát...")
        return

    # Cài đặt dependencies
    print("\n📦 Cài đặt dependencies...")
    if not install_dependencies():
        input("\nNhấn Enter để thoát...")
        return

    # Kiểm tra dependencies
    print("\n🔍 Kiểm tra dependencies...")
    if not check_dependencies():
        print("❌ Một số dependencies chưa được cài đặt đúng")
        input("\nNhấn Enter để thoát...")
        return

    # Chạy game
    run_game()

if __name__ == "__main__":
    main()
