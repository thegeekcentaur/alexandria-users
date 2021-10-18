__author__ = 'archanda'
__date__ = '31-Mar-2021'
__copyright__ = "Copyright 2021"
__credits__ = ["archanda"]
__license__ = "All rights reserved"
__version__ = "0.1"
__maintainer__ = "archanda"
__email__ = "2020mt93064@wilp.bits-pilani.ac.in"
__status__ = "dev"

# Book search APIs
get_book_details_by_isbn = "http://book-service:9000/books/api/books/isbn/{}"
get_book_details_by_author = "http://book-service:9000/books/api/books/author/{}"
get_book_details_by_genre = "http://book-service:9000/books/api/books/genre/{}"
get_book_details_by_publisher = "http://book-service:9000/books/api/books/publishers/{}"

# Catalog APIs
create_catalog_url = "http://catalogs-service:9000/catalogs/api/catalogs/local"
add_book_to_catalog_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/name/{}/{}"
update_books_to_catalog_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/name/{}/books"
delete_books_from_catalog_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/name/{}/books"
get_all_catalogs_of_user_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/name/{}"
get_books_of_catalog_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/books"
delete_catalog_by_name_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/name/{}"
get_all_catalogs_url = "http://catalogs-service:9000/catalogs/api/catalogs/local/all"

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