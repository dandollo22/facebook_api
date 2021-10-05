from scraper import FacebookScraper
import database as _database
import sqlalchemy.orm as _orm
import schemas as _schemas
import models as _models


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def scrap_data(facebook_page, db):
    scraper = FacebookScraper(browser='chrome')
    data = scraper.get_posts(facebook_page)
    for post in data[facebook_page]:
        fb_post = _schemas.FacebookPost(**post)
        create_post(db, fb_post)
    return data


def create_post(db: _orm.Session, post: _schemas.FacebookPost):
    db_post = _models.FacebookPost(id=post.id,
                                   post_url=post.post_url,
                                   shared_at=post.shared_at,
                                   page=post.page,
                                   likes=post.likes,
                                   comments=post.comments,
                                   shares=post.shares)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)


def get_post_by_page(db: _orm.Session, page_ext: str):
    return db.query(_models.FacebookPost).filter(_models.FacebookPost.page == page_ext).all()
