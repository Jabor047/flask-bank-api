import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.models.database import Base


# for linux and windows systems uncomment below
docker_host_ip = os.getenv("DB_HOST")

# for mac os
# docker_host_ip = "host.docker.internal"
engine = create_engine(f"postgresql://docker:docker@{docker_host_ip}/docker")

Base.metadata.bind = engine

db = scoped_session(sessionmaker(bind=engine))
