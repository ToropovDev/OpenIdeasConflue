from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    MetaData,
    UUID,
    func,
    JSON,
    Integer,
    Boolean,
)
import uuid

metadata = MetaData()

comment = Table(
    "comment",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("text", String(64), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
)

article = Table(
    "article",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("name", String(64), nullable=False),
    Column("text", String, nullable=False, default="", server_default=""),
    Column("section", String, nullable=False),
    Column("created_at", DateTime(True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(True), nullable=True, server_default=func.now()),
    Column("tags", JSON, nullable=True),
    Column("watching_count", Integer, nullable=False, default=0, server_default='0'),
    Column("is_draft", Boolean, nullable=False, default=True, server_default="true"),
)


file = Table(
    "file",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("s3_link", String(512), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
)
