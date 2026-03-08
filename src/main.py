from helper_funcs import *
import os

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
CONTENT_PATH = "./content"
SRC_FILE = "./content/index.md"
TEMPLATE_FILE = "./template.html"
DESTINATION_FILE = os.path.join(PUBLIC_PATH, "index.html")

def main():
    copy_static_to_public(src=STATIC_PATH, dst=PUBLIC_PATH)
    generate_pages_recursive(src_path=CONTENT_PATH, template_path=TEMPLATE_FILE, dst_path=PUBLIC_PATH)




if __name__ == "__main__":
    main()
