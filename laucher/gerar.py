"""Execute com Python + PyInstaller no sistema de destino."""
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
windows = sys.platform == "win32"
if sys.platform not in ("linux", "win32"):
    raise SystemExit("Geração disponível para Linux ou Windows.")
output = ROOT / "laucher" / ("windows" if windows else "linux")
command = [
    sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
    "--name", "BlockLab", "--paths", str(ROOT),
    "--distpath", str(output),
    "--workpath", str(ROOT / "laucher" / "build" / platform.system()),
    "--specpath", str(ROOT / "laucher" / "build"),
]
if windows:
    command.append("--windowed")
command.append(str(ROOT / "laucher" / "entrada.py"))
subprocess.run(command, check=True, cwd=ROOT)
print(f"Executável gerado em {output}")
