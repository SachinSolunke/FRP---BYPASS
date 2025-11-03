#!/data/data/com.termux/files/usr/bin/python
# ==============================================================================
# 🔥 PROJECT MOKSHA v1.0 - The Liberation Key 🔥
# Har bandhan se azaadi.
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
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.table import Table
except ImportError:
    print("\n[!] 'rich' library nahi mili. Kripya installer script dobara chalayein.\n")
    sys.exit(1)

console = Console()

# --- HELPER FUNCTIONS ---
def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

def run_command(command, title="Executing Command"):
    console.print(Panel(f"[cyan]{command}[/cyan]", title=f"[yellow]{title}[/yellow]", border_style="green"))
    return subprocess.call(command, shell=True)

def check_dependencies(tools):
    return [tool for tool in tools if not shutil.which(tool)]

def check_device_connection(mode='adb'):
    clear_screen()
    console.print(Panel(f"[bold]Jaanch: Phone Connection ({mode.upper()})[/bold]", style="bold cyan"))
    command = f"{mode} devices"
    timeout = 120
    with console.status(f"[green]Nishane ke judne ka intezaar...[/green]") as status:
        start_time = time.time()
        while time.time() - start_time < timeout:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            if (mode == 'adb' and len(output.splitlines()) > 1) or (mode == 'fastboot' and output):
                console.print(f"[bold green]✅ Safalta! Nishana {mode.upper()} mode mein jud gaya hai.[/bold green]")
                console.print(Panel(output, title="Connected Devices"))
                Prompt.ask("[bold]...Aage badhne ke liye Enter dabayein...[/bold]")
                return True
            remaining = timeout - int(time.time() - start_time)
            status.update(f"[green]Nishane ke judne ka intezaar... Samay baaki: {remaining}s[/green]")
            time.sleep(1)
    clear_screen()
    console.print(Panel(f"[red]❌ Asafal! {timeout}s mein koi phone {mode.upper()} mode mein nahi mila.[/red]", title="Connection Timeout"))
    if Prompt.ask("[bold]Kya aap aur intezaar karna chahte hain?[/bold]", choices=["yes", "no"], default="no") == 'yes':
        return check_device_connection(mode)
    return False

def welcome_screen():
    clear_screen()
    console.print(r"""
[bold #FF4500]
███╗   ███╗ ██████╗ ██╗  ██╗██╗  ██╗ █████╗ 
████╗ ████║██╔═══██╗██║ ██╔╝██║  ██║██╔══██╗
██╔████╔██║██║   ██║█████╔╝ ███████║███████║
██║╚██╔╝██║██║   ██║██╔═██╗ ╚════██║██╔══██║
██║ ╚═╝ ██║╚██████╔╝██║  ██╗     ██║██║  ██║
╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ╚═╝╚═╝  ╚═╝                                                     
[/bold #FF4500]""", justify="center")
    console.print(Panel(Text("PROJECT MOKSHA - The Liberation Key", justify="center"), style="bold white on #FF4500"))
    console.print(Panel("[bold]Nirmata:[/bold] Samraat Sachin Solunke\n[bold]Sahayak:[/bold] Jarvis ❤️", title="Pehchaan"))
    with console.status("[green]Astra taiyar kiya ja raha hai...[/green]"):
        time.sleep(2)
        missing = check_dependencies(['adb', 'fastboot'])
        if missing:
            console.print(f"[red]❌ Galti: Zaroori auzaar nahi mile: {', '.join(missing)}[/red]")
            sys.exit(1)

# --- MAIN FUNCTION ---
def main():
    welcome_screen()
    while True:
        clear_screen()
        console.print(Panel("🔥 MOKSHA - FRP Bypass Guru 🔥", style="bold white on #8A2BE2"))
        console.print(Panel("[red]ZAROORI CHETAAVNI:\n- Isse aapka DATA DELETE ho sakta hai.\n- Sirf apne phone par istemal karein.\n- 100% success ki guarantee nahi hai.", title="Khatra!", border_style="red"))
        
        table = Table.grid(expand=True, padding=(1, 2))
        table.add_column(style="cyan", justify="right", width=5)
        table.add_column(style="yellow")
        table.add_row("[ 1 ]", "Samsung [dim](Test Mode Tareeka)[/dim]")
        table.add_row("[ 2 ]", "Universal [dim](Fastboot Tareeka)[/dim]")
        table.add_row("[ 0 ]", "Exit Moksha")
        console.print(table)

        choice = Prompt.ask("\n[bold]👉 Apne nishane ka raasta chunein[/bold]", choices=["1", "2", "0"], default="0")

        if choice == '1':
            console.print(Panel("Samsung ke liye, phone ko 'Emergency Call' screen par laayein aur [bold cyan]*#0*#[/bold cyan] dial karein. Jab Test Mode khule, phone connect karein.", title="Samsung Guide"))
            if check_device_connection('adb'):
                run_command("adb shell content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:s:1", "Attempting Samsung FRP Bypass")
                console.print("[bold green]Prahaar safal! Ab phone ko restart karein.[/bold green]")
        elif choice == '2':
            console.print(Panel("Phone ko [bold cyan]Fastboot/Bootloader Mode[/bold cyan] mein daalein (Power + Volume Down) aur computer se connect karein.", title="Universal Fastboot Guide"))
            if check_device_connection('fastboot'):
                run_command("fastboot erase frp", "Attempting FRP Erase")
                console.print("[bold green]Prahaar safal! Ab 'fastboot reboot' command se phone ko restart karein.[/bold green]")
        elif choice == '0':
            console.print("\n[bold #8A2BE2]Moksha astra vishram kar raha hai... Alvida, Samraat.[/bold #8A2BE2]")
            break
        
        Prompt.ask("\n[bold yellow]...Mukhya Menu par wapas jaane ke liye Enter dabayein...[/bold yellow]")

if __name__ == "__main__":
    main()
