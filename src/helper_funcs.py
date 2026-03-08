import re
import os

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, BlockType



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                string = ""
                delimit = False
                i = 0
                while i < len(node.text):
                    if node.text[i:i+len(delimiter)] == delimiter:
                        if delimit:
                            if len(string) > 0:
                                new_node = TextNode(string, text_type)
                                results.append(new_node)
                            else:
                                raise ValueError("No Value between delimiters")
                            delimit = False
                            string = ""
                        else:
                            if len(string) > 0:
                                new_node = TextNode(string, TextType.TEXT)
                                results.append(new_node)
                            delimit = True
                            string = ""
                        i += len(delimiter) - 1
                    else:
                        string += node.text[i]
                    i += 1

                    if i == len(node.text):
                        if len(string) > 0:
                            if delimit:
                                raise ValueError("No Closing Delimiter")
                            if not delimit:
                                new_node = TextNode(string, node.text_type)
                                results.append(new_node)

            case _:
                results.append(node)
        #print(node)
    return results

def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                text = node.text
                delimits = extract_markdown_images(text)
                for delimit in delimits:
                    delimiter = f"![{delimit[0]}]({delimit[1]})"
                    split = text.split(delimiter, maxsplit=1)
                    if len(split[0]) > 0:
                        new_text_node = TextNode(text=split[0], text_type=TextType.TEXT)
                        results.append(new_text_node)
                    new_img_node = TextNode(text=delimit[0], text_type=TextType.IMAGE, url=delimit[1])
                    results.append(new_img_node)
                    text = split[1]
                if len(text) > 0:
                    new_text_node = TextNode(text=text, text_type=TextType.TEXT)
                    results.append(new_text_node)
            case _:
                results.append(node)
    return results

def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                text = node.text
                delimits = extract_markdown_links(text)
                for delimit in delimits:
                    delimiter = f"[{delimit[0]}]({delimit[1]})"
                    split = text.split(delimiter, maxsplit=1)
                    if len(split[0]) > 0:
                        new_text_node = TextNode(text=split[0], text_type=TextType.TEXT)
                        results.append(new_text_node)
                    new_link_node = TextNode(text=delimit[0], text_type=TextType.LINK, url=delimit[1])
                    results.append(new_link_node)
                    text = split[1]
                if len(text) > 0:
                    new_text_node = TextNode(text=text, text_type=TextType.TEXT)
                    results.append(new_text_node)
            case _:
                results.append(node)
    return results

def extract_markdown_images(text):
    if not text:
        return []
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    if not text:
        return []
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnode(text) -> list[TextNode]:
    if not text:
        raise ValueError("Need text to convert to textnode")
    nodes = [TextNode(text, TextType.TEXT)]

    for text_type in TextType:
        match text_type:
            case TextType.BOLD | TextType.ITALIC | TextType.CODE:
                nodes = split_nodes_delimiter(nodes, text_type.value, text_type)
                #print(f"After {text_type}: {nodes}")
            case TextType.IMAGE:
                nodes = split_nodes_image(nodes)
                #print(f"After {text_type}: {nodes}")
            case TextType.LINK:
                nodes = split_nodes_link(nodes)
                #print(f"After {text_type}: {nodes}")
            case TextType.TEXT:
                #print(f"After {text_type}: {nodes}")
                continue

    return nodes

def markdown_to_blocks(markdown_text) -> list[str]:
    if not markdown_text:
        raise ValueError("Need text to convert to blocks")
    blocks = markdown_text.split("\n\n")
    results = []
    for block in blocks:
        lines = block.splitlines()
        stripped_lines = [line.strip() for line in lines]
        block = "\n".join(line for line in stripped_lines if line)
        if block:
            results.append(block)
    return results

