__author__ = 'surendar'
__date__ = '15-Oct-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["surendar"]
__license__ = "All rights reserved"
__maintainer__ = "surendar"
__email__ = "2020mt93162@wilp.bits-pilani.ac.in"
__status__ = "dev"

from fastapi import FastAPI, HTTPException
from typing import Optional
import requests
import logging
from core import database
from services import (book_details_module)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_search_term_and_filter_type(isbn: str, author_name: str, subject: str, publisher_name: str):
    if isbn:
        return {"search_term": isbn, "filter": "isbn"}
    elif author_name:
        return {"search_term": author_name, "filter": "inauthor"}
    elif subject:
        return {"search_term": subject, "filter": "subject"}
    elif publisher_name:
        return {"search_term": publisher_name, "filter": "inpublisher"}
    else:
        return {"filter": "invalid_filter"}

async def search_book_by_filter(search_term: str, filter: str):    
    search_response = book_details_module.get_books_by_filter(filter, search_term)
    if search_response:
        logger.info("Book search response: {}".format(search_response))
        return search_response
    else:
        raise HTTPException(
            status_code=404,
            detail="No book found for given filter: {} and value: {}".format(filter, search_term)
        )

def validateUser(user_id: str, user_list):
    user_found = next((user for user in user_list if user.user_id == user_id), None)
    return True if user_found else False