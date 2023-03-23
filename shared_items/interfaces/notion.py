import os

from typing import Any, Callable, Literal, Optional, TypedDict, Union, cast
from typing_extensions import NotRequired
from operator import itemgetter

from notion_client import Client as NotionClient

from shared_items.utils import pp

MOVIES_PAGE_ID = "491cd007d6cf466a80be98a6576e01f2"
MOVIES_DATABASE_ID = "e341bcbed2f14bdeaa7377415865d2fa"


class TextPropContent(TypedDict):
    content: Union[str, int]


class DatePropContent(TypedDict):
    start: str
    end: NotRequired[str]
    time_zone: NotRequired[str] # note: not required if only date


class Prop(TypedDict):
    name: str
    type: str
    content: Union[TextPropContent, DatePropContent]


ARRAY_CONTENT_TYPES = ["rich_text", "title"]

COMPATIBLE_TYPES = Literal["rich_text", "title", "date", "number", "url"]

TYPE_MAP = {"rich_text": "text", "title": "text"}


class Notion:
    def __init__(self):
        self.__token = os.getenv("NOTION_TOKEN")
        self.client = NotionClient(auth=self.__token)

    def assemble_prop(self, prop: Prop) -> dict:
        type = prop["type"]
        content = prop["content"]

        content_structure: Any

        if type == "date":
            content = cast(DatePropContent, content)
            content_structure = self.__date_prop(content)
        else:
            content = cast(TextPropContent, content)
            content_structure = self.__text_prop(content, type)

        return {type: content_structure}


    def __date_prop(self, content: DatePropContent) -> dict:
        content_structure = {
            "start": content["start"],
        }
        if content.get("time_zone"):
            content_structure["time_zone"] = content["time_zone"]
        return content_structure

    def __text_prop(self, content: TextPropContent, type: str) -> Union[list, Union[str, int]]:
        content_structure: Union[list, Union[str, int]]
        if type in ARRAY_CONTENT_TYPES:
            content_structure = [{TYPE_MAP[type]: {"content": content["content"]}}]
        elif type == "number":
            content_structure = content["content"]
        elif type == "url":
            content_structure = content["content"]
        return content_structure



    def assemble_props(self, props: list[Prop]) -> dict:
        update_props = {}

        for prop in props:
            name = itemgetter("name")(prop)
            update_props[name] = self.assemble_prop(prop)

        return update_props

    # note: this only handles text type content for now
    # the dict returned is a Notion Page, too complicated to type for now, given lack of need
    def update_page_props(self, page_id: str, props: dict) -> dict:
        return self.client.pages.update(page_id=page_id, properties=props)

    # the dict returned contains a list of Notion Pages, too complicated to type for now, given lack of need
    def query_database(self, database_id: str) -> dict:
        return self.client.databases.query(database_id=database_id)

    def recursive_fetch_and_delete(self, fetcher: Callable[[Optional[str]], dict]):
        def func(next_cursor: Optional[str] = None):
            database_response = fetcher(next_cursor)
            database_rows = database_response["results"]

            for row in database_rows:
                self.client.blocks.delete(block_id=row["id"])

            if database_response["has_more"]:
                func(database_response["next_cursor"])

        return func

    def recursive_fetch(self, fetcher: Callable[[Optional[str]], dict]):
        rows: list[dict] = []

        def func(next_cursor: Optional[str] = None, rows=rows):
            database_response = fetcher(next_cursor)
            database_rows = database_response["results"]
            rows += database_rows

            if database_response["has_more"]:
                func(database_response["next_cursor"], rows)
            else:
                return rows

        return func

    def create_row_for_database(self, database_id: str):
        def create_row(props: dict):
            self.client.pages.create(
                parent={"database_id": database_id}, properties=props
            )

        return create_row
