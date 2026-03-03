import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType



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
                continue
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
                continue
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

def text_to_textnode(text):
    if not text:
        raise ValueError("Need text to convert to textnode")
    nodes = [TextNode(text, TextType.TEXT)]

    for text_type in TextType:
        match text_type:
            case TextType.BOLD | TextType.ITALIC | TextType.CODE:
                nodes = split_nodes_delimiter(nodes, text_type.value, text_type)
            case TextType.IMAGE:
                nodes = split_nodes_image(nodes)
            case TextType.LINK:
                nodes = split_nodes_link(nodes)
            case TextType.TEXT:
                continue

    return nodes

def markdown_to_blocks(markdown_text):
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