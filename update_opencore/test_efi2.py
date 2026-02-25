import subprocess
diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
raw_parts = [line.split()[-1] for line in diskutil_output.splitlines() if "disk" in line.split()[-1] and "s" in line.split()[-1]]

for part in raw_parts:
    try:
        part_info = subprocess.check_output(["diskutil", "info", part]).decode("utf-8").lower()
        if "fat32" in part_info or "ms-dos" in part_info or "efi" in part_info:
            print(f"FAT32 match: {part}")
    except:
        pass
