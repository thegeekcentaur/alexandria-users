__author__ = 'archanda'
__date__ = '31-Mar-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["archanda"]
__license__ = "All rights reserved"
__maintainer__ = "archanda"
__email__ = "2020mt93064@wilp.bits-pilani.ac.in"
__status__ = "dev"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import routes here
from services.book_service_v1 import router as BookServiceRouteV1
from services.catalog_service_v1 import router as CatalogServiceRouteV1
from services.user_service_v1 import router as UserServiceRouteV1

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserServiceRouteV1, prefix='/users')