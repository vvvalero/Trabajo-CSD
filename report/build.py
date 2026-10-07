"""Compila la memoria a PDF (Windows / macOS / Linux). Requiere latexmk.

  python report/build.py            genera report/memoria.pdf
  python report/build.py --clean    borra lo generado
En macOS usar python3.
"""
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def main(argv):
    if shutil.which("latexmk") is None:
        sys.exit("No se encuentra latexmk. Instala MiKTeX (Windows) o MacTeX / BasicTeX (macOS).")
    if "--clean" in argv:
        subprocess.run(["latexmk", "-C", "memoria.tex"], cwd=HERE)
        shutil.rmtree(HERE / "build", ignore_errors=True)
        return 0
    r = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-outdir=build", "memoria.tex"],
        cwd=HERE,
    )
    if r.returncode == 0:
        shutil.copy(HERE / "build" / "memoria.pdf", HERE / "memoria.pdf")
        print(f"OK -> {HERE / 'memoria.pdf'}")
    return r.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
