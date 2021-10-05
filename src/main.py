import fastapi as _fastapi
import services as _services
import sqlalchemy.orm as _orm
from uvicorn import run
from starlette.responses import RedirectResponse
import models as _models
from database import engine

app = _fastapi.FastAPI()
_services.create_database()
_models.FacebookPost.metadata.create_all(bind=engine)


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


@app.post("/scrapper/{facebook_page}")
async def scrap_page_posts(facebook_page: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.scrap_data(facebook_page, db)


@app.get("/get_posts/{facebook_page}")
async def get_page_posts(facebook_page: str, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return _services.get_post_by_page(db=db, page_ext=facebook_page)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
