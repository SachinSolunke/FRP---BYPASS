#!/usr/bin/python
# ==============================================================================
# 🔥 PROJECT AGNI v2.0 - The Phoenix 🔥
# Ek sampoorn shastragar, aapke andaaz mein.
#
# By The Emperor (Sachin Solunke) & his Senapati, Jarvis. ❤️
# ==============================================================================

import os
import sys
import time
import subprocess
import shutil

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
except ImportError:
    print("\n[!] 'rich' library nahi mili. Kripya 'pip install rich' chalayein.\n")
    sys.exit(1)

console = Console()

# --- HELPER FUNCTIONS ---
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')
def run_command(command, title="..."):
    console.print(Panel(f"[cyan]$ {command}[/cyan]", title=f"[yellow]{title}[/yellow]", border_style="green", subtitle="Executing"))
    return subprocess.call(command, shell=True)
def check_dependencies(tools):
    missing = [tool for tool in tools if not shutil.which(tool)]
    if missing:
        console.print(Panel(f"[red]Galti: Yeh zaroori auzaar nahi mile: {', '.join(missing)}[/red]", title="Dependency Error"))
        sys.exit(1)

# --- ASTRA LAUNCHERS ---

def guide_unlock_bootloader():
    clear_screen(); console.print(Panel("[bold]🔓 1 - Unlock Bootloader[/bold]", style="bold on blue"))
    console.print("[red]Chetaavni: Isse aapka saara data DELETE ho jayega.[/red]")
    console.print("\n[bold]Nirdesh:[/bold]\n1. Phone mein 'Developer Options' on karein.\n2. 'OEM Unlocking' on karein.\n3. Phone ko Fastboot mode mein daalein.")
    if Prompt.ask("\n[bold]Universal 'fastboot oem unlock' command chalayein?[/bold]", choices=["y", "n"]) == "y":
        run_command("fastboot oem unlock", "Unlocking Bootloader")

def fastboot_flasher():
    clear_screen(); console.print(Panel("[bold]⚡ 2 - Flash Fastboot ROM[/bold]", style="bold on red"))
    search_path = os.path.expanduser('~/storage/shared'); rom_paths = []
    with console.status("[green]Fastboot ROMs dhoondhe ja rahe hain...[/green]"):
        for root, dirs, files in os.walk(search_path):
            if 'Android' in dirs: dirs.remove('Android')
            if 'images' in dirs and any(f.startswith('flash_all') for f in files): rom_paths.append(root)
            for file in files:
                if file.endswith(".tgz"): rom_paths.append(os.path.join(root, file))
    if not rom_paths: console.print("[red]❌ Koi Fastboot ROM (.tgz ya folder) nahi mila.[/red]"); return
    
    table = Table(title="Mili Hui Fastboot ROMs"); table.add_column("#"); table.add_column("Path")
    for i, path in enumerate(rom_paths, 1): table.add_row(str(i), path)
    console.print(table)
    choice = Prompt.ask("\n[bold]👉 ROM chunein[/bold]", choices=[str(i) for i in range(1, len(rom_paths) + 1)])
    selected_path = rom_paths[int(choice) - 1]

    if selected_path.endswith(".tgz"):
        extract_dir = os.path.join(os.path.dirname(selected_path), "AGNI_TEMP")
        if os.path.exists(extract_dir): shutil.rmtree(extract_dir)
        os.makedirs(extract_dir)
        tar_command = f"pv -bpe '{selected_path}' | tar --strip-components=1 -xzf - -C '{extract_dir}/'"
        if run_command(tar_command, "Extracting ROM") != 0: console.print("[red]Extraction Fail Hua.[/red]"); return
        flash_from_folder(extract_dir)
    elif os.path.isdir(selected_path):
        flash_from_folder(selected_path)

