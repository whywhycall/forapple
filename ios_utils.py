import subprocess


def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), 1


def list_devices():
    out, err, code = run_cmd(["tidevice", "list"])
    if code != 0:
        return []

    devices = []
    for line in out.splitlines():
        line = line.strip()
        if line:
            devices.append(line)
    return devices


def get_first_udid():
    devices = list_devices()
    if not devices:
        return None
    return devices[0].split()[0]


def tap(udid, x, y):
    return run_cmd(["tidevice", "--udid", udid, "xcuitest", "tap", str(x), str(y)])


def swipe(udid, x1, y1, x2, y2, duration=0.3):
    return run_cmd([
        "tidevice", "--udid", udid, "xcuitest", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration)
    ])


def launch_app(udid, bundle_id):
    return run_cmd(["tidevice", "--udid", udid, "launch", bundle_id])


def get_device_info(udid):
    return run_cmd(["tidevice", "--udid", udid, "info"])
