import logging
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from importlib.resources import files as resource_files
from logging.config import dictConfig

import yaml
from examples_gcloud import __version__
from examples_gcloud.gauth import AuthAccount, get_credentials

with resource_files("examples_gcloud.resources").joinpath("logging_config.yaml").open() as file:
    config_dict = yaml.safe_load(file)
dictConfig(config_dict)

logger = logging.getLogger("examples_gcloud")


def __parse_arguments() -> Namespace:
    parser = ArgumentParser(
        description="Google Cloud API programming examples.",
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
    from examples_gcloud.console._gdrive import configure_parser as configure_gdrive

    gdrive_parser = subparsers.add_parser("gdrive", help="Google drive API example")
    configure_gdrive(gdrive_parser)

    # gsheets
    from examples_gcloud.console._gsheets import configure_parser as configure_gsheets

    gspread_parser = subparsers.add_parser("gsheets", help="Google Sheets API example")
    configure_gsheets(gspread_parser)

    # gspread
    from examples_gcloud.console._gspread import configure_parser as configure_gspread

    gspread_parser = subparsers.add_parser("gspread", help="Python API for Google Sheets example")
    configure_gspread(gspread_parser)

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
