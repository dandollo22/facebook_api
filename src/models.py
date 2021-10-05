import sqlalchemy as _sql
import database as _database


class FacebookPost(_database.Base):
    __tablename__ = "facebook_data"
    id = _sql.Column(_sql.String, primary_key=True, index=True)
    post_url = _sql.Column(_sql.String, unique=True, index=True)
    shared_at = _sql.Column(_sql.String)
    page = _sql.Column(_sql.String)
    likes = _sql.Column(_sql.String)
    comments = _sql.Column(_sql.String)
    shares = _sql.Column(_sql.String)
