from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
    TEXT = ""
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "["
    IMAGE = "!"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def text_node_to_html_node(self):
        match self.text_type:
            case (TextType.TEXT):
                return LeafNode(tag=None, value=self.text)
            case (TextType.BOLD):
                return LeafNode(tag="b", value=self.text)
            case (TextType.ITALIC):
                return LeafNode(tag="i", value=self.text)
            case (TextType.CODE):
                return LeafNode(tag="code", value=self.text)
            case (TextType.LINK):
                return LeafNode(tag="a", value=self.text, props=self.url)
            case (TextType.IMAGE):
                return LeafNode(tag="img", value=self.text, props=self.url)
            case _:
                return None






    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"



