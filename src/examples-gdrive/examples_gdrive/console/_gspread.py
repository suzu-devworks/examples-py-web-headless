from argparse import ArgumentParser, Namespace
from datetime import datetime
from logging import getLogger

import gspread
from google.oauth2.credentials import Credentials

logger = getLogger(__name__)


def do_create(args: Namespace, creds: Credentials) -> str:
    title: str = args.title.strip()
    parent_id: str = args.parent_id.strip() if args.parent_id else None

    client = gspread.authorize(creds)

    if parent_id:
        logger.info(f"Parent ID: {parent_id}")

    logger.debug("call create.")
    spreadsheet = client.create(title=title, folder_id=parent_id)

    # If you're using a service account, you'll need to share the spreadsheet via email.
    # spreadsheet.share("otto@example.com", perm_type="user", role="writer", notify=False)

    logger.info(f"Spreadsheet ID: {spreadsheet.id} ({spreadsheet.title})")
    logger.info(f"Spreadsheet URL: {spreadsheet.url}")
    logger.info(f">>> { spreadsheet.creationTime}")
    logger.info(f">>> { spreadsheet.lastUpdateTime}")

    return spreadsheet.id


def do_add_sheet(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)

    logger.debug("call add_worksheet.")
    worksheet = spreadsheet.add_worksheet(title=None, rows=20, cols=12)
    worksheet.update_tab_color({"red": 1.0, "green": 0.3, "blue": 0.4})

    logger.info(f"Updated Spreadsheet ID: {spreadsheet.id} ")
    logger.info(f"Sheet ID: {worksheet.id} ({worksheet.title})")

    return


def do_write_data(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.get_worksheet(0)

    # clear range data
    logger.debug("call batch_clear.")
    # all clear : worksheet.clear()
    response = worksheet.batch_clear(["A1:H50"])

    logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
    logger.info(f" clearedRanges: {response.get('clearedRanges')}")

    # write range data
    # fmt: off
    values = ([
        ["A", "B"],
        ["C", str(datetime.now())],
    ])
    # fmt: on

    logger.debug("call batch_clear.")
    response = worksheet.update("A1:C2", values)

    logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
    logger.info(f" updatedRange: {response.get('updatedRange')}")
    logger.info(f" updatedCells: {response.get('updatedCells')}")

    # write multiple range data
    # fmt: off
    values = ([
        ["F", "B"],
        ["C", str(datetime.now())],
    ])

    logger.debug("call batch_update.")
    response = worksheet.batch_update([{
        'range': 'D4',
        'values': values,
    }, {
        'range': 'D8',
        'values': values,
    }])

    logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
    logger.info(f" totalUpdatedCells: {response.get('totalUpdatedCells')}")

    # format
    formats = [
        {
            "range": "A1:C1",
            "format": {
                "textFormat": {
                    "bold": True,
                },
                "backgroundColorStyle": {
                    "rgbColor": {"red": 1.0, "green": 0.3, "blue": 0.3},
                }
            },
        },
        {
            "range": "A2:C2",
            "format": {
                "textFormat": {
                    "fontSize": 16,
                    "foregroundColor": {"red": (10 / 255.0) , "green": (50 / 255.0), "blue": float(100 / 255.0)},
                },
            },
        },
    ]
    logger.debug("call batch_format.")
    response = worksheet.batch_format(formats)

    logger.info(f"Spreadsheet ID: {response.get('spreadsheetId')}")
    logger.info(f"len(replies): {len(response.get('replies', []))}")

    return


def do_read_data(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId

    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1

    logger.debug("call any ...")
    cell = worksheet.acell("B2")
    logger.info(f"'{cell.address}' >>> {cell.value}")
    cell = worksheet.cell(2, 1)
    logger.info(f"'{cell.address}' >>> {cell.value}")
    cell = worksheet.acell("A1:C2")
    logger.info(f"'{cell.address}' >>> {cell.value}")

    values = worksheet.row_values(1)
    logger.info(f" >>> {values}")
    values = worksheet.col_values(5)
    logger.info(f" >>> {values}")

    list_of_lists = worksheet.get_all_values()
    logger.info(f" >>> {list_of_lists}")

    logger.debug("call get.")
    values = worksheet.get("A1:B2")

    logger.info(f"{values.range} >>> {values}")

    logger.debug("call batch_get.")
    values_list = worksheet.batch_get(["D4:F5", "D8:F9"])

    for values in values_list:
        logger.info(f"{values.range} >>> {values}")

    return


def do_delete(args: Namespace, creds: Credentials) -> None:
    spreadsheet_id: str = args.fileId
    force: bool = args.force

    client = gspread.authorize(creds)

    if force:
        logger.debug("call del_spreadsheet.")
        client.del_spreadsheet(spreadsheet_id)

        logger.info(f"deleted(force): {spreadsheet_id} ")
    else:
        # TODO move to trashed ?
        pass

    return


def configure_parser(parser: ArgumentParser) -> None:
    subparsers = parser.add_subparsers(
        title="Python API for Google Sheets example",
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
        default="A new spreadsheet",
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
