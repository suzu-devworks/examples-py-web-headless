from argparse import ArgumentParser, Namespace

from httplib2 import Credentials


def configure_parser(parser: ArgumentParser) -> None:
    parser.set_defaults(exec=lambda args, creds: do_sample(args, creds))


def do_sample(args: Namespace, creds: Credentials) -> None:
    pass
