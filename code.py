import os
import sys

def is_hidden(filepath):
    name = os.path.basename(os.path.abspath(filepath))
    if name.startswith('.'):
        return True
    if os.name == 'nt':
        import ctypes
        attrs = ctypes.windll.kernel32.GetFileAttributesW(str(filepath))
        return attrs != -1 and bool(attrs & 2)
    return False

def clean_hidden_files(directory):
    removed = []
    for root, dirs, files in os.walk(directory):
        for item in files + dirs:
            path = os.path.join(root, item)
            try:
                if is_hidden(path):
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        os.rmdir(path)
                    removed.append(path)
            except Exception:
                pass
    return removed

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python hidden_cleaner.py <directory_path>")
        sys.exit(1)
    target_dir = sys.argv[1]
    if not os.path.isdir(target_dir):
        print("Invalid directory")
        sys.exit(1)
    deleted_items = clean_hidden_files(target_dir)
    for item in deleted_items:
        print(f"Removed: {item}")
    print(f"Total removed: {len(deleted_items)}")
