import logging
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from importlib.resources import files as resource_files
from logging.config import dictConfig

import yaml
from examples_gdrive import __version__
from examples_gdrive.gauth import AuthAccount, get_credentials

with resource_files("examples_gdrive.resources").joinpath("logging_config.yaml").open() as file:
    config_dict = yaml.safe_load(file)
dictConfig(config_dict)

logger = logging.getLogger("examples_gdrive")


def __parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="console examples for argparse.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "--auth",
        type=lambda s: AuthAccount.from_string(s),
        choices=list(AuthAccount),
        dest="auth_type",
        help="select auth account type\n(default: %(default)s)",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="show verbose output, -vv -vvv is even more.",
        default=0,
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show version and exit",
    )

    subparsers = parser.add_subparsers(
        title="sub commands",
        description="for examples commands",
        help="choose command",
        required=True,
    )

    # gdrive
    from examples_gdrive.console._gdrive import configure_parser as configure_gdrive

    gdrive_parser = subparsers.add_parser("gdrive", help="Google drive API example")
    configure_gdrive(gdrive_parser)

    args = parser.parse_args()

    return args


def main() -> None:
    args = __parse_arguments()

    # authentication
    creds = get_credentials(args.auth_type)

    try:
        args.exec(args, creds)
    except Exception:
        logger.exception("Exiting due to an unhandled exception.")


if __name__ == "__main__":
    main()
