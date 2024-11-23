from sqlalchemy import (
    Table,
    Column,
    String,
    DateTime,
    MetaData,
    UUID,
    func,
    JSON,
    INT,
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
    Column("text", String, nullable=False),
    Column("chapter", INT, nullable=False),
    Column("created_by", DateTime(True), nullable=False),
    Column("created_at", DateTime(True), nullable=False, server_default=func.now()),
    Column("updated_by", DateTime(True), nullable=False),
    Column("updated_at", DateTime(True), nullable=False, server_default=func.now()),
    Column("tags", JSON, nullable=False),
    Column("watching_count", INT, nullable=False),
    Column("is_draft", Boolean, nullable=False),
)


file = Table(
    "file",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("s3_link", String(512), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
)
