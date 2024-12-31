import os
import subprocess
import socket
import platform
from telegram import send_message


def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        return f"Не удалось определить IP-адрес: {e}"

def get_os_info():
    os_info = platform.system() + " " + platform.release()
    return os_info

def get_load_average():
    try:
        load1, load5, load15 = os.getloadavg()
        return f"1 мин: {load1:.2f}, 5 мин: {load5:.2f}, 15 мин: {load15:.2f}"
    except AttributeError:
        return "Load average недоступен"

def check_disk_space():
    result = subprocess.run(['df', '/'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    lines = output.splitlines()
    disk_info = lines[1].split()
    total = int(disk_info[1]) * 1024  # в байтах
    used = int(disk_info[2]) * 1024
    available = int(disk_info[3]) * 1024
    free_percent = available / total * 100
    return {
        'total_gb': total / (1024**3),
        'used_gb': used / (1024**3),
        'available_gb': available / (1024**3),
        'free_percent': free_percent
    }

def check_memory():
    with open('/proc/meminfo', 'r') as meminfo:
        mem_data = {}
        for line in meminfo:
            if line.startswith('MemTotal:'):
                mem_data['total'] = int(line.split()[1]) * 1024  # в байтах
            elif line.startswith('MemAvailable:'):
                mem_data['available'] = int(line.split()[1]) * 1024
        used = mem_data['total'] - mem_data['available']
        free_percent = mem_data['available'] / mem_data['total'] * 100
        return {
            'total_gb': mem_data['total'] / (1024**3),
            'used_gb': used / (1024**3),
            'available_gb': mem_data['available'] / (1024**3),
            'free_percent': free_percent
        }


if __name__ == "__main__":
    ip_address = get_ip_address()
    os_info = get_os_info()
    load_avg = get_load_average()
    disk_stats = check_disk_space()
    memory_stats = check_memory()

    message = f"""
📊 <b>Системный мониторинг</b> 📊

🖥️ <b>IP-адрес:</b> {ip_address}
🛡️ <b>ОС:</b> {os_info}
⚙️ <b>Load Average:</b> {load_avg}

💾 <b>Дисковое пространство (/):</b>
• Всего: {disk_stats['total_gb']:.2f} ГБ
• Использовано: {disk_stats['used_gb']:.2f} ГБ
• Свободно: {disk_stats['available_gb']:.2f} ГБ ({disk_stats['free_percent']:.2f}%)

🧠 <b>Оперативная память:</b>
• Всего: {memory_stats['total_gb']:.2f} ГБ
• Использовано: {memory_stats['used_gb']:.2f} ГБ
• Свободно: {memory_stats['available_gb']:.2f} ГБ ({memory_stats['free_percent']:.2f}%)
"""

    # Проверка на наличие предупреждений
    warnings = ""
    if disk_stats['free_percent'] < 20:
        warnings += "⚠️ <b>Внимание!</b> Мало свободного места на жестком диске.\n"
    if memory_stats['free_percent'] < 20:
        warnings += "⚠️ <b>Внимание!</b> Мало свободной оперативной памяти.\n"

    if warnings != "":
        final_message = warnings + message

        send_message(final_message)
