import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode
from helper_funcs import split_nodes_delimiter



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

if __name__ == "__main__":
    unittest.main()