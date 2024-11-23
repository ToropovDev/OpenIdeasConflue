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
    ForeignKey,
)
import uuid

metadata = MetaData()

article = Table(
    "article",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("name", String(64), nullable=False),
    Column(
        "section_id",
        UUID(as_uuid=True),
        ForeignKey("section.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("text", String, nullable=False, default="", server_default=""),
    Column("created_at", DateTime(True), nullable=False, server_default=func.now()),
    Column("updated_at", DateTime(True), nullable=True, server_default=func.now()),
    Column("tags", JSON, nullable=True),
    Column("watching_count", Integer, nullable=False, default=0, server_default="0"),
    Column("is_draft", Boolean, nullable=False, default=True, server_default="true"),
)

section = Table(
    "section",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4(), unique=True),
    Column("name", String(64), nullable=False),
    Column("parent_section_id", UUID, nullable=True),
)


file = Table(
    "file",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("s3_link", String(512), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
)

file_article = Table(
    "file_article",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("file_id", UUID, ForeignKey("file.id"), nullable=False),
    Column("article_id", UUID, ForeignKey("article.id"), nullable=False),
)

comment = Table(
    "comment",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("text", String(64), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
    Column("updated_at", DateTime(True), nullable=True),
    Column("article_id", UUID, ForeignKey("article.id"), nullable=False),
)
