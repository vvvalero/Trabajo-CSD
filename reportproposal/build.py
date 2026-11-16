"""Compila la memoria a PDF (Windows / macOS / Linux). Requiere latexmk.

  python3 reportproposal/build.py          genera reportproposal/memoria.pdf
  python3 reportproposal/build.py --datos  regenera las mediciones antes de compilar
  python3 reportproposal/build.py --clean  borra lo generado en esta propuesta
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
    if "--datos" in argv:
        datos = subprocess.run([sys.executable, str(HERE / "generar_datos.py")])
        if datos.returncode:
            return datos.returncode
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
