from argparse import ArgumentParser, Namespace
from logging import getLogger

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

logger = getLogger(__name__)


def do_quickstart(args: Namespace, creds: Credentials) -> None:
    parent_id: str | None = args.parent_id
    try:
        service: Resource = build("drive", "v3", credentials=creds)

        # fmt: off
        query = (
            "mimeType!='application/vnd.google-apps.folder'" +
            " and trashed=false")
        # fmt: on

        if parent_id:
            query += f" and '{parent_id}' in parents"

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                q=query,
                pageSize=10,
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            logger.warn("No files found.")
            return

        logger.info("Files:")
        for item in items:
            logger.info("  {0} ({1})".format(item["name"], item["id"]))

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        logger.exception(f"An error occurred: {error}")


def configure_parser(parser: ArgumentParser) -> None:
    subparsers = parser.add_subparsers(
        title="Google Drive API example",
        help="choose command",
        required=True,
    )

    # list
    list_parser = subparsers.add_parser("list", help="list a drive")
    list_parser.add_argument(
        "-d",
        "--dir",
        dest="parent_id",
        help="parent directory id",
        default=None,
    )
    list_parser.set_defaults(exec=lambda args, creds: do_quickstart(args, creds))
