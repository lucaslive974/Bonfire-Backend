from argparse import ArgumentParser, Namespace


class Args(Namespace):
    port: int
    debug: bool

    def __init__(self):
        super().__init__()
        self.port = 5000
        self.debug = False


class BonfireArgumentParser(ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.add_argument("--debug", action="store_true", help="Debug mode")
        self.add_argument("--port", type=int, default=5000, help="Server port")

        self._args = self.parse_args(namespace=Args())

    def isDebug(self) -> bool:
        return self._args.debug

    def port(self) -> int:
        return self._args.port
