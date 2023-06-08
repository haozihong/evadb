# coding=utf-8
# Copyright 2018-2023 EvaDB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from evadb.catalog.catalog_type import TableType
from evadb.catalog.models.base_model import BaseModel
from evadb.catalog.models.utils import TableCatalogEntry


class TableCatalog(BaseModel):
    """The `TableCatalog` catalog stores information about all tables (structured, media, etc.) and materialized views. It has the following columns, not all of which are relevant for all table types.
    `_row_id:` an autogenerated unique identifier.
    `_name:` the name of the table, view, etc.
    `_file_url:` the path to the data file on disk
    `_table_type:` the type of the table (refer to TableType).
    """

    __tablename__ = "table_catalog"

    _name = Column("name", String(100), unique=True)
    _file_url = Column("file_url", String(100))
    _identifier_column = Column("identifier_column", String(100))
    _table_type = Column("table_type", Enum(TableType))

    # the child table containing information about the columns of the each table
    _columns = relationship(
        "ColumnCatalog",
        back_populates="_table_catalog",
        cascade="all, delete, delete-orphan",
    )

    def __init__(
        self, name: str, file_url: str, table_type: int, identifier_column="id"
    ):
        self._name = name
        self._file_url = file_url
        self._identifier_column = identifier_column
        self._table_type = table_type

    def as_dataclass(self) -> "TableCatalogEntry":
        column_entries = [col_obj.as_dataclass() for col_obj in self._columns]
        return TableCatalogEntry(
            row_id=self._row_id,
            name=self._name,
            file_url=self._file_url,
            identifier_column=self._identifier_column,
            table_type=self._table_type,
            columns=column_entries,
        )
