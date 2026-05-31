import shutil
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def copy_file_or_dir(src, dst):
    """Копирует файл или папку из src в dst."""
    try:
        if os.path.isfile(src):
            shutil.copy2(src, dst)  # copy2 сохраняет метаданные
        elif os.path.isdir(src):
            # Имя исходной папки для создания внутри dst
            dest_path = os.path.join(dst, os.path.basename(src))
            shutil.copytree(src, dest_path)
        else:
            raise FileNotFoundError(f"Источник не найден: {src}")
        return True, "Копирование выполнено успешно!"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"


def select_source():
    """Открывает диалог выбора файла или папки."""
    # Сначала спрашиваем, что копировать: файл или папку
    choice = messagebox.askyesno(
        "Выбор типа",
        "Нажмите 'Да' для выбора папки, 'Нет' для выбора файла."
    )
    if choice:  # Папка
        path = filedialog.askdirectory(title="Выберите папку для копирования")
    else:  # Файл
        path = filedialog.askopenfilename(title="Выберите файл для копирования")

    if path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, path)


def start_copy():
    """Запускает процесс копирования с выбранным источником."""
    src = source_entry.get().strip()
    if not src:
        messagebox.showwarning("Предупреждение", "Сначала выберите файл или папку!")
        return

    dst = r"D:\SERVER"
    # Создаём папку назначения, если её нет
    os.makedirs(dst, exist_ok=True)

    # Обновляем статус
    status_label.config(text="Копирование...", fg="blue")
    root.update_idletasks()

    success, msg = copy_file_or_dir(src, dst)
    if success:
        status_label.config(text=msg, fg="green")
        messagebox.showinfo("Успех", msg)
    else:
        status_label.config(text=msg, fg="red")
        messagebox.showerror("Ошибка", msg)


# Создаём главное окно
root = tk.Tk()
root.title("SAVEPROGRAM - Резервное копирование")
root.geometry("500x250")
root.resizable(False, False)

# Виджеты
label_title = tk.Label(root, text="Резервное копирование файлов и папок", font=("Arial", 14))
label_title.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

source_entry = tk.Entry(frame, width=50)
source_entry.pack(side=tk.LEFT, padx=5)

browse_btn = tk.Button(frame, text="Обзор...", command=select_source)
browse_btn.pack(side=tk.LEFT)

copy_btn = tk.Button(root, text="КОПИРОВАТЬ НА D:\\SERVER", command=start_copy,
                     bg="lightblue", font=("Arial", 10, "bold"))
copy_btn.pack(pady=20)

status_label = tk.Label(root, text="Готов к работе", font=("Arial", 10))
status_label.pack(pady=5)

root.mainloop()
