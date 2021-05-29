import cx_Freeze

executables = [cx_Freeze.Executable("sushi_dodger.py")]

cx_Freeze.setup(
    name="Sushi Dodger",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["racecar.png"]}},
    executables = executables

    )
