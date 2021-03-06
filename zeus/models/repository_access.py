from zeus.config import db
from zeus.constants import Permission
from zeus.db.types import Enum, GUID
from zeus.db.utils import model_repr


class RepositoryAccess(db.Model):
    repository_id = db.Column(
        GUID, db.ForeignKey("repository.id", ondelete="CASCADE"), primary_key=True
    )
    user_id = db.Column(
        GUID, db.ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    permission = db.Column(
        Enum(Permission), nullable=False, default=Permission.read, server_default="1"
    )

    repository = db.relationship("Repository", innerjoin=True, uselist=False)
    user = db.relationship("User", innerjoin=True, uselist=False)

    __tablename__ = "repository_access"
    __repr__ = model_repr("repository_id", "user_id")