def block_to_block_type(block: str) -> BlockType:
    # Heading: 1-6 # chars followed by a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code block: starts with ``` + newline, ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.splitlines()

    # Quote: every line starts with >
    if lines and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if lines and all(line.startswith("- ") for line in lines):
        return BlockType.UN_LIST

    # Ordered list: lines start with 1. 2. 3. ... incrementing from 1
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered and lines:
        return BlockType.OR_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown_file: str) -> HTMLNode:
    if not markdown_file:
        raise ValueError("Need markdown_file to convert to html nodes")
    markdown_blocks = markdown_to_blocks(markdown_file)
    root_node = ParentNode(tag="div", children=[])

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                split = block.split(" ", 1)
                head = len(split[0])
                text_nodes = text_to_textnode(split[1])
                html_leaf_nodes = []
                for text_node in text_nodes:
                    html_leaf_nodes.append(text_node.text_node_to_html_node())
                tag = f"h{head}"
                block_html_parent = ParentNode(tag=tag, children=html_leaf_nodes)
                root_node.children.append(block_html_parent)

            case BlockType.CODE:
                striped = block[4:-3]
                node = TextNode(striped, TextType.CODE)
                code_html = node.text_node_to_html_node()
                code_parent_node = ParentNode(tag="pre", children=[code_html])
                root_node.children.append(code_parent_node)

            case BlockType.QUOTE:
                lines = block.splitlines()
                clean_lines = []
                for line in lines:
                    clean_line = line[1:].strip()
                    clean_lines.append(clean_line)
                cleaned_block = " ".join(clean_lines)
                text_nodes = text_to_textnode(cleaned_block)
                html_leaf_nodes = []
                for text_node in text_nodes:
                    html_leaf_nodes.append(text_node.text_node_to_html_node())

                quote_parent_node = ParentNode(tag="blockquote", children=html_leaf_nodes)
                root_node.children.append(quote_parent_node)

            case BlockType.OR_LIST:
                lines = block.splitlines()
                i = 1
                or_list_parent_node = ParentNode(tag="ol", children=[])

                for line in lines:
                    length = len(f"{i}. ")
                    i += 1
                    clean_line = line[length:].strip()
                    line_item_text_nodes = text_to_textnode(clean_line)
                    list_item_html_nodes = []
                    for text_node in line_item_text_nodes:
                        list_item_html_nodes.append(text_node.text_node_to_html_node())

                    list_item_parent_node = ParentNode(tag="li", children=list_item_html_nodes)
                    or_list_parent_node.children.append(list_item_parent_node)
                root_node.children.append(or_list_parent_node)

            case BlockType.UN_LIST:
                lines = block.splitlines()
                un_list_parent_nodes = ParentNode(tag="ul", children=[])

                for line in lines:
                    clean_line = line[2:].strip()
                    line_item_text_nodes = text_to_textnode(clean_line)
                    list_item_html_nodes = []
                    for text_node in line_item_text_nodes:
                        list_item_html_nodes.append(text_node.text_node_to_html_node())

                    list_item_parent_node = ParentNode(tag="li", children=list_item_html_nodes)
                    un_list_parent_nodes.children.append(list_item_parent_node)

                root_node.children.append(un_list_parent_nodes)

            case BlockType.PARAGRAPH:
                lines = block.splitlines()
                cleaned = " ".join(lines)
                text_nodes = text_to_textnode(cleaned)
                html_leaf_nodes = []
                for text_node in text_nodes:
                    html_leaf_nodes.append(text_node.text_node_to_html_node())
                paragraph_parent_node = ParentNode(tag="p", children=html_leaf_nodes)
                root_node.children.append(paragraph_parent_node)

    return root_node

def delete_directory(path) -> None:
    """Recursively deletes all contents of a directory."""
    if not os.path.exists(path):
        return

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            delete_directory(item_path)
            os.rmdir(item_path)
        else:
            os.remove(item_path)

def copy_directory(src, dst):
    """
    Recursively copies all contents from src directory to dst directory.

    Args:
        src: Source directory path
        dst: Destination directory path
    """
    os.makedirs(dst, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)
        else:
            with open(src_path, "rb") as src_file:
                with open(dst_path, "wb") as dst_file:
                    dst_file.write(src_file.read())
            print(f"Copied: {src_path} -> {dst_path}")

def copy_static_to_public(src="./static", dst="./public"):
    print(f"Deleting contents of '{dst}'...")
    delete_directory(dst)
    print(f"Copying '{src}' -> '{dst}'...")
    copy_directory(src, dst)
    print("Done.")

def extract_title(markdown) -> str:
    if not markdown:
        raise ValueError("Could not extract h1 Heading from markdown_file")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if re.match(r"(?<!#)# ", block):
                return block[1:].strip()
    raise ValueError("Could not extract h1 Heading from markdown_file")

def generate_page(src_path: str, template_path: str, dst_path: str) -> None:
    print(f"Generating Page From: '{src_path}' -> '{dst_path}':\nUsing Template: '{template_path}'...")

    with open(src_path, "r") as src:
        src_file = src.read()
    with open(template_path, "r") as template:
        template_file = template.read()

    html_root = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)
    temp_edit1 = template_file.replace("{{ Title }}", title)
    temp_edit2 = temp_edit1.replace("{{ Content }}", html_root)
    with open(dst_path, "w") as dst:
        dst.write(temp_edit2)

def generate_pages_recursive(src_path: str, template_path: str, dst_path: str) -> None:
    directories = os.listdir(src_path)
    for entry in directories:
        if os.path.isfile(os.path.join(src_path, entry)):
            if entry.endswith(".md"):
                dst_entry = entry.replace(".md", ".html")
                generate_page(os.path.join(src_path, entry), template_path, os.path.join(dst_path, dst_entry))
        else:
            os.makedirs(os.path.join(dst_path, entry), exist_ok=True)
            generate_pages_recursive(os.path.join(src_path, entry), template_path, os.path.join(dst_path, entry))

