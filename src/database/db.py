import configparser
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URI:  postgresql://username:password@domain:port/database
# path_archive = Path(os.path.join(clean_folder, "archives"))
file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
database = config.get('DEV_DB', 'DB_NAME')

URI = f"postgresql+psycopg2://{username}:{password}@{domain}:{port}/{database}"

engine = create_engine(URI, echo=True, max_overflow=5)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
