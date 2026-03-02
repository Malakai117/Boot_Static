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