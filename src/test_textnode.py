import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from helper_funcs import *



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.TEXT)
        node4 = TextNode("This is different", TextType.BOLD)
        node5 = TextNode("This is different", TextType.TEXT, url= "fakeasfuck")
        node6 = TextNode("This is different", TextType.TEXT, url= "fakeasfuck")

        self.assertEqual(node, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node4)
        self.assertNotEqual(node4, node5)
        self.assertEqual(node5, node6)
        self.assertNotEqual(node5, node3)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        leaf_node = LeafNode(value="This is a text node", tag=None)
        self.assertEqual(leaf_node, node.text_node_to_html_node())

    def test_delimiter(self):

        node1 = TextNode("This is a text node with a `code block` in it.", TextType.TEXT)
        node1_comp1 = TextNode("This is a text node with a ", TextType.TEXT)
        node1_comp2 = TextNode("code block", TextType.CODE)
        node1_comp3 = TextNode(" in it.", TextType.TEXT)

        result1 = split_nodes_delimiter([node1], "`", TextType.CODE)
        comp_list1 = [node1_comp1, node1_comp2, node1_comp3]
        self.assertEqual(result1, comp_list1)

        node2 = TextNode("This is a text node with a _italic block_ in it.", TextType.TEXT)
        node2_comp1 = TextNode("This is a text node with a ", TextType.TEXT)
        node2_comp2 = TextNode("italic block", TextType.ITALIC)
        node2_comp3 = TextNode(" in it.", TextType.TEXT)

        result2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        comp_list2 = [node2_comp1, node2_comp2, node2_comp3]
        self.assertEqual(result2, comp_list2)

        node3 = TextNode("This is a text node with a _italic block_ in it, and a _second_ one in it.", TextType.TEXT)
        node3_comp1 = TextNode("This is a text node with a ", TextType.TEXT)
        node3_comp2 = TextNode("italic block", TextType.ITALIC)
        node3_comp3 = TextNode(" in it, and a ", TextType.TEXT)
        node3_comp4 = TextNode("second", TextType.ITALIC)
        node3_comp5 = TextNode(" one in it.", TextType.TEXT)

        result3 = split_nodes_delimiter([node3], "_", TextType.ITALIC)
        comp_list3 = [node3_comp1, node3_comp2, node3_comp3, node3_comp4, node3_comp5]
        self.assertEqual(result3, comp_list3)

        node_list1 = [node2, node3]
        list_result = split_nodes_delimiter(node_list1, "_", TextType.ITALIC)
        list1_comp = comp_list2 + comp_list3
        self.assertEqual(list_result, list1_comp)

        node4 = TextNode("This is a text node with a **Bold Block** in it.", TextType.TEXT)
        node4_comp1 = TextNode("This is a text node with a ", TextType.TEXT)
        node4_comp2 = TextNode("Bold Block", TextType.BOLD)
        node4_comp3 = TextNode(" in it.", TextType.TEXT)

        result4 = split_nodes_delimiter([node4], "**", TextType.BOLD)
        comp_list4 = [node4_comp1, node4_comp2, node4_comp3]
        self.assertEqual(result4, comp_list4)

class TestExtractMarkdowns(unittest.TestCase):
    def test_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_links(text)
        self.assertEqual(2, len(matches))
    def test_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_images(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT, )
        node2 = TextNode("This is text with an ", TextType.TEXT)
        node3 = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node4 = TextNode(" and another ", TextType.TEXT)
        node5 = TextNode("![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)

        falsey_node1 = TextNode("", TextType.TEXT)
        falsey_node2 = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.BOLD)

        node_list = [node2, node3, node4, node5]
        falsey_list = [node2, falsey_node1, node3, falsey_node2, node4, node5]


        new_nodes1 = split_nodes_image([node1])
        new_nodes2 = split_nodes_image([node2])
        new_nodes3 = split_nodes_image([node3])
        new_nodes4 = split_nodes_image([node2, node3])
        new_nodes5 = split_nodes_image(node_list)
        new_nodes6 = split_nodes_image(falsey_list)

        new_falsey1 = split_nodes_image([falsey_node1])
        new_falsey2 = split_nodes_image([falsey_node2])

        node1_comp1 = TextNode("This is text with an ", TextType.TEXT)
        node1_comp2 = TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        node1_comp3 = TextNode(" and another ", TextType.TEXT)
        node1_comp4 = TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        comp1 = [node1_comp1, node1_comp2, node1_comp3, node1_comp4]
        comp2 = [node1_comp1, node1_comp2, node1_comp3, node1_comp4]

        self.assertListEqual(comp1, new_nodes1)
        self.assertListEqual([node1_comp1], new_nodes2)
        self.assertListEqual([node1_comp2], new_nodes3)
        self.assertListEqual([node1_comp1, node1_comp2], new_nodes4)
        self.assertListEqual(comp1, new_nodes5)
        self.assertListEqual(comp1, new_nodes6)
        self.assertEqual(new_falsey1, new_falsey2)

    def test_split_links(self):
        node1 = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        node2 = TextNode("This is text with an ", TextType.TEXT)
        node3 = TextNode("[image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node4 = TextNode(" and another ", TextType.TEXT)
        node5 = TextNode("[second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        node_list = [node2, node3, node4, node5]

        new_nodes1 = split_nodes_link([node1])
        new_nodes2 = split_nodes_link([node2])
        new_nodes3 = split_nodes_link([node3])
        new_nodes4 = split_nodes_link([node2, node3])
        new_nodes5 = split_nodes_link(node_list)

        node1_comp1 = TextNode("This is text with an ", TextType.TEXT)
        node1_comp2 = TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
        node1_comp3 = TextNode(" and another ", TextType.TEXT)
        node1_comp4 = TextNode("second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png")
        comp1 = [node1_comp1, node1_comp2, node1_comp3, node1_comp4]

        self.assertListEqual(comp1, new_nodes1)
        self.assertListEqual([node1_comp1], new_nodes2)
        self.assertListEqual([node1_comp2], new_nodes3)
        self.assertListEqual([node1_comp1, node1_comp2], new_nodes4)
        self.assertListEqual(comp1, new_nodes5)

class TestTextToNode(unittest.TestCase):
    def setUp(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_textnode(text)
        comp = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertListEqual(res, comp)

class TestTextToMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

if __name__ == "__main__":
    unittest.main()