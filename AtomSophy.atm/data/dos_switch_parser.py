import sys


def parse_args(args):
    opts = {
        "commands": [],
        "quiet": False,
        "new_file": False,
        "force_disk": False,
        "hidden": False,
        "ex_file": None,
        "file": None,
        "window_only": False,
    }

    for arg in args:
        if arg.lower().startswith("/c"):
            cmd_str = arg[2:]
            opts["commands"] = [cmd.strip() for cmd in cmd_str.split(";") if cmd.strip()]
        elif arg.lower() == "/q":
            opts["quiet"] = True
        elif arg.lower() == "/n":
            opts["new_file"] = True
        elif arg.lower() == "/d":
            opts["force_disk"] = True
        elif arg.lower() == "/h":
            opts["hidden"] = True
        elif arg.lower().startswith("/e"):
            opts["ex_file"] = arg[2:]
        elif arg.lower() == "/w":
            opts["window_only"] = True
        elif not arg.startswith("/"):
            opts["file"] = arg

    return opts


class AtomSophyShell:
    def __init__(self, quiet=False, ex_file=None, window_only=False):
        self.quiet = quiet
        self.ex_file = ex_file
        self.window_only = window_only
        self.filename = None
        self.current_file = ""
        self.hidden_mode = False

    def load_file(self, filename, new=False, force_disk=False, hidden=False):
        if new:
            self.current_file = ""
            self.filename = filename
        elif force_disk:
            self.filename = filename
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                self.current_file = f.read()
        else:
            self.filename = filename

        if hidden:
            self.hidden_mode = True

    def execute_command(self, command):
        # Aquí iría el parser tipo FoxPro o comando CLI interno
        print(f"[EXEC] {command}")

    def run(self):
        print("Hola! Soy AtomSophy, tu ayudante retro en CLI")
        while True:
            try:
                line = input("AtomSophy> ").strip()
                if line.upper() == "EXIT":
                    break
                self.execute_command(line)
            except KeyboardInterrupt:
                break


def main():
    args = sys.argv[1:]
    opts = parse_args(args)

    shell = AtomSophyShell(
        quiet=opts["quiet"],
        ex_file=opts["ex_file"],
        window_only=opts["window_only"]
    )

    if opts["file"]:
        shell.load_file(opts["file"], new=opts["new_file"], force_disk=opts["force_disk"], hidden=opts["hidden"])

    if opts["commands"]:
        for cmd in opts["commands"]:
            if not opts["quiet"]:
                print(f"> {cmd}")
            shell.execute_command(cmd)
        return

    if not opts["quiet"]:
        print("Hola! Soy AtomSophy, tu ayudante retro en CLI")

    shell.run()


if __name__ == "__main__":
    main()
