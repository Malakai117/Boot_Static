from helper_funcs import *
import os
import sys

STATIC_PATH = "./static"
PUBLIC_PATH = "./docs"
CONTENT_PATH = "./content"
TEMPLATE_FILE = "./template.html"
BASE_PATH = "/"
if len(sys.argv) == 2:
    BASE_PATH = sys.argv[1]

def main():
    copy_static_to_public(src=STATIC_PATH, dst=PUBLIC_PATH)
    generate_pages_recursive(src_path= CONTENT_PATH,
                             template_path= TEMPLATE_FILE,
                             dst_path= PUBLIC_PATH,
                             base_path= BASE_PATH
                             )




if __name__ == "__main__":
    main()
