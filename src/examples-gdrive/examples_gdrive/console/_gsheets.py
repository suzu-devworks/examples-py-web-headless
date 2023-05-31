from argparse import ArgumentParser, Namespace
from datetime import datetime
from logging import getLogger

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

logger = getLogger(__name__)


def __build_drive_resource(credentials: Credentials) -> Resource:
    return build("drive", "v3", credentials=credentials)


def __build_sheets_resource(credentials: Credentials) -> Resource:
    return build("sheets", "v4", credentials=credentials)


def do_create(args: Namespace, creds: Credentials) -> str:
    title: str = args.title.strip()
    parent_id: str = args.parent_id.strip() if args.parent_id else None

    try:
        # --- can only be created by root folder.
        # service = build("sheets", "v4", credentials=creds)
        # spreadsheet = {"properties": {"title": title}}
        # spreadsheet = service.spreadsheets().create(body=spreadsheet, fields="spreadsheetId").execute()

        # create sheet
        service = __build_drive_resource(credentials=creds)
        file_metadata = {
            "name": title,
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]
            logger.info(f"Parent ID: {parent_id}")

        logger.debug("Request files create.")
        response = service.files().create(body=file_metadata, fields="id").execute()

        file_id = response.get("id")
        logger.debug(f"File ID: {file_id}")

        # open sheet
        service = __build_sheets_resource(credentials=creds)

        logger.debug("Request get.")
        response = service.spreadsheets().get(spreadsheetId=file_id).execute()

        spreadsheet_id = response.get("spreadsheetId")
        spreadsheet_url = response.get("spreadsheetUrl")
        spreadsheet_title = response.get("properties").get("title")
        logger.info(f"Spreadsheet ID: {spreadsheet_id} ({spreadsheet_title})")
        logger.info(f"Spreadsheet URL: {spreadsheet_url}")

        return spreadsheet_id

    except HttpError:
        logger.exception("An error occurred.")


def do_add_sheet(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    try:
        # add sheet
        service = __build_sheets_resource(credentials=creds)

        properties = {
            "gridProperties": {"rowCount": 20, "columnCount": 12},
            "tabColor": {"red": 1.0, "green": 0.3, "blue": 0.4},
        }

        requests = []
        requests.append({"addSheet": {"properties": properties}})
        request_body = {
            # A list of updates to apply to the spreadsheet.
            # Requests will be applied in the order they are specified.
            # If any request is not valid, no requests will be applied.
            "requests": requests
        }

        logger.debug("Request batchUpdate.")
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()

        spreadsheet_id = response.get("spreadsheetId")
        sheet = response.get("replies")[0].get("addSheet").get("properties")
        sheet_id = sheet.get("sheetId")
        sheet_title = sheet.get("title")
        logger.info(f"Updated Spreadsheet ID: {spreadsheet_id} ")
        logger.info(f"Sheet ID: {sheet_id} ({sheet_title})")

    except HttpError:
        logger.exception("An error occurred.")


def do_write_data(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    try:
        service = __build_sheets_resource(credentials=creds)

        # clear range data
        range = "'シート1'!A1:H50"

        logger.debug("Request value clear.")
        response = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=range).execute()

        logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
        logger.info(f" clearedRange: {response.get('clearedRange')}")

        # write range data
        # fmt: off
        values = ([
            ["A", "B"],
            ["C", str(datetime.now())],
        ])
        # fmt: on
        request_body = {"values": values}
        request_range = "'シート1'!A1:C2"

        logger.debug("Request value update.")
        response = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=request_range,
                valueInputOption="USER_ENTERED",
                body=request_body,
            )
            .execute()
        )
        logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
        logger.info(f" updatedRange: {response.get('updatedRange')}")
        logger.info(f" updatedCells: {response.get('updatedCells')}")

        # write multiple range data
        # fmt: off
        values = ([
            ["F", "B"],
            ["C", str(datetime.now())],
        ])
        # fmt: on
        data = [
            {"range": "'シート1'!D4", "values": values},
            {"range": "'シート1'!D8", "values": values},
        ]
        request_body = {"valueInputOption": "USER_ENTERED", "data": data}

        logger.debug("Request value batchUpdate.")
        response = (
            service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()
        )

        logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
        logger.info(f" totalUpdatedCells: {response.get('totalUpdatedCells')}")

        # append table datas
        # fmt: off
        values = ([
            ["G", "B"],
            ["C", str(datetime.now())],
        ])
        # fmt: on
        request_body = {"values": values}

        logger.debug("Request append.")
        response = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range="A1",
                valueInputOption="USER_ENTERED",
                body=request_body,
            )
            .execute()
        )
        logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
        logger.info(f" tableRange: {response.get('tableRange')}")
        logger.info(f" updatedCells: {response.get('updates').get('updatedCells')}")

    except HttpError:
        logger.exception("An error occurred.")


