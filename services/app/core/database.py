import motor.motor_asyncio
from bson.objectid import ObjectId

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# DB details
MONGO_DETAILS = "mongodb://mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.user_preferences
books_collection = database.get_collection("books_collection")
catalog_collection = database.get_collection("catalog_collection")
user_collection = database.get_collection("user_collection")
#database.catalog_collection.ensureIndex( { name: 1 }, { unique: true, sparse: true } )
# helpers

def format_book(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "isbnID": book["isbnID"],
        "notes": book["notes"],
        "tags": book["tags"],
        "publisher": book["publisher"] # Added key 'publisher' - Arindam
    }

async def add_book(book_data: dict):
    book = await books_collection.insert_one(
        {"_id": ObjectId(), "title": book_data.title, "isbnID": book_data.isbnID, "notes": book_data.notes, "tags": book_data.tags,"publisher": book_data.publisher}
    # Added key 'publisher' - Arindam
    )
    new_book = await books_collection.find_one({"_id": book.inserted_id})
    return format_book(new_book)

# Added by ArchanaTBits
async def update_book_by_id(book_id:str, book_data: dict) -> dict:
    curr_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if curr_book is not None:
        logger.info("Book Exists")
        update_criteria = { "_id": ObjectId(book_id) }
        newvalues = {"$set": { "title": book_data.title if (book_data.title is not None and len(book_data.title) > 0) else curr_book.title ,
                             "isbnID": book_data.isbnID if (book_data.isbnID is not None  and len(book_data.isbnID) > 0) else curr_book.isbnID,
                             "notes": book_data.notes if (book_data.notes is not None  and len(book_data.notes) > 0) else curr_book.notes,
                              "tags": book_data.tags  if (book_data.tags is not None  and len(book_data.tags) > 0) else curr_book.tags} }
    book_updated = await books_collection.update_one(update_criteria, newvalues)
    return book_updated.acknowledged# returns true: if updated successfully

async def get_book(book_id: str) -> dict:
    curr_book = await books_collection.find_one({"_id": ObjectId(book_id)})
    return format_book(curr_book)

async def delete_book(book_id: str):
    book_deleted = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book_deleted:
        await books_collection.delete_one({"_id": ObjectId(book_id)})
    return True

async def retrieve_books():
    books = []
    async for curr_book in books_collection.find():
        books.append(format_book(curr_book))
    return books


#Catalog Operations added by ArchanaTBits
def format_catalog(catalog) -> dict:
    return {
        "catalog_name": catalog["name"],
        "user": catalog["user_id"],
        "description": catalog["description"],
        "books": catalog["books_list"]
    }

async def create_catalog(catalog_data: dict):
    catalog_names = []
    async for catalog in catalog_collection.find():
        catalog_names.append(catalog["name"])
    if catalog_data.name not in catalog_names:
        catalog = await catalog_collection.insert_one(
        { "name": catalog_data.name, "user_id": catalog_data.user_id, "description": catalog_data.description, "books_list": catalog_data.books_list})
    new_catalog = await catalog_collection.find_one({"name": catalog_data.name, "user_id": catalog_data.user_id})
    return format_catalog(new_catalog)

async def get_all_catalogs_of_user(user_id : str, catalog_name: str) -> dict:
    curr_catalog = await catalog_collection.find_one({"name": catalog_name,"user_id": user_id })
    return format_catalog(curr_catalog)

async def add_book_to_catalog(user_id : str, catalog_name:str, book_isbn_id: str) -> dict:
    curr_catalog = await catalog_collection.find_one({"name": catalog_name,"user_id": user_id})
    if curr_catalog is not None:
        logger.info("Catalog Exists")
        update_criteria = { "name": catalog_name,"user_id": user_id }
        curr_catalog["books_list"].append(book_isbn_id)
        newvalues = {"$set": { "name": curr_catalog["name"] ,
                                "user_id" : curr_catalog["user_id"],
                                "description": curr_catalog["description"] ,
                                "books_list": curr_catalog["books_list"]} }

    catalog_updated = await catalog_collection.update_one(update_criteria, newvalues)
    return catalog_updated.acknowledged

