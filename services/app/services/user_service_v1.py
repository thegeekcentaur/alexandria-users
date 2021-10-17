__author__ = 'archanda'
__date__ = '3-Oct-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["archanda"]
__license__ = "All rights reserved"
__maintainer__ = "archanda"
__email__ = "2020mt93064@wilp.bits-pilani.ac.in"
__status__ = "dev"

from fastapi import FastAPI, Body, APIRouter, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from core import database
import logging

from services import (user_management_module, catalog_service_v1)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# route-specific modules go here
from api.routes import urls

router = APIRouter()

from models.schemas.user import ( UserSchema )

from models.schemas.catalog import ( CatalogSchema )

# Added By Surendar S BITS

# ______________________
#  User Management APIs
# ______________________

# 1) Get all Users from mongodb...
@router.get(urls.get_all_users_url)
async def get_user_list():
    users = await database.get_all_user_details()
    return {"users": users, "totalUsers": len(users)}

# 2) Get user by id from mongodb...
@router.get(urls.get_user_by_id_url)
async def user_management(user_id: str):
    logger.info("Fetching User details for the ID {}".format(user_id))
    try:
        user_found = await validateUser(user_id)
        if user_found:
            logger.info('User details: {}'.format(user_found))
            return user_found
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message

# 3) Save new User to mongodb...
@router.post(urls.save_user_url)
async def save_user(user_data: UserSchema = Body(...)):
    logger.info('Checking if the user \'{}\' already exists'.format(user_data.name))
    user_already_exists = await database.is_user_name_already_taken(user_data.name)
    if user_already_exists:
        raise HTTPException(status_code=400, detail="User name already exists.")
    new_user = await database.add_user(user_data)
    return {"new_user": new_user}

# 4) Update the existing user data
@router.put(urls.update_user_by_id_url)
async def update_user_by_id(user_id: str, user_data: UserSchema = Body(...)):
    logger.info("Updating User details for the User Id {}".format(user_id))
    try:
        await validateUser(user_id)
        user_updated = await database.update_user_by_id(user_id, user_data)
        if user_updated:
            return {
                "id": user_id, "message":
                "User details for [{}] has been updated Successfully.".format(user_id)
            }
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message

# 5) Deleting user data from mongodb...
@router.delete(urls.delete_user_by_id_url)
async def delete_user_by_id(user_id: str):
    try:
        await validateUser(user_id)
        user_deleted = await database.delete_user_by_id(user_id)
        if user_deleted:
            return {"id": user_id, "message": "Deletion successful"}
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        return message

# ___________________________________________
#  API to Search books by impersonating User
# ___________________________________________

@router.post(urls.search_book_by_user_id)
async def search_book_with_user_id(
    user_id: str,
    isbn: Optional[str] = None,
    inauthor: Optional[str] = None,
    subject: Optional[str] = None,
    inpublisher: Optional[str] = None):

    #check if a valid User ID has been typed
    await validateUser()

    # Get the search term and filter type to call appropriate book API
    search_term_and_filter_type = user_management_module.get_search_term_and_filter_type(
        isbn, inauthor, subject, inpublisher)
    
    logger.info(search_term_and_filter_type);

    # Throw error when the filter type is invalid
    if search_term_and_filter_type["filter"] == "invalid_filter":
        filter_list = ['isbn', 'inauthor', 'subject', 'inpublisher']
        raise HTTPException(
            status_code=400,
            detail="Invalid search Filter/ No search term has been entered. Please use any one of these filters to search {}".format(filter_list)
        )

    search_result = await user_management_module.search_book_by_filter(
        search_term_and_filter_type["search_term"],
        search_term_and_filter_type["filter"]
        )
    return {"book_search_result": search_result}

# _____________________________
#  User Catalog management API 
# _____________________________

# Get All Catalogs for a given user
@router.get(urls.get_all_catalog_for_user_id)
async def get_all_catalogs_for_user(user_id: str):
    await validateUser(user_id)
    return await catalog_service_v1.get_catalog_list(user_id)

# Get a Catalog for given catalog name for given user
@router.get(urls.get_catalog_by_name_for_user_id)
async def get_catalog_by_name_for_user_id(user_id: str, catalog_name: str):
    await validateUser(user_id)
    return await catalog_service_v1.get_all_catalogs_of_user(user_id, catalog_name)

# Get all books list for a Catalog for a given user
@router.get(urls.get_all_books_from_catalog_for_user_id)
async def get_all_books_from_catalog_for_user_id(user_id: str, catalog_name: str):
    await validateUser(user_id)
    return await catalog_service_v1.get_books_of_catalog(user_id, catalog_name)

# Create new Catalog
@router.post(urls.save_catalog_by_user_id)
async def save_catalog_by_user_id(user_id: str, catalog_data: CatalogSchema = Body(...)):
    await validateUser(user_id)
    return await catalog_service_v1.create_catalog(catalog_data)

# Update the book list in a catalog:
@router.put(urls.update_books_in_catalog_for_user_id)
async def update_books_in_catalog_for_user_id(user_id: str, catalog_name: str, books_list: list[str]):
    await validateUser(user_id)
    return await catalog_service_v1.update_books_to_catalog(user_id, catalog_name, books_list)

# Delete a Catalog by catalog name
@router.delete(urls.delete_catalog_by_name_for_user_id)
async def delete_catalog_by_name_for_user_id(user_id: str, catalog_name: str):
    await validateUser(user_id)
    return await catalog_service_v1.delete_catalog_by_name(user_id, catalog_name)

async def validateUser(user_id: str):
    user_found = await database.get_user_details_by_id(user_id)
    if user_found:
        logger.info('User details: {}'.format(user_found))
        return user_found
    else:
        logger.info("User with ID \'{}\' does not exist.".format(user_id))
        raise HTTPException(status_code=400, detail="User does not exists.")