def flash_from_folder(folder_path):
    scripts = [f for f in os.listdir(folder_path) if f.startswith('flash_all') and f.endswith('.sh')]
    if not scripts: console.print(f"[red]❌ '{folder_path}' ke andar koi 'flash_all.sh' script nahi mili.[/red]"); return
    table = Table(title="Kaunsa Prahaar Karna Hai?"); table.add_column("#"); table.add_column("Description")
    script_map = {"flash_all.sh": "Flash ROM (Data Safe/Unlock)", "flash_all_lock.sh": "[red]Flash ROM (Bootloader LOCK & Data Wipe)[/red]"}
    available_scripts = sorted([s for s in script_map.keys() if s in scripts] + [s for s in scripts if s not in script_map])
    for i, script in enumerate(available_scripts, 1): table.add_row(str(i), script_map.get(script, script))
    console.print(table)
    choice = Prompt.ask("\n[bold]👉 Script chunein[/bold]", choices=[str(i) for i in range(1, len(available_scripts) + 1)])
    selected_script = available_scripts[int(choice) - 1]
    
    console.print("\n[yellow]Nirdesh:[/yellow] Phone ko Fastboot mode mein daalein aur connect karein.")
    if Prompt.ask("\n[bold]Prahaar shuru karein?[/bold]", choices=["y", "n"]) == 'y':
        original_dir = os.getcwd(); os.chdir(folder_path)
        run_command(f"bash ./{selected_script}", "Flashing in Progress")
        os.chdir(original_dir)

def sideload_flasher():
    clear_screen(); console.print(Panel("[bold]📦 3 - Flash Zip With Sideload[/bold]", style="bold on green"))
    search_path = os.path.expanduser('~/storage/shared'); rom_paths = []
    with console.status("[green]Recovery ROMs (.zip) dhoondhe ja rahe hain...[/green]"):
        for root, dirs, files in os.walk(search_path):
            if 'Android' in dirs: dirs.remove('Android')
            for file in files:
                if file.endswith(".zip"): rom_paths.append(os.path.join(root, file))
    if not rom_paths: console.print("[red]❌ Koi bhi .zip ROM file nahi mili.[/red]"); return
    table = Table(title="Mili Hui Recovery ROMs"); table.add_column("#"); table.add_column("Path")
    for i, path in enumerate(rom_paths, 1): table.add_row(str(i), path)
    console.print(table)
    choice = Prompt.ask("\n[bold]👉 ROM chunein[/bold]", choices=[str(i) for i in range(1, len(rom_paths) + 1)])
    selected_zip = rom_paths[int(choice) - 1]
    console.print("\n[yellow]Nirdesh:[/yellow] Phone ko Recovery mode mein 'Apply update from ADB' par laayein.")
    if Prompt.ask("\n[bold]Prahaar shuru karein?[/bold]", choices=["y", "n"]) == 'y':
        run_command(f"adb sideload '{selected_zip}'", "Sideloading ZIP")

def frp_bypass():
    clear_screen(); console.print(Panel("[bold]🔑 4 - Bypass[/bold]", style="bold on #FF4500"))
    console.print("\n1. [magenta]Samsung[/magenta]\n2. [cyan]Universal (Fastboot)[/cyan]")
    choice = Prompt.ask("\n[bold]Apna raasta chunein[/bold]", choices=["1", "2"])
    if choice == '1':
        console.print(Panel("Nirdesh: Phone ko 'Emergency Call' screen par laayein aur [cyan]*#0*#[/cyan] dial karein.", title="Samsung Guide"))
        if Prompt.ask("[bold]Taiyar hain?[/bold]", choices=["y", "n"]) == "y":
            run_command("adb shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:s:1", "Attempting Samsung FRP")
    elif choice == '2':
        console.print(Panel("Nirdesh: Phone ko [cyan]Fastboot Mode[/cyan] mein daalein aur connect karein.", title="Universal Guide"))
        if Prompt.ask("[bold]Taiyar hain?[/bold]", choices=["y", "n"]) == "y":
            run_command("fastboot erase frp", "Attempting FRP Erase")