async def update_catalog_book_list(user_id : str, catalog_name:str, new_books_list: list) -> dict:
    curr_catalog = await catalog_collection.find_one({"name": catalog_name,"user_id": user_id})
    if curr_catalog is not None:
        logger.info("Catalog Exists")
        update_criteria = { "name": catalog_name,"user_id": user_id }
        for book_isbn_id in new_books_list:
            if book_isbn_id not in curr_catalog["books_list"]:
                curr_catalog["books_list"].append(book_isbn_id)
        newvalues = {"$set": { "name": curr_catalog["name"] ,
                                "user_id" : curr_catalog["user_id"],
                                "description": curr_catalog["description"] ,
                                "books_list": curr_catalog["books_list"]} }
    catalog_updated = await catalog_collection.update_one(update_criteria, newvalues)
    return catalog_updated.acknowledged

async def delete_catalog(user_id : str, catalog_name: str):
    catalog_available = await catalog_collection.find_one({"name": catalog_name, "user_id": user_id})
    if catalog_available:
        await catalog_collection.delete_one({"name": catalog_name, "user_id": user_id})
    return True

async def delete_books_from_catalog(user_id : str, catalog_name: str, books_remove_list: list):
    catalog_available = await catalog_collection.find_one({"name": catalog_name, "user_id": user_id})
    if catalog_available:
        new_books_list = [ele for ele in catalog_available["books_list"] if ele not in books_remove_list]
        update_criteria = { "name": catalog_name,"user_id": user_id }
        newvalues = {"$set": { "name": catalog_available["name"] ,
                                "user_id" : catalog_available["user_id"],
                                "description": catalog_available["description"] ,
                                "books_list": new_books_list} }
    catalog_updated = await catalog_collection.update_one(update_criteria, newvalues)
    return catalog_updated.acknowledged

async def retrieve_catalogs():
    catalogs = []
    async for curr_catalog in catalog_collection.find():
        catalogs.append(format_catalog(curr_catalog))
    return catalogs

async def retrieve_catalogs_for_user(user_id: str):
    catalogs_for_user = []
    async for curr_catalog in catalog_collection.find():
        if curr_catalog["user_id"] == user_id:
            catalogs_for_user.append(format_catalog(curr_catalog))
    return catalogs_for_user

#User management operations by Surendar S BITs

def format_user(user) -> dict:
    return {
        "user_id": user["_id"],
        "name": user["name"],
        "email": user["email"]
    }

async def get_all_user_details():
    users = []
    async for current_user in user_collection.find():
        logger.info("User : [{}]".format(current_user))
        users.append(format_user(current_user))
    return users

def get_user_id(user_name):
    return "user_{}".format(user_name.replace(" ", "").lower())

async def get_user_details_by_id(user_id: str):
    current_user = await user_collection.find_one({"_id": user_id})
    logger.info("Found User: [{}]".format(current_user))
    if current_user:
        return format_user(current_user)
    return current_user

async def is_user_name_already_taken(user_name) :
    current_user = await get_user_details_by_id(get_user_id(user_name))
    if current_user is not None:
        return True
    return False

async def add_user(user_details: dict):
    new_user_id = get_user_id(user_details.name)
    user = await user_collection.insert_one(
        {
            "_id": new_user_id,
            "name": user_details.name,
            "email": user_details.email
        }
    )
    new_user = await user_collection.find_one({"_id": new_user_id})
    return format_user(new_user)

async def update_user_by_id(user_id: str ,user_details: dict) -> dict:
    current_user = await user_collection.find_one({"_id": user_id})
    if current_user is not None:
        logger.info("User [{}] is found".format(user_details.name))
        update_criteria = { "_id": user_id }
        newvalues = {"$set":
                        {
                            "name": user_details.name if (user_details.name is not None  and len(user_details.name) > 0) else current_user.name,
                            "email": user_details.email if (user_details.email is not None and len(user_details.email) > 0) else current_user.email
                        }
                    }
    user_updated = await user_collection.update_one(update_criteria, newvalues)
    return user_updated.acknowledged  # returns true: if updated successfully
    
async def delete_user_by_id(user_id: str):
    user_to_be_deleted = await books_collection.find_one({"_id": user_id})
    if user_to_be_deleted:
        logger.info("User [{}] is about to be deleted".format(user_to_be_deleted.name))
        await books_collection.delete_one({"_id": user_id})
        logger.info("Deleted User [{}]".format(user_to_be_deleted.name))
    return True