from textnode import  TextNode, TextType




def main():
    print("Hello World")

    dummy_node = TextNode("Where you at?", TextType.link)
    print(dummy_node.__repr__())



if __name__ == "__main__":
    main()
