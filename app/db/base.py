from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so SQLAlchemy registers them on Base.metadata.
from app.models import models  # noqa: F401,E402