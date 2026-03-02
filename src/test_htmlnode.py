import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node1 = HTMLNode(tag="test", value="test")
        node2 = HTMLNode(tag="test")
        node3 = HTMLNode(tag="test")
        node4 = HTMLNode(tag="test", value="test2")
        node5 = HTMLNode(props={"class": "test"})
        node6 = HTMLNode(props={"class": "test"})
        node7 = HTMLNode(props={"class": "testing"})
        node8 = HTMLNode(children=[node1, node2, node3])
        node9 = HTMLNode(children=[node4, node5])
        node10 = HTMLNode(children=[node4, node5])
        node11 = HTMLNode(tag="test", value="test_value", children=[node1, node2, node3, node4, node5], props={"class": "test"})
        node12 = HTMLNode(tag="test", value="test_value", children=[node1, node2, node3, node4, node5], props={"class": "test"})


        self.assertEqual(node2, node3)
        self.assertEqual(node5, node6)
        self.assertEqual(node9, node10)
        self.assertEqual(node11, node12)

        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node4, node5)
        self.assertNotEqual(node4, node6)
        self.assertNotEqual(node6, node7)
        self.assertNotEqual(node7, node8)
        self.assertNotEqual(node8, node9)



if __name__ == "__main__":
    unittest.main()