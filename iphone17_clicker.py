import tkinter as tk
from tkinter import messagebox
import threading
import time

from ios_utils import list_devices, tap, swipe, launch_app, get_device_info

running = False
click_thread = None
current_udid = None

# iPhone 17 sample preset (separate app)
DEFAULT_X = 200
DEFAULT_Y = 600
DEFAULT_INTERVAL = 1.0
DEFAULT_BUNDLE = "com.apple.Preferences"


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
        messagebox.showwarning("연결 오류", "연결된 iPhone이 없습니다.")
        return
    out, err, code = get_device_info(current_udid)
    messagebox.showinfo("기기 정보", out if out else err)


def tap_once():
    if not update_device_status():
        messagebox.showwarning("연결 오류", "연결된 iPhone이 없습니다.")
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
        messagebox.showwarning("연결 오류", "연결된 iPhone이 없습니다.")
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
        return
    swipe(current_udid, 200, 800, 200, 300, 0.3)


def open_app():
    if not update_device_status():
        return
    bundle_id = bundle_entry.get().strip()
    if not bundle_id:
        messagebox.showwarning("입력 오류", "Bundle ID를 입력하세요.")
        return
    launch_app(current_udid, bundle_id)


root = tk.Tk()
root.title("iPhone 17 Auto Clicker")
root.geometry("450x520")
root.resizable(False, False)

tk.Label(root, text="iPhone 17 자동 클릭기", font=("맑은 고딕", 14, "bold")).pack(pady=10)
status_device = tk.Label(root, text="기기 상태: 확인 전", fg="blue", font=("맑은 고딕", 10, "bold"))
status_device.pack(pady=5)

tk.Button(root, text="기기 연결 확인", command=update_device_status, width=22, height=2).pack(pady=5)
tk.Button(root, text="기기 정보 확인", command=show_device_info, width=22, height=2).pack(pady=5)

coord_frame = tk.Frame(root)
coord_frame.pack(pady=10)

tk.Label(coord_frame, text="X 좌표:").grid(row=0, column=0, padx=5, pady=5)
x_entry = tk.Entry(coord_frame, width=12)
x_entry.insert(0, str(DEFAULT_X))
x_entry.grid(row=0, column=1, padx=5)

tk.Label(coord_frame, text="Y 좌표:").grid(row=1, column=0, padx=5, pady=5)
y_entry = tk.Entry(coord_frame, width=12)
y_entry.insert(0, str(DEFAULT_Y))
y_entry.grid(row=1, column=1, padx=5)

interval_frame = tk.Frame(root)
interval_frame.pack(pady=10)
tk.Label(interval_frame, text="반복 간격(초):").pack(side=tk.LEFT)
interval_entry = tk.Entry(interval_frame, width=12)
interval_entry.insert(0, str(DEFAULT_INTERVAL))
interval_entry.pack(side=tk.LEFT, padx=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)
tk.Button(btn_frame, text="1회 터치", command=tap_once, width=12, height=2).grid(row=0, column=0, padx=5, pady=5)
tk.Button(btn_frame, text="자동 시작", command=start_clicking, width=12, height=2).grid(row=0, column=1, padx=5, pady=5)
tk.Button(btn_frame, text="정지", command=stop_clicking, width=12, height=2).grid(row=0, column=2, padx=5, pady=5)

tk.Button(root, text="테스트 스와이프", command=swipe_test, width=22, height=2).pack(pady=8)
tk.Label(root, text="앱 Bundle ID 실행 (예: com.apple.Preferences)").pack(pady=5)
bundle_entry = tk.Entry(root, width=38)
bundle_entry.insert(0, DEFAULT_BUNDLE)
bundle_entry.pack(pady=5)
tk.Button(root, text="앱 실행", command=open_app, width=22, height=2).pack(pady=8)

status_run = tk.Label(root, text="실행 상태: 정지", fg="red", font=("맑은 고딕", 10, "bold"))
status_run.pack(pady=10)

root.mainloop()
