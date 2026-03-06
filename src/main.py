from helper_funcs import *
import os

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
SRC_FILE = "./content/index.md"
TEMPLATE_FILE = "./template.html"
DESTINATION_FILE = os.path.join(PUBLIC_PATH, "index.html")

def main():
    copy_static_to_public(STATIC_PATH, PUBLIC_PATH)
    generate_page(src_path=SRC_FILE, dst_path=DESTINATION_FILE, template_path=TEMPLATE_FILE)




if __name__ == "__main__":
    main()
