from pathlib import Path
from .language.compiler import Compiler
from typer import run, Exit, style, colors
from sys import exc_info



def compile(bs: str, py: str = "", run: bool = True):
    if bs == str():
        raise ValueError(f"Parameter {bs} must be a path")
    bs: Path = Path(bs).resolve()

    if bs.suffix == ".bs":
        py: Path = Path(py) if py != str() else Path(
            str(bs.parent) + "/" + bs.stem + ".py").resolve()

        if bs.exists():
            compiler = Compiler()
            python_code = str()
            with open(bs, "r") as fbs:
                # # ! Uncomment for debug
                # python_code = compiler(fbs.read())

                # ! Comment for debug
                try:
                    python_code = compiler(fbs.read())
                except BaseException as e:
                    print(style("Error", fg=colors.RED, bold=True) + "\t" + str(exc_info()[1]))
                    Exit(code=1)
            if not run:
                with open(py, "w") as fpy:
                    fpy.write(python_code)
                print(f"{style('Compiled!', fg=colors.BRIGHT_GREEN, bold=True)}\nResult file: {py}")
            else:
                exec(python_code)
            return
        raise ValueError(f"File {bs} dont exist")
    raise ValueError(f"File {bs} must be Battle Script type")


if __name__ == "__main__":
    run(compile)
    # compile("./test/examples/ex6.bs", run=False)