def firmware_extractor():
    clear_screen(); console.print(Panel("[bold]🔬 6 - Firmware-Content-Extractor[/bold]", style="bold on magenta"))
    if not shutil.which("payload-dumper-go"):
        console.print(Panel("[red]Galti: 'payload-dumper-go' astra nahi mila.[/red] [yellow]Kripya ise GitHub se install karein.[/yellow]")); return
    search_path = os.path.expanduser('~/storage/shared'); payload_files = []
    with console.status("[green]'payload.bin' file dhoondhi ja rahi hai...[/green]"):
        for root, _, files in os.walk(search_path):
            if 'payload.bin' in files: payload_files.append(os.path.join(root, 'payload.bin'))
    if not payload_files: console.print("[red]❌ Koi 'payload.bin' file nahi mili.[/red]"); return
    table = Table(title="Mili Hui payload.bin Files"); table.add_column("#"); table.add_column("Path")
    for i, path in enumerate(payload_files, 1): table.add_row(str(i), path)
    console.print(table)
    choice = Prompt.ask("\n[bold]👉 File chunein[/bold]", choices=[str(i) for i in range(1, len(payload_files) + 1)])
    selected_payload = payload_files[int(choice) - 1]
    output_dir = os.path.join(os.path.dirname(selected_payload), "Extracted_Firmware")
    run_command(f"payload-dumper-go -o {output_dir} {selected_payload}", "Extracting Firmware")
    console.print(f"[green]✅ Extraction poora hua! Files '{output_dir}' mein save ho gayi hain.[/green]")

def universal_tools_menu():
    clear_screen(); console.print(Panel("[bold]📱 7 - Universal Android Tools[/bold]", style="bold on yellow"))
    console.print("1. Device Information\n2. Rebooter Menu")
    choice = Prompt.ask("\nChunein", choices=["1", "2"])
    if choice == '1':
        run_command("adb devices -l", "ADB Devices")
        run_command("fastboot devices", "Fastboot Devices")
    elif choice == '2':
        c = Prompt.ask("1. Reboot System (ADB)\n2. Reboot Recovery (ADB)\n3. Reboot Bootloader (ADB)\n4. Reboot System (Fastboot)", choices=["1", "2", "3", "4"])
        if c == '1': run_command("adb reboot")
        elif c == '2': run_command("adb reboot recovery")
        elif c == '3': run_command("adb reboot bootloader")
        elif c == '4': run_command("fastboot reboot")

def main():
    check_dependencies(['adb', 'fastboot', 'pv', 'tar'])
    while True:
        clear_screen()
        ver = "2.0"
        title = f"AGNI {ver}"
        box_width = len(title) + 4
        padding = (console.width - box_width) // 2
        console.print(" " * padding + "┏" + "━" * box_width + "┓")
        console.print(" " * padding + f"┃  [bold]{title}[/bold]  ┃")
        console.print(" " * padding + "┗" + "━" * box_width + "┛")
        
        menu = {
            "1": "🔓 Unlock-Bootloader", "2": "⚡ Flash-Fastboot-ROM",
            "3": "📦 Flash-Zip-With-Sideload", "4": "🔑 Bypass",
            "5": "🔬 Firmware-Content-Extractor", "6": "📱 Universal-Tools"
        }
        
        print("\n")
        for key, value in menu.items():
            console.print(f" ━ [green]{key}[/green] {value}")
        print("\n")
        
        choice = Prompt.ask(f"Enter your [green]choice[/green]", choices=list(menu.keys()) + ["0"], default="0")

        if choice == '1': guide_unlock_bootloader()
        elif choice == '2': fastboot_flasher()
        elif choice == '3': sideload_flasher()
        elif choice == '4': frp_bypass()
        elif choice == '5': firmware_extractor()
        elif choice == '6': universal_tools_menu()
        elif choice == '0':
            console.print("\n[bold #8B0000]Agni shant ho rahi hai... Alvida, Samraat.[/bold #8B0000]"); break
        
        Prompt.ask("\n[bold yellow]...Mukhya Menu par wapas jaane ke liye Enter dabayein...[/bold yellow]")

    clear_screen()
    footer = Panel("By Emperor [bold]Sachin Solunke[/bold] & [bold]Jarvis[/bold] ❤️ | GitHub: [link=https://github.com/SachinSolunke/FRP---BYPASS]SachinSolunke/FRP---BYPASS[/link]",
                   title="[dim]Credits[/dim]", border_style="dim")
    console.print(footer)

if __name__ == "__main__":
    main()