def do_read_data(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    try:
        service = __build_sheets_resource(credentials=creds)

        # read range data
        range_name = "'シート1'!A1:C4"

        logger.debug("Request value get.")
        response = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

        values = response.get("values", [])
        logger.info(f"{response.get('range')} >>> {values}")

        # read multiple range datas
        range_names = [
            "D4:F5",
            "D8:F9",
        ]

        logger.debug("Request value batchGet.")
        response = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_names).execute()

        logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
        response = response.get("valueRanges", [])
        for reply in response:
            values = reply.get("values", [])
            logger.info(f"{reply.get('range')} >>> {values}")

    except HttpError:
        logger.exception("An error occurred.")


def do_delete(args: Namespace, creds: Credentials) -> None:
    file_id: str = args.fileId
    force: bool = args.force

    try:
        # delete file(drive)
        service = __build_drive_resource(credentials=creds)

        if force:
            logger.debug("Request files delete.")
            response = service.files().delete(fileId=file_id).execute()

            logger.info(f"deleted(force) : {file_id}")

        else:
            logger.debug("Request files move to trashed.")
            response = service.files().update(fileId=file_id, body={"trashed": True}).execute()  # noqa F841

            logger.info(f"deleted : {file_id}")

    except HttpError:
        logger.exception("An error occurred.")


def configure_parser(parser: ArgumentParser) -> None:
    subparsers = parser.add_subparsers(
        title="Google Sheets API example",
        help="choose command",
        required=True,
    )

    # create
    create_parser = subparsers.add_parser("create", help="create new spreadsheet")
    create_parser.add_argument(
        "-t",
        "--title",
        dest="title",
        help="file title",
        default="無題のスプレッドシート",
    )
    create_parser.add_argument(
        "-d",
        "--dir",
        dest="parent_id",
        help="parent directory id",
        default=None,
    )
    create_parser.set_defaults(exec=lambda args, creds: do_create(args, creds))

    # add sheet
    sheet_parser = subparsers.add_parser("add", help="add sheet in spreadsheet sample")
    sheet_parser.add_argument(
        "fileId",
        help="fileId",
        type=str,
    )
    sheet_parser.set_defaults(exec=lambda args, creds: do_add_sheet(args, creds))

    # write
    wraite_parser = subparsers.add_parser("write", help="write data sample")
    wraite_parser.add_argument(
        "fileId",
        help="fileId",
        type=str,
    )
    wraite_parser.set_defaults(exec=lambda args, creds: do_write_data(args, creds))

    # read
    read_parser = subparsers.add_parser("read", help="read data sample")
    read_parser.add_argument(
        "fileId",
        help="fileId",
        type=str,
    )
    read_parser.set_defaults(exec=lambda args, creds: do_read_data(args, creds))

    # delete
    delete_parser = subparsers.add_parser("delete", help="delete spreadsheet sample")
    delete_parser.add_argument(
        "fileId",
        help="fileId",
        type=str,
    )
    delete_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        dest="force",
        help="force delete spreadsheeet.",
        default=False,
    )
    delete_parser.set_defaults(exec=lambda args, creds: do_delete(args, creds))
