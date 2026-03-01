import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()