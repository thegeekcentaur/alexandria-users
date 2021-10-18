import motor.motor_asyncio
from bson.objectid import ObjectId

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# DB details
MONGO_DETAILS = "mongodb://mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.user_preferences
user_collection = database.get_collection("user_collection")
#database.catalog_collection.ensureIndex( { name: 1 }, { unique: true, sparse: true } )
# helpers

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
    logger.info("User details before Update: {}".format(current_user))
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
    logger.info("User details after Update: {}".format(user_updated))
    return user_updated.acknowledged  # returns true: if updated successfully
    
async def delete_user_by_id(user_id: str):
    user_to_be_deleted = await user_collection.find_one({"_id": user_id})
    logger.info("User to be deleted: {}".format(user_to_be_deleted))
    if user_to_be_deleted:
        logger.info("User [{}] is about to be deleted".format(user_to_be_deleted["name"]))
        await user_collection.delete_one({"_id": user_id})
        logger.info("Deleted User [{}]".format(user_to_be_deleted["name"]))
        return True
    return False
    