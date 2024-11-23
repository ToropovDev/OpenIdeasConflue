from sqlalchemy import Table, Column, String, DateTime, MetaData, UUID, func
import uuid

metadata = MetaData()


comment = Table(
    "comment",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid.uuid4, unique=True),
    Column("text", String(64), nullable=False),
    Column("created_at", DateTime(True), server_default=func.now()),
)
