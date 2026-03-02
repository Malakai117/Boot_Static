import unittest

from htmlnode import LeafNode

class LeafNodeTest(unittest.TestCase):


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "This is a paragraph of text.")
        node3 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node3.to_html(), '<a href="https://www.google.com">Click me!</a>')



if __name__ == '__main__':
    unittest.main()