from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    func,
)


class TimestampMixin:
    loaded_at = Column(
        DateTime,
        nullable=False,
        index=True,
        default=datetime.utcnow,
        server_default=func.now(),
    )
