__author__ = 'archanda'
__date__ = '31-Mar-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["archanda"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "archanda"
__email__ = "2020mt93064@wilp.bits-pilani.ac.in"
__status__ = "dev"

#Added By Surendar S BITs
#User Management APIs
get_all_users_url = "/api/user/local/all"
get_user_by_id_url = "/api/user/local/id/{user_id}"
save_user_url = "/api/user/local"
update_user_by_id_url = "/api/user/local/id/{user_id}"
delete_user_by_id_url = "/api/user/local/id/{user_id}"

#Search Books by user impersonation
search_book_by_user_id = "/api/user/{user_id}/book/search"

#APIs to perfrom catalog CRUD operations by user impersonation
get_all_catalog_for_user_id = "/api/user/{user_id}/catalog"
get_all_books_from_catalog_for_user_id = "/api/user/{user_id}/catalog/{catalog_name}/books"
get_catalog_by_name_for_user_id = "/api/user/{user_id}/catalog/{catalog_name}"
save_catalog_by_user_id = "/api/user/{user_id}/catalog/"
update_catalog_by_name_for_user_id = "/api/user/{user_id}/catalog/{catalog_name}"
update_books_in_catalog_for_user_id = "/api/user/{user_id}/catalog/{catalog_name}/books"
delete_catalog_by_name_for_user_id = "/api/user/{user_id}/catalog/{catalog_name}"