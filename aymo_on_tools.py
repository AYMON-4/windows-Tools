"""
╔══════════════════════════════════════════════════════╗
║           AYMO_ON Tools Menu                         ║
║           Windows System Maintenance Tool            ║
║           Requires: Python 3.x, Administrator        ║
╚══════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import ctypes
import winreg
import tempfile
import shutil
import time
from datetime import datetime


# ════════════════════════════════════════════════════════
#  CONSTANTS & CONFIG
# ════════════════════════════════════════════════════════

class Colors:
    """ANSI color codes for colored terminal output."""
    RED    = '\033[91m'
    GREEN  = '\033[92m'
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    PURPLE = '\033[95m'
    CYAN   = '\033[96m'
    WHITE  = '\033[97m'
    GRAY   = '\033[90m'
    RESET  = '\033[0m'
    BOLD   = '\033[1m'

# ASCII logo used throughout the app
LOGO = f"""{Colors.CYAN}
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║    █████╗ ██╗   ██╗███╗   ███╗ ██████╗          ██████╗ ███╗   ██╗           ║
    ║   ██╔══██╗╚██╗ ██╔╝████╗ ████║██╔═══██╗        ██╔═══██╗████╗  ██║           ║
    ║   ███████║ ╚████╔╝ ██╔████╔██║██║   ██║        ██║   ██║██╔██╗ ██║           ║
    ║   ██╔══██║  ╚██╔╝  ██║╚██╔╝██║██║   ██║        ██║   ██║██║╚██╗██║           ║
    ║   ██║  ██║   ██║   ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝██║ ╚████║           ║
    ║   ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝           ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""

# نفس الـ logo بس للـ HTML (بدون ANSI)
LOGO_HTML = """
 █████╗ ██╗   ██╗███╗   ███╗ ██████╗          ██████╗ ███╗   ██╗
██╔══██╗╚██╗ ██╔╝████╗ ████║██╔═══██╗        ██╔═══██╗████╗  ██║
███████║ ╚████╔╝ ██╔████╔██║██║   ██║        ██║   ██║██╔██╗ ██║
██╔══██║  ╚██╔╝  ██║╚██╔╝██║██║   ██║        ██║   ██║██║╚██╗██║
██║  ██║   ██║   ██║ ╚═╝ ██║╚██████╔╝███████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
"""

# CSS مشترك بين تقارير HTML (Dark Theme)
SHARED_HTML_CSS = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #e0e0e0;
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #2d2d2d 100%);
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header {
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border-radius: 15px; padding: 30px; margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            text-align: center; border: 1px solid #404040;
        }
        .logo {
            font-family: 'Courier New', monospace; font-size: 14px;
            line-height: 1.3; color: #00d4ff; margin-bottom: 20px;
            background: rgba(0, 212, 255, 0.1); padding: 15px;
            border-radius: 10px; border-left: 4px solid #00d4ff;
        }
        .report-title {
            color: #ffffff; font-size: 2.5em; margin-bottom: 10px;
            font-weight: 300; text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        .subtitle { color: #b0b0b0; font-size: 1.2em; margin-bottom: 20px; }
        .section {
            background: linear-gradient(135deg, #2d2d2d 0%, #1a1a1a 100%);
            border-radius: 15px; padding: 25px; margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            border: 1px solid #404040;
            animation: fadeIn 0.6s ease-out;
        }
        .section-title {
            color: #ffffff; font-size: 1.5em; margin-bottom: 20px;
            display: flex; align-items: center; gap: 10px;
        }
        .section-title::before { content: "▶"; color: #00d4ff; font-size: 0.8em; }
        .info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; }
        .info-item {
            background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;
            border-left: 4px solid #00d4ff; border: 1px solid #404040;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .info-item:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,212,255,0.2); }
        .info-label { font-weight: 600; color: #00d4ff; margin-bottom: 5px; font-size: 0.9em; }
        .info-value { color: #e0e0e0; word-break: break-all; font-size: 1.1em; }
        .progress-bar {
            background: #404040; border-radius: 10px; overflow: hidden;
            height: 20px; margin-top: 5px; border: 1px solid #555;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00d4ff, #0099cc);
            box-shadow: 0 0 10px rgba(0,212,255,0.3);
        }
        .table { width: 100%; border-collapse: collapse; background: rgba(255,255,255,0.05); border-radius: 8px; overflow: hidden; }
        .table th {
            background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
            color: #000; padding: 12px; text-align: left; font-weight: 600;
        }
        .table td { padding: 12px; border-bottom: 1px solid #404040; color: #e0e0e0; }
        .table tr:nth-child(even) { background: rgba(255,255,255,0.02); }
        .table tr:hover { background: rgba(0,212,255,0.1); }
        .footer { text-align: center; margin-top: 30px; padding: 20px; color: #b0b0b0; }
        .footer-logo {
            font-family: 'Courier New', monospace; font-size: 12px; line-height: 1.2;
            color: #00d4ff; margin-top: 20px; background: rgba(0,212,255,0.1);
            padding: 15px; border-radius: 8px; border: 1px solid #00d4ff;
        }
        .badge {
            display: inline-block; padding: 3px 8px; border-radius: 12px;
            font-size: 0.8em; font-weight: 600; margin-left: 10px;
        }
        .badge-success { background: #27ae60; color: white; }
        .badge-warning { background: #f39c12; color: white; }
        .badge-danger  { background: #e74c3c; color: white; }
        .badge-info    { background: #3498db; color: white; }
        .glow { text-shadow: 0 0 10px rgba(0,212,255,0.5); }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #2d2d2d; border-radius: 4px; }
        ::-webkit-scrollbar-thumb { background: #00d4ff; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #0099cc; }
    </style>
"""


# ════════════════════════════════════════════════════════
#  HELPER UTILITIES
# ════════════════════════════════════════════════════════

def is_admin():
    """Returns True if the script is running with Administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """Re-launch the script with Administrator privileges via UAC prompt."""
    set_full_screen()
    _show_admin_request_screen()
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()


def set_full_screen():
    """Maximize console window size (Windows only)."""
    try:
        os.system('mode con: cols=120 lines=9001')
    except:
        pass


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause(msg="    Press Enter to continue..."):
    """Wait for user to press Enter before returning to menu."""
    input(f"\n{Colors.GRAY}{msg}{Colors.RESET}")


def run_command(cmd, timeout=60):
    """Run a shell command and return (stdout, stderr, returncode)."""
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.stdout, result.stderr, result.returncode


def clean_folder(folder_path):
    """
    Delete all files inside folder_path recursively.
    Returns the number of files successfully removed.
    """
    removed = 0
    if os.path.exists(folder_path):
        for root, _, files in os.walk(folder_path):
            for f in files:
                try:
                    os.remove(os.path.join(root, f))
                    removed += 1
                except:
                    pass
    return removed


# ════════════════════════════════════════════════════════
#  DISPLAY / UI
# ════════════════════════════════════════════════════════

def _show_admin_request_screen():
    """Show the UAC request screen before relaunching as admin."""
    clear_screen()
    print(LOGO)
    print(f"\n{Colors.YELLOW}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                🔐 ADMINISTRATOR ACCESS REQUIRED                              ║")
    print(f"    ║                                                                              ║")
    print(f"    ║  This tool needs Administrator privileges to perform:                        ║")
    print(f"    ║  • 🛡️  System file checks (SFC/DISM)                                         ║")
    print(f"    ║  • 💾 Disk maintenance and repairs                                           ║")
    print(f"    ║  • 🧹 Cleaning system folders                                                ║")
    print(f"    ║  • ⚙️  Managing Windows services                                             ║")
    print(f"    ║  • 🔒 Accessing protected system areas                                       ║")
    print(f"    ║                                                                              ║")
    print(f"    ║  Please click 'Yes' in the UAC prompt to continue...                         ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"\n{Colors.GRAY}    Waiting for administrator approval...{Colors.RESET}")
    time.sleep(3)


def print_banner():
    """Print the AYMO_ON banner with a welcome message."""
    print(LOGO)
    print(f"{Colors.YELLOW}    👋 Welcome, {os.getenv('USERNAME')}!{Colors.RESET}")
    print(f"{Colors.GRAY}    " + "═" * 78 + f"{Colors.RESET}")
    print()


def wait_for_exit():
    """Show a notice that an external app was opened, then wait for Enter."""
    print(f"\n{Colors.YELLOW}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                           ⚠️  APPLICATION OPENED                              ║")
    print(f"    ║  • Close the opened application/tool                                         ║")
    print(f"    ║  • Then press Enter to return to the main menu                               ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    pause()


def show_menu():
    """Render the full two-column main menu."""
    clear_screen()
    print_banner()

    def pad_text(text, target_width):
        """Account for emoji rendering width differences on Windows."""
        compensation = text.count('\ufe0f')
        for emoji in ['⚡', '🔄']:
            if emoji in text:
                compensation += 1
        return f"{text:<{target_width + compensation}}"

    # ── Column 1: Open Tools ──────────────────────────────
    tools = [
        ("1.  📊 DXDIAG",                Colors.YELLOW),
        ("2.  📅 Event Viewer",           Colors.BLUE),
        ("3.  📈 Reliability Monitor",    Colors.GREEN),
        ("4.  📊 Resource Monitor",       Colors.YELLOW),
        ("5.  🔒 Windows Security",       Colors.RED),
        ("6.  🖥️  Task Manager",          Colors.CYAN),
        ("7.  🗂️  System Information",    Colors.WHITE),
        ("8.  🛠️  Device Manager",        Colors.GRAY),
        ("9.  📊 Performance Monitor",    Colors.YELLOW),
        ("10. 🛡️  Group Policy Editor",   Colors.PURPLE),
        ("11. 📜 Registry Editor",        Colors.BLUE),
        ("12. 📁 Startup Folder",         Colors.CYAN),
        ("13. 📁 AppData Folder",         Colors.GREEN),
        ("14. 📁 ProgramData Folder",     Colors.BLUE),
        ("15. 🌐 Network Adapters",       Colors.CYAN),
    ]

    # ── Column 2 (top): Run Diagnostics ──────────────────
    diagnostics = [
        ("16. 🧠  Windows Memory Diagnostic",  Colors.PURPLE),
        ("17. 🛡️  System File Checker (SFC)",  Colors.RED),
        ("18. 🔍  DISM Health Check",           Colors.YELLOW),
        ("19. 💽  Disk Check (CHKDSK)",         Colors.BLUE),
        ("20. 🛠️  Full Maintenance (SFC+DISM)", Colors.GRAY),
    ]

    # ── Column 2 (bottom): Clear Temp Files ──────────────
    temp_files = [
        ("21. 🧹  User Temp Folder",          Colors.CYAN),
        ("22. 🧹  Windows Temp Folder",        Colors.CYAN),
        ("23. 🧹  Windows Update Cache",       Colors.CYAN),
        ("24. 🧹  Prefetch Files",             Colors.CYAN),
        ("25. 🧹 CLEAN ALL TEMPORARY FILES",   Colors.RED),
    ]

    # Build left column lines
    left = []
    left.append(f"{Colors.CYAN}    ┌────────────── 🚀 OPEN TOOLS ─────────────────┐{Colors.RESET}")
    left.append(f"{Colors.CYAN}    │{Colors.RESET}                                              {Colors.CYAN}│{Colors.RESET}")
    for name, color in tools:
        left.append(f"{Colors.CYAN}    │{Colors.RESET}  {color}{pad_text(name, 42)}{Colors.RESET} {Colors.CYAN}│{Colors.RESET}")
    left.append(f"{Colors.CYAN}    │{Colors.RESET}                                              {Colors.CYAN}│{Colors.RESET}")
    left.append(f"{Colors.CYAN}    └──────────────────────────────────────────────┘{Colors.RESET}")

    # Build right column lines
    right = []
    right.append(f"{Colors.GREEN}┌──────────── ⚡  RUN DIAGNOSTICS ─────────────┐{Colors.RESET}")
    right.append(f"{Colors.GREEN}│{Colors.RESET}                                              {Colors.GREEN}│{Colors.RESET}")
    for name, color in diagnostics:
        right.append(f"{Colors.GREEN}│{Colors.RESET}  {color}{pad_text(name, 42)}{Colors.RESET} {Colors.GREEN}│{Colors.RESET}")
    right.append(f"{Colors.GREEN}│{Colors.RESET}                                              {Colors.GREEN}│{Colors.RESET}")
    right.append(f"{Colors.GREEN}└──────────────────────────────────────────────┘{Colors.RESET}")
    right.append(" " * 48)
    right.append(f"{Colors.YELLOW}┌────────── 🧹 CLEAR TEMPORARY FILES ──────────┐{Colors.RESET}")
    right.append(f"{Colors.YELLOW}│{Colors.RESET}                                              {Colors.YELLOW}│{Colors.RESET}")
    for name, color in temp_files:
        right.append(f"{Colors.YELLOW}│{Colors.RESET} {color}{pad_text(name, 44)}{Colors.RESET}{Colors.YELLOW}│{Colors.RESET}")
    right.append(f"{Colors.YELLOW}│{Colors.RESET}                                              {Colors.YELLOW}│{Colors.RESET}")
    right.append(f"{Colors.YELLOW}└──────────────────────────────────────────────┘{Colors.RESET}")

    # Merge columns side-by-side
    max_lines = max(len(left), len(right))
    left  += [" " * 52] * (max_lines - len(left))
    right += [""] * (max_lines - len(right))
    for l, r in zip(left, right):
        print(f"{l}    {r}")

    print()

    # ── Special Tools ─────────────────────────────────────
    print(f"{Colors.PURPLE}    ┌───────────── 🛠️  SPECIAL TOOLS ──────────────┐{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}                                              {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.GRAY}{'26. ⚙️  Set PowerShell Execution Policy':<43}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.GREEN}{'27. ⚡  Windows Activation':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.BLUE}{'28. 🗄️  Create God Mode Folder':<43}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.RED}{'29. 🚫  Disable Suggested Apps':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.YELLOW}{'30. 🔄  Restart and Enter BIOS':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.GREEN}{'31. 🔋  Generate Battery Report':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.CYAN}{'32. 💾  Generate System Report':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}  {Colors.PURPLE}{'33. 📊  Installed Programs Report':<42}{Colors.RESET} {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    │{Colors.RESET}                                              {Colors.PURPLE}│{Colors.RESET}")
    print(f"{Colors.PURPLE}    └──────────────────────────────────────────────┘{Colors.RESET}")
    print()
    # ── Exit ──────────────────────────────────────────────
    print(f"{Colors.RED}    ┌────────────────── ❌ EXIT ───────────────────┐{Colors.RESET}")
    print(f"{Colors.RED}    │{Colors.RESET}                                              {Colors.RED}│{Colors.RESET}")
    print(f"{Colors.RED}    │{Colors.RESET}  {Colors.RED}34. ❌ Exit{Colors.RESET}                                 {Colors.RED}│{Colors.RESET}")
    print(f"{Colors.RED}    │{Colors.RESET}                                              {Colors.RED}│{Colors.RESET}")
    print(f"{Colors.RED}    └──────────────────────────────────────────────┘{Colors.RESET}")
    print()


# ════════════════════════════════════════════════════════
#  TEMP FILE CLEANING
# ════════════════════════════════════════════════════════

def _toggle_update_services(action):
    """Start or stop Windows Update related services. action = 'stop' | 'start'."""
    for svc in ["wuauserv", "bits", "cryptsvc"]:
        subprocess.run(["net", action, svc], capture_output=True)


def clean_user_temp():
    """Remove all files from the current user's TEMP folder."""
    removed = clean_folder(tempfile.gettempdir())
    print(f"{Colors.GREEN}    ✓ User Temp cleared — {removed} files removed.{Colors.RESET}")
    return removed


def clean_windows_temp():
    """Remove all files from C:\\Windows\\Temp."""
    removed = clean_folder("C:\\Windows\\Temp")
    print(f"{Colors.GREEN}    ✓ Windows Temp cleared — {removed} files removed.{Colors.RESET}")
    return removed


def clean_update_cache():
    """Clear the Windows Update cache (SoftwareDistribution folder)."""
    path = "C:\\Windows\\SoftwareDistribution"
    try:
        _toggle_update_services("stop")
        if os.path.exists(path):
            shutil.rmtree(path)
            os.makedirs(path)
        _toggle_update_services("start")
        print(f"{Colors.GREEN}    ✓ Windows Update Cache cleared.{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}    ✗ Failed to clear Update Cache: {e}{Colors.RESET}")


def clean_prefetch():
    """Remove prefetch files from C:\\Windows\\Prefetch."""
    removed = clean_folder("C:\\Windows\\Prefetch")
    print(f"{Colors.GREEN}    ✓ Prefetch cleared — {removed} files removed.{Colors.RESET}")
    return removed


def clean_all_temp_files():
    """Run all four cleaning operations in sequence and show a summary."""
    clear_screen()
    print(f"{Colors.RED}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                     🧹🔥 CLEANING ALL TEMPORARY FILES                       ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    print(f"{Colors.YELLOW}    Please make sure all programs are closed before continuing.{Colors.RESET}")
    pause("    Press Enter to start cleaning...")

    total = 0
    print(f"\n{Colors.CYAN}    [1/4] Cleaning User Temp...{Colors.RESET}")
    total += clean_user_temp()

    print(f"\n{Colors.CYAN}    [2/4] Cleaning Windows Temp...{Colors.RESET}")
    total += clean_windows_temp()

    print(f"\n{Colors.CYAN}    [3/4] Clearing Windows Update Cache...{Colors.RESET}")
    clean_update_cache()

    print(f"\n{Colors.CYAN}    [4/4] Clearing Prefetch Files...{Colors.RESET}")
    total += clean_prefetch()

    print(f"\n{Colors.GREEN}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                           🎉 CLEANUP COMPLETED!                               ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"\n{Colors.CYAN}    💾 Total files removed: {total}{Colors.RESET}")
    pause()


# ════════════════════════════════════════════════════════
#  HTML REPORT HELPERS
# ════════════════════════════════════════════════════════

def _html_header(title, subtitle):
    """Return the standard HTML header block used in all reports."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AYMO_ON Tools</title>
    {SHARED_HTML_CSS}
</head>
<body>
<div class="container">
    <div class="header">
        <div class="logo"><pre>{LOGO_HTML}</pre></div>
        <h1 class="report-title glow">{title}</h1>
        <p class="subtitle">{subtitle}</p>
    </div>
"""


def _html_footer():
    """Return the standard HTML footer block used in all reports."""
    return f"""
    <div class="footer">
        <p>Report generated by <strong>AYMO_ON Tools Menu</strong></p>
        <div class="footer-logo"><pre>{LOGO_HTML}</pre></div>
    </div>
</div>
</body>
</html>"""


# ════════════════════════════════════════════════════════
#  BATTERY REPORT
# ════════════════════════════════════════════════════════

def _enhance_battery_report(path):
    """
    Inject Dark Theme CSS and AYMO_ON header/footer into
    the battery report generated by powercfg.
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    extra_css = f"""
    <style>
        body {{ background: linear-gradient(135deg, #0f0f0f, #1a1a1a, #2d2d2d) !important; color: #e0e0e0 !important; }}
        h1,h2,h3,h4,h5,h6 {{ color: #00d4ff !important; }}
        table {{ background: rgba(255,255,255,0.05) !important; border: 1px solid #404040 !important; }}
        th {{ background: linear-gradient(135deg, #00d4ff, #0099cc) !important; color: #000 !important; }}
        td {{ color: #e0e0e0 !important; border-bottom: 1px solid #404040 !important; }}
        tr:hover {{ background: rgba(0,212,255,0.1) !important; }}
    </style>"""

    header_block = f"""
    <div style="background:#2d2d2d;border-radius:15px;padding:30px;margin-bottom:20px;text-align:center;border:1px solid #404040;">
        <div style="font-family:monospace;color:#00d4ff;background:rgba(0,212,255,0.1);padding:15px;border-radius:10px;">
            <pre>{LOGO_HTML}</pre>
        </div>
        <h1 style="color:#fff;font-size:2em;">🔋 Battery Health Report</h1>
        <p style="color:#b0b0b0;">Generated by AYMO_ON Tools • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>"""

    footer_block = f"""
    <div style="text-align:center;margin-top:30px;color:#b0b0b0;border-top:1px solid #404040;padding-top:20px;">
        <p>Report generated by <strong>AYMO_ON Tools Menu</strong></p>
    </div>"""

    content = content.replace('</head>', extra_css + '</head>')
    content = content.replace('<body>', '<body>' + header_block)
    content = content.replace('</body>', footer_block + '</body>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def generate_battery_report():
    """Generate a styled battery report using powercfg and open it."""
    clear_screen()
    print(f"{Colors.GREEN}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                               🔋 BATTERY REPORT                                 ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()

    path = os.path.join(os.path.expanduser("~"), "Desktop", "battery-report.html")
    subprocess.run(["powercfg", "/batteryreport", "/output", path], capture_output=True)

    print(f"{Colors.CYAN}    Enhancing report with Dark Theme...{Colors.RESET}")
    try:
        _enhance_battery_report(path)
        print(f"{Colors.GREEN}    ✓ Report enhanced and saved to Desktop!{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.YELLOW}    ⚠ Basic report generated ({e}){Colors.RESET}")

    subprocess.Popen(["start", "", path], shell=True)
    pause()


# ════════════════════════════════════════════════════════
#  SYSTEM REPORT
# ════════════════════════════════════════════════════════

def _ensure_psutil():
    """Import psutil, installing it if missing. Returns the module or None."""
    try:
        import psutil
        return psutil
    except ImportError:
        print(f"{Colors.YELLOW}    psutil not found — installing...{Colors.RESET}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psutil"],
                           check=True, capture_output=True)
            import psutil
            return psutil
        except Exception:
            print(f"{Colors.RED}    ✗ Could not install psutil. Run: pip install psutil{Colors.RESET}")
            return None


def generate_system_report():
    """Build a detailed HTML system report and open it in the browser."""
    clear_screen()
    print(f"{Colors.CYAN}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                           💾 GENERATING SYSTEM REPORT                            ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()

    import platform, socket
    psutil = _ensure_psutil()
    if not psutil:
        pause()
        return

    print(f"{Colors.YELLOW}    Collecting system information...{Colors.RESET}")
    path = os.path.join(os.path.expanduser("~"), "Desktop", "Complete_System_Report.html")

    try:
        with open(path, 'w', encoding='utf-8') as f:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(_html_header("💾 Complete System Report", f"Generated on: {ts}"))

            # ── Basic Info ────────────────────────────────
            f.write(f"""
            <div class="section">
                <h2 class="section-title">🔰 Basic System Information</h2>
                <div class="info-grid">
                    <div class="info-item"><div class="info-label">Computer Name</div>
                        <div class="info-value">{socket.gethostname()}</div></div>
                    <div class="info-item"><div class="info-label">Operating System</div>
                        <div class="info-value">{platform.system()} {platform.release()}</div></div>
                    <div class="info-item"><div class="info-label">OS Version</div>
                        <div class="info-value">{platform.version()}</div></div>
                    <div class="info-item"><div class="info-label">Architecture</div>
                        <div class="info-value">{platform.architecture()[0]}</div></div>
                    <div class="info-item"><div class="info-label">Processor</div>
                        <div class="info-value">{platform.processor()}</div></div>
                    <div class="info-item"><div class="info-label">Last Boot</div>
                        <div class="info-value">{datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}</div></div>
                </div>
            </div>""")

            # ── CPU & Memory ──────────────────────────────
            cpu_pct = psutil.cpu_percent(interval=1)
            mem     = psutil.virtual_memory()
            freq_str = ""
            try:
                freq = psutil.cpu_freq()
                if freq:
                    freq_str = f"""<div class="info-item"><div class="info-label">Current Frequency</div>
                        <div class="info-value">{freq.current:.2f} MHz</div></div>"""
            except:
                pass

            f.write(f"""
            <div class="section">
                <h2 class="section-title">🚀 Processor &amp; Memory</h2>
                <div class="info-grid">
                    <div class="info-item"><div class="info-label">Physical Cores</div>
                        <div class="info-value">{psutil.cpu_count(logical=False)}</div></div>
                    <div class="info-item"><div class="info-label">Logical Cores</div>
                        <div class="info-value">{psutil.cpu_count(logical=True)}</div></div>
                    {freq_str}
                    <div class="info-item"><div class="info-label">CPU Usage</div>
                        <div class="info-value">{cpu_pct}%</div>
                        <div class="progress-bar"><div class="progress-fill" style="width:{cpu_pct}%"></div></div></div>
                    <div class="info-item"><div class="info-label">Total RAM</div>
                        <div class="info-value">{mem.total/(1024**3):.2f} GB</div></div>
                    <div class="info-item"><div class="info-label">Available RAM</div>
                        <div class="info-value">{mem.available/(1024**3):.2f} GB</div></div>
                    <div class="info-item"><div class="info-label">RAM Usage</div>
                        <div class="info-value">{mem.percent}%</div>
                        <div class="progress-bar"><div class="progress-fill" style="width:{mem.percent}%"></div></div></div>
                </div>
            </div>""")

            # ── Disk Info ─────────────────────────────────
            f.write("""
            <div class="section">
                <h2 class="section-title">💾 Disk Information</h2>
                <table class="table">
                    <thead><tr><th>Drive</th><th>FS</th><th>Total</th><th>Used</th><th>Free</th><th>Usage</th></tr></thead>
                    <tbody>""")
            for p in psutil.disk_partitions():
                try:
                    u = psutil.disk_usage(p.mountpoint)
                    badge = "badge-success" if u.percent < 70 else "badge-warning" if u.percent < 90 else "badge-danger"
                    f.write(f"""<tr>
                        <td><strong>{p.device}</strong></td><td>{p.fstype}</td>
                        <td>{u.total/(1024**3):.2f} GB</td><td>{u.used/(1024**3):.2f} GB</td>
                        <td>{u.free/(1024**3):.2f} GB</td>
                        <td>{u.percent}% <span class="badge {badge}">{u.percent}%</span></td>
                    </tr>""")
                except (PermissionError, OSError):
                    continue
            f.write("</tbody></table></div>")

            # ── Network Info ──────────────────────────────
            f.write("""<div class="section"><h2 class="section-title">🌐 Network Information</h2><div class="info-grid">""")
            try:
                stats = psutil.net_if_stats()
                for name, addrs in psutil.net_if_addrs().items():
                    up     = name in stats and stats[name].isup
                    badge  = "badge-success" if up else "badge-danger"
                    status = "Up" if up else "Down"
                    addr_lines = "".join(
                        f'<div class="info-value"><strong>{a.family.name}:</strong> {a.address}</div>'
                        for a in addrs
                    )
                    f.write(f"""<div class="info-item">
                        <div class="info-label">{name} <span class="badge {badge}">{status}</span></div>
                        {addr_lines}</div>""")
            except Exception as e:
                f.write(f'<div class="info-item"><div class="info-label">Error</div>'
                        f'<div class="info-value">{e}</div></div>')
            f.write("</div></div>")

            # ── systeminfo command output ─────────────────
            f.write("""<div class="section"><h2 class="section-title">📋 SYSTEMINFO Output</h2>
                <div style="background:#1a1a1a;color:#00ff88;padding:15px;border-radius:8px;
                            font-family:'Courier New',monospace;font-size:12px;line-height:1.4;
                            max-height:400px;overflow-y:auto;white-space:pre-wrap;border:1px solid #404040;">""")
            try:
                out, _, rc = run_command(["systeminfo"], timeout=30)
                f.write("\n".join(l.strip() for l in out.splitlines() if l.strip()) if rc == 0
                        else "systeminfo command failed.")
            except subprocess.TimeoutExpired:
                f.write("systeminfo timed out after 30 seconds.")
            f.write("</div></div>")

            f.write(_html_footer())

        print(f"{Colors.GREEN}    ✓ Report saved → {path}{Colors.RESET}")
        subprocess.Popen(["start", "", path], shell=True)

    except Exception as e:
        import traceback
        print(f"{Colors.RED}    ✗ Error: {e}\n{traceback.format_exc()}{Colors.RESET}")

    pause()


# ════════════════════════════════════════════════════════
#  INSTALLED PROGRAMS REPORT
# ════════════════════════════════════════════════════════

def _get_installed_programs():
    """
    Read installed programs from the Windows registry.
    Returns a list of dicts sorted alphabetically by name.
    """
    programs = []
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER,  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]

    def _read_value(key, name):
        try:
            return winreg.QueryValueEx(key, name)[0]
        except FileNotFoundError:
            return "N/A"

    for hive, path in reg_paths:
        try:
            with winreg.OpenKey(hive, path) as key:
                i = 0
                while True:
                    try:
                        sub_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_name) as sub:
                            name = _read_value(sub, 'DisplayName')
                            if name != "N/A":
                                programs.append({
                                    'name':             name,
                                    'version':          _read_value(sub, 'DisplayVersion'),
                                    'publisher':        _read_value(sub, 'Publisher'),
                                    'install_date':     _read_value(sub, 'InstallDate'),
                                    'install_location': _read_value(sub, 'InstallLocation'),
                                })
                        i += 1
                    except WindowsError:
                        break
        except FileNotFoundError:
            continue

    programs.sort(key=lambda x: x['name'].lower())
    return programs


def generate_installed_programs_report():
    """Build an interactive HTML report of all installed programs."""
    clear_screen()
    print(f"{Colors.PURPLE}    ╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"    ║                         📊 INSTALLED PROGRAMS REPORT                           ║")
    print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    print(f"{Colors.YELLOW}    Collecting installed programs...{Colors.RESET}")

    try:
        programs = _get_installed_programs()
        if not programs:
            print(f"{Colors.RED}    ✗ No programs found in registry.{Colors.RESET}")
            pause()
            return

        path = os.path.join(os.path.expanduser("~"), "Desktop", "Installed_Programs_Report.html")
        ts   = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with_pub  = sum(1 for p in programs if p['publisher']    != 'N/A')
        with_ver  = sum(1 for p in programs if p['version']      != 'N/A')
        with_date = sum(1 for p in programs if p['install_date'] != 'N/A')

        with open(path, 'w', encoding='utf-8') as f:
            # Wider container for the programs table
            header = _html_header("📊 Installed Programs Report", f"Generated on: {ts}")
            header = header.replace("max-width: 1200px", "max-width: 1400px")
            f.write(header)

            # Stats cards
            f.write(f"""
            <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin-bottom:20px;">
                {"".join(f'<div style="background:linear-gradient(135deg,#2d2d2d,#1a1a1a);padding:20px;border-radius:10px;text-align:center;border:1px solid #404040;"><div style="font-size:2em;font-weight:bold;color:#00d4ff;">{n}</div><div style="color:#b0b0b0;font-size:.9em;">{label}</div></div>'
                for n, label in [(len(programs),"Total Programs"),(with_pub,"With Publisher"),(with_ver,"With Version"),(with_date,"With Install Date")])}
            </div>""")

            # Search box
            f.write("""<input type="text" placeholder="🔍 Search programs..."
                onkeyup="searchPrograms()"
                style="background:rgba(255,255,255,.05);border:1px solid #404040;border-radius:25px;
                       padding:12px 20px;color:#e0e0e0;font-size:1em;width:100%;margin-bottom:20px;">""")

            # Table
            f.write("""
            <div style="background:linear-gradient(135deg,#2d2d2d,#1a1a1a);border-radius:15px;padding:25px;border:1px solid #404040;">
                <table class="table" id="programsTable">
                    <thead><tr>
                        <th onclick="sortTable(0)">Program Name ▼</th>
                        <th onclick="sortTable(1)">Version ▼</th>
                        <th onclick="sortTable(2)">Publisher ▼</th>
                        <th onclick="sortTable(3)">Install Date ▼</th>
                        <th onclick="sortTable(4)">Install Path ▼</th>
                    </tr></thead>
                    <tbody>""")

            for p in programs:
                f.write(f"""<tr>
                    <td style="font-weight:600;color:#fff;">{p['name']}</td>
                    <td style="color:#00ff88;font-family:monospace;">{p['version']}</td>
                    <td style="color:#ffaa00;">{p['publisher']}</td>
                    <td style="color:#b0b0b0;font-size:.9em;">{p['install_date']}</td>
                    <td style="color:#8888ff;font-size:.85em;font-family:monospace;max-width:200px;
                               overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
                        title="{p['install_location']}">{p['install_location']}</td>
                </tr>""")

            f.write("</tbody></table></div>")
            f.write(_html_footer())

            # JavaScript for search & sort
            f.write("""
            <script>
            function searchPrograms() {
                const filter = document.querySelector('input').value.toLowerCase();
                document.querySelectorAll('#programsTable tbody tr').forEach(row => {
                    row.style.display = row.cells[0].textContent.toLowerCase().includes(filter) ? '' : 'none';
                });
            }
            function sortTable(col) {
                const tbody = document.querySelector('#programsTable tbody');
                const rows  = Array.from(tbody.rows);
                const asc   = tbody.dataset.sort != col + 'a';
                tbody.dataset.sort = asc ? col + 'a' : col + 'd';
                rows.sort((a, b) => {
                    const av = a.cells[col].textContent, bv = b.cells[col].textContent;
                    return asc ? av.localeCompare(bv,undefined,{numeric:true,sensitivity:'base'})
                               : bv.localeCompare(av,undefined,{numeric:true,sensitivity:'base'});
                });
                rows.forEach(r => tbody.appendChild(r));
            }
            </script>""")

        print(f"{Colors.GREEN}    ✓ Report saved → {path}{Colors.RESET}")
        print(f"{Colors.CYAN}    Found {len(programs)} programs.{Colors.RESET}")
        subprocess.Popen(["start", "", path], shell=True)

    except Exception as e:
        import traceback
        print(f"{Colors.RED}    ✗ Error: {e}\n{traceback.format_exc()}{Colors.RESET}")

    pause()


# ════════════════════════════════════════════════════════
#  MENU ACTION DISPATCHER
# ════════════════════════════════════════════════════════

def execute_choice(choice):
    """Map user menu input to the corresponding action."""

    # ── Open Tools (1–15) ─────────────────────────────────
    OPEN_TOOLS = {
        "1":  (["dxdiag"],                                       "DXDIAG",             Colors.YELLOW),
        "2":  (["mmc.exe", "eventvwr.msc"],                      "Event Viewer",        Colors.BLUE),
        "3":  (["perfmon.exe", "/rel"],                          "Reliability Monitor", Colors.GREEN),
        "4":  (["resmon.exe"],                                   "Resource Monitor",    Colors.YELLOW),
        "5":  (None,                                             "Windows Security",    Colors.RED),  # special
        "6":  (["taskmgr.exe"],                                  "Task Manager",        Colors.CYAN),
        "7":  (["msinfo32.exe"],                                 "System Information",  Colors.WHITE),
        "8":  (["mmc.exe", "devmgmt.msc"],                       "Device Manager",      Colors.GRAY),
        "9":  (["perfmon.exe"],                                  "Performance Monitor", Colors.YELLOW),
        "10": (["gpedit.msc"],                                   "Group Policy Editor", Colors.PURPLE),
        "11": (["regedit.exe"],                                  "Registry Editor",     Colors.BLUE),
        "15": (["control", "ncpa.cpl"],                          "Network Adapters",    Colors.CYAN),
    }

    try:
        if choice in OPEN_TOOLS:
            cmd, label, color = OPEN_TOOLS[choice]
            print(f"{color}    Opening {label}...{Colors.RESET}")
            if choice == "5":
                subprocess.Popen(["start", "windowsdefender:"], shell=True)
            elif choice == "10":
                try:
                    subprocess.Popen(cmd)
                except Exception:
                    subprocess.Popen(["mmc.exe", "gpedit.msc"])
            else:
                subprocess.Popen(cmd)
            wait_for_exit()

        elif choice == "12":
            startup = os.path.join(os.getenv('APPDATA'),
                                   'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            print(f"{Colors.CYAN}    Opening Startup Folder...{Colors.RESET}")
            subprocess.Popen(["explorer", startup])
            wait_for_exit()

        elif choice == "13":
            print(f"{Colors.GREEN}    Opening AppData Folder...{Colors.RESET}")
            subprocess.Popen(["explorer", os.getenv('APPDATA')])
            wait_for_exit()

        elif choice == "14":
            print(f"{Colors.BLUE}    Opening ProgramData Folder...{Colors.RESET}")
            subprocess.Popen(["explorer", os.getenv('ProgramData')])
            wait_for_exit()

        # ── Diagnostics (16–20) ───────────────────────────
        elif choice == "16":
            print(f"{Colors.PURPLE}    Opening Windows Memory Diagnostic...{Colors.RESET}")
            subprocess.Popen(["mdsched.exe"])
            wait_for_exit()

        elif choice == "17":
            print(f"{Colors.RED}    Running SFC — this may take several minutes...{Colors.RESET}")
            out, err, _ = run_command(["sfc", "/scannow"], timeout=600)
            print(f"\n{Colors.CYAN}    Results:{Colors.RESET}\n{out}")
            if err:
                print(f"{Colors.RED}    Errors: {err}{Colors.RESET}")
            pause()

        elif choice == "18":
            print(f"{Colors.YELLOW}    Running DISM Health Check...{Colors.RESET}")
            out, err, _ = run_command(
                ["dism", "/online", "/cleanup-image", "/checkhealth"], timeout=300)
            print(f"\n{Colors.CYAN}    Results:{Colors.RESET}\n{out}")
            if err:
                print(f"{Colors.RED}    Errors: {err}{Colors.RESET}")
            pause()

        elif choice == "19":
            print(f"{Colors.BLUE}    Scheduling CHKDSK on next reboot...{Colors.RESET}")
            out, err, _ = run_command(["chkdsk", "C:", "/f"])
            print(f"\n{Colors.CYAN}    Results:{Colors.RESET}\n{out}")
            if err:
                print(f"{Colors.RED}    Errors: {err}{Colors.RESET}")
            pause()

        elif choice == "20":
            clear_screen()
            print(f"{Colors.GRAY}    Running Full Maintenance (SFC + DISM)...{Colors.RESET}")
            print(f"\n{Colors.YELLOW}    [1/2] Running SFC...{Colors.RESET}")
            sfc_out, _, _ = run_command(["sfc", "/scannow"], timeout=600)
            print(sfc_out)
            print(f"\n{Colors.YELLOW}    [2/2] Running DISM RestoreHealth...{Colors.RESET}")
            dism_out, _, _ = run_command(
                ["dism", "/online", "/cleanup-image", "/restorehealth"], timeout=600)
            print(dism_out)
            pause()

        # ── Temp File Cleaning (21–25) ────────────────────
        elif choice == "21":
            clean_user_temp()
            pause()

        elif choice == "22":
            clean_windows_temp()
            pause()

        elif choice == "23":
            print(f"{Colors.CYAN}    Clearing Windows Update Cache...{Colors.RESET}")
            clean_update_cache()
            pause()

        elif choice == "24":
            print(f"{Colors.CYAN}    Clearing Prefetch Files...{Colors.RESET}")
            clean_prefetch()
            pause()

        elif choice == "25":
            clean_all_temp_files()

        # ── Special Tools (26–33) ─────────────────────────
        elif choice == "26":
            print(f"{Colors.GRAY}    Setting PowerShell Execution Policy to RemoteSigned...{Colors.RESET}")
            subprocess.run(
                ["powershell", "-Command",
                 "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"],
                capture_output=True)
            print(f"{Colors.GREEN}    ✓ Execution Policy updated.{Colors.RESET}")
            pause()

        elif choice == "27":
            print(f"{Colors.GREEN}    Launching Windows Activation script...{Colors.RESET}")
            subprocess.Popen([
                "powershell", "-Command",
                "Start-Process powershell -Verb RunAs -ArgumentList "
                "'-Command irm https://get.activated.win | iex'"
            ])
            wait_for_exit()

        elif choice == "28":
            god_path = os.path.join(os.path.expanduser("~"), "Desktop",
                                    "GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}")
            os.makedirs(god_path, exist_ok=True)
            print(f"{Colors.GREEN}    ✓ God Mode folder created on Desktop!{Colors.RESET}")
            pause()

        elif choice == "29":
            print(f"{Colors.RED}    Disabling Suggested Apps in Start Menu...{Colors.RESET}")
            try:
                key_path = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    winreg.SetValueEx(key, "SubscribedContent-338389Enabled", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(key, "SubscribedContent-338388Enabled", 0, winreg.REG_DWORD, 0)
                print(f"{Colors.GREEN}    ✓ Suggested apps disabled.{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}    ✗ Error: {e}{Colors.RESET}")
            pause()

        elif choice == "30":
            print(f"{Colors.YELLOW}    Restarting to BIOS/UEFI in 5 seconds...{Colors.RESET}")
            time.sleep(5)
            subprocess.run(["shutdown", "/r", "/fw", "/t", "0"])

        elif choice == "31":
            generate_battery_report()

        elif choice == "32":
            generate_system_report()

        elif choice == "33":
            generate_installed_programs_report()

        # ── Exit (34) ─────────────────────────────────────
        elif choice == "34":
            clear_screen()
            print(LOGO)
            print(f"{Colors.CYAN}    ╔══════════════════════════════════════════════════════════════════════════════╗")
            print(f"    ║                  👋 GOODBYE! THANK YOU FOR USING AYMO_ON TOOLS                  ║")
            print(f"    ╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")
            time.sleep(2)
            sys.exit()

        else:
            print(f"{Colors.RED}    [!] Invalid choice. Please enter a number between 1 and 34.{Colors.RESET}")
            pause()

    except Exception as e:
        print(f"{Colors.RED}    Unexpected error: {e}{Colors.RESET}")
        pause()


# ════════════════════════════════════════════════════════
#  ENTRY POINT
# ════════════════════════════════════════════════════════

def main():
    """Initialise console settings and run the main menu loop."""
    # Enable ANSI escape codes on Windows
    if os.name == 'nt':
        os.system('')
        try:
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7)
        except:
            pass

    set_full_screen()

    if not is_admin():
        run_as_admin()

    os.system('title AYMO_ON Tools Menu — Administrator Mode')

    while True:
        show_menu()
        choice = input(f"{Colors.YELLOW}    Enter your choice: {Colors.RESET}").strip()
        execute_choice(choice)


if __name__ == "__main__":
    main()
