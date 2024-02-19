import sys
from krita import *
import xml.etree.ElementTree as ET

def refersh(doc):
    root_node = doc.rootNode()
    if root_node and len(root_node.childNodes()) > 0:
        test_layer = doc.createNode("DELME", "paintLayer")
        root_node.addChildNode(test_layer, root_node.childNodes()[0])
        # QtCore.QTimer.singleShot(200, lambda: test_layer.remove() )
        test_layer.remove()
    doc.refreshProjection()


def make_v_text(layer, shape, scale=1):
    print(shape.name())
    print(shape.type())
    print("dx", shape.absoluteTransformation().dx())
    translation = shape.absoluteTransformation()
    scale_x = translation.m11()
    scale_y = translation.m22()
    print(scale_x, ", ", scale_y)
    pos = shape.position()
    print(pos.x())
    tree = ET.ElementTree(ET.fromstring(shape.toSvg()))
    xml_root = tree.getroot()
    print("root", xml_root)
    print(f"<{xml_root.tag}>")
    if xml_root.tag != "text":
        print("tag is not <text>!")
    print(xml_root.attrib)
    style_str = xml_root.attrib.pop("style", "")
    xml_root.set("writing-mode", "vertical-rl")
    styles = style_str.split(";")
    font_size: float = 10
    for style in styles:
        if style.startswith("font-size:"):
            styles.remove(style)
            print(style)
            parts = style.split(":")
            font_size_str = parts[1].strip()
            font_size = float(font_size_str)
    print("font size: ", font_size)
    # font_size = font_size * scale
    # font_size = int(font_size)
    xml_root.set("font-size", f"{font_size}")
    print(styles)
    xml_root.set("style", ";".join(styles))
    if "writing-mode" not in xml_root.attrib:
        print("no writing mode")
    else:
        write_mode = xml_root.attrib["writing-mode"]
        print(write_mode)
    child_index = 0
    max_text_len = 0
    for child in xml_root:
        print(child.tag, child.attrib)
        print(child.text.encode("utf-8"))
        if max_text_len < len(child.text):
            max_text_len = len(child.text)
        child.set("x", "0")
        child.set("dy", "0")
        child.set("y", "0")
        child.set("dx", f"-{child_index * font_size * 1.2}")
        child_index += 1
    new_svg_str = ET.tostring(xml_root, encoding="unicode")
    new_svg_str = f"<svg>{new_svg_str}</svg>"
    print(new_svg_str.encode("utf-8"))
    new_shape = layer.addShapesFromSvg(new_svg_str)[0]
    new_shape.setTransformation(shape.absoluteTransformation())
    print(new_shape)
    p = QPoint()
    p.setX(int(pos.x() + child_index * font_size / scale / scale_x))
    p.setY(int(pos.y() - max_text_len * font_size / scale * 2 * scale_y))
    print(p)
    print(pos)
    new_shape.setPosition(p)

    # old_o = layer.opacity()
    # layer.setOpacity(1)
    # layer.setOpacity(old_o)
    new_shape.select()
    shape.deselect()


def make_active_text_vertical():
    doc = Application.activeDocument()
    doc_root = doc.rootNode()

    active_node = doc.activeNode()

    print(active_node)

    if not (str(active_node.type()) == "vectorlayer"):
        print("Not vector layer!")
        return
    selected_shape = None
    for shape in active_node.shapes():
        if shape.isSelected():
            selected_shape = shape
            break
    if selected_shape is None:
        print("No shape selected!")
        return
    print(selected_shape.name())
    scale = doc.resolution() / 72
    print(doc.resolution())
    print(scale)
    make_v_text(active_node, selected_shape, scale)

    refersh(doc)
    doc.setActiveNode(active_node)