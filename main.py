import tkinter as tk
from tkinter import messagebox
import threading
import time
import json
import os

from ios_utils import list_devices, get_first_udid, tap, swipe, launch_app, get_device_info

running = False
click_thread = None
PRESET_FILE = "presets.json"
current_udid = None


def load_preset(profile="iphone17"):
    if os.path.exists(PRESET_FILE):
        try:
            with open(PRESET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                preset = data.get(profile, {})
                x_entry.delete(0, tk.END)
                x_entry.insert(0, str(preset.get("x", 200)))

                y_entry.delete(0, tk.END)
                y_entry.insert(0, str(preset.get("y", 600)))

                interval_entry.delete(0, tk.END)
                interval_entry.insert(0, str(preset.get("interval", 1.0)))

                bundle_entry.delete(0, tk.END)
                bundle_entry.insert(0, preset.get("bundle_id", "com.apple.Preferences"))
        except:
            pass


def save_current_preset():
    profile = profile_var.get()
    data = {}
    if os.path.exists(PRESET_FILE):
        try:
            with open(PRESET_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {}

    try:
        data[profile] = {
            "x": int(x_entry.get().strip()),
            "y": int(y_entry.get().strip()),
            "interval": float(interval_entry.get().strip()),
            "bundle_id": bundle_entry.get().strip()
        }
        with open(PRESET_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo("저장 완료", f"{profile} 프리셋 저장 완료")
    except Exception as e:
        messagebox.showerror("저장 오류", str(e))


def update_device_status():
    global current_udid
    devices = list_devices()
    if devices:
        current_udid = devices[0].split()[0]
        status_device.config(text=f"기기 상태: 연결됨 ({current_udid})", fg="green")
        return True
    else:
        current_udid = None
        status_device.config(text="기기 상태: 연결 안 됨", fg="red")
        return False


def show_device_info():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone/iPad가 없습니다.")
        return
    out, err, code = get_device_info(current_udid)
    messagebox.showinfo("기기 정보", out if out else err)


def tap_once():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone/iPad가 없습니다.")
        return

    try:
        x = int(x_entry.get().strip())
        y = int(y_entry.get().strip())
    except:
        messagebox.showwarning("입력 오류", "X, Y 좌표를 숫자로 입력하세요.")
        return

    tap(current_udid, x, y)


def click_loop():
    global running
    while running:
        try:
            x = int(x_entry.get().strip())
            y = int(y_entry.get().strip())
            interval = float(interval_entry.get().strip())
            tap(current_udid, x, y)
            time.sleep(interval)
        except:
            time.sleep(1)


def start_clicking():
    global running, click_thread
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone/iPad가 없습니다.")
        return

    try:
        int(x_entry.get().strip())
        int(y_entry.get().strip())
        float(interval_entry.get().strip())
    except:
        messagebox.showwarning("입력 오류", "좌표와 간격 값을 확인하세요.")
        return

    if running:
        return

    running = True
    status_run.config(text="실행 상태: 작동 중", fg="green")
    click_thread = threading.Thread(target=click_loop, daemon=True)
    click_thread.start()


def stop_clicking():
    global running
    running = False
    status_run.config(text="실행 상태: 정지", fg="red")


def swipe_test():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone/iPad가 없습니다.")
        return
    swipe(current_udid, 200, 800, 200, 300, 0.3)


def open_app():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone/iPad가 없습니다.")
        return

    bundle_id = bundle_entry.get().strip()
    if not bundle_id:
        messagebox.showwarning("입력 오류", "Bundle ID를 입력하세요.")
        return

    launch_app(current_udid, bundle_id)


def switch_profile(*args):
    load_preset(profile_var.get())


root = tk.Tk()
root.title("iPhone 17 / iPad 10 Auto Clicker")
root.geometry("470x560")
root.resizable(False, False)

title = tk.Label(root, text="iPhone 17 / iPad 10 자동 클릭기", font=("맑은 고딕", 14, "bold"))
title.pack(pady=10)

profile_var = tk.StringVar(value="iphone17")
profile_var.trace_add("write", switch_profile)

profile_frame = tk.Frame(root)
profile_frame.pack(pady=5)

tk.Label(profile_frame, text="기기 프리셋:", font=("맑은 고딕", 10)).pack(side=tk.LEFT)
tk.OptionMenu(profile_frame, profile_var, "iphone17", "ipad10").pack(side=tk.LEFT, padx=5)

status_device = tk.Label(root, text="기기 상태: 확인 전", fg="blue", font=("맑은 고딕", 10, "bold"))
status_device.pack(pady=5)

tk.Button(root, text="기기 연결 확인", command=update_device_status, width=22, height=2).pack(pady=5)
tk.Button(root, text="기기 정보 확인", command=show_device_info, width=22, height=2).pack(pady=5)

coord_frame = tk.Frame(root)
coord_frame.pack(pady=10)

tk.Label(coord_frame, text="X 좌표:", font=("맑은 고딕", 10)).grid(row=0, column=0, padx=5, pady=5)
x_entry = tk.Entry(coord_frame, width=12)
x_entry.grid(row=0, column=1, padx=5)

tk.Label(coord_frame, text="Y 좌표:", font=("맑은 고딕", 10)).grid(row=1, column=0, padx=5, pady=5)
y_entry = tk.Entry(coord_frame, width=12)
y_entry.grid(row=1, column=1, padx=5)

interval_frame = tk.Frame(root)
interval_frame.pack(pady=10)

tk.Label(interval_frame, text="반복 간격(초):", font=("맑은 고딕", 10)).pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, width=12)
interval_entry.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="1회 터치", command=tap_once, width=12, height=2).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="자동 시작", command=start_clicking, width=12, height=2, bg="#dff0d8").grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="정지", command=stop_clicking, width=12, height=2, bg="#f2dede").grid(row=0, column=2, padx=5, pady=5)

tk.Button(root, text="테스트 스와이프", command=swipe_test, width=22, height=2).pack(pady=8)

bundle_label = tk.Label(root, text="앱 Bundle ID 실행 (예: com.apple.Preferences)", font=("맑은 고딕", 10))
bundle_label.pack(pady=5)

bundle_entry = tk.Entry(root, width=38)
bundle_entry.pack(pady=5)

tk.Button(root, text="앱 실행", command=open_app, width=22, height=2).pack(pady=8)

tk.Button(root, text="현재 프리셋 저장", command=save_current_preset, width=22, height=2).pack(pady=8)

status_run = tk.Label(root, text="실행 상태: 정지", fg="red", font=("맑은 고딕", 10, "bold"))
status_run.pack(pady=10)

load_preset()
root.mainloop()
