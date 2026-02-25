import subprocess

diskutil_output = subprocess.check_output(["diskutil", "list"]).decode("utf-8")
efis = [line.split()[-1] for line in diskutil_output.splitlines() if "EFI" in line]

efi_list = []
for efi in efis:
    if not efi.startswith("disk"):
        continue
    parent_disk = efi.split('s')[0]
    parent_info = subprocess.check_output(["diskutil", "info", parent_disk]).decode("utf-8")
    media_name_line = [line for line in parent_info.splitlines() if "Device / Media Name:" in line]
    disk_name = media_name_line[0].split(":", 1)[1].strip() if media_name_line else "Disco Desconhecido"
    
    efi_list.append(f"{efi} ({disk_name})")

print(efi_list)
