"""SParser XML Based Parser for PyQT6"""
try:
    import time
    import os
    import sys
    import xml.etree.ElementTree as ET
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import QIcon
except Exception as err:
    print("Error loading modules.")
    print("Now Quitting in 3 seconds")
    time.sleep(3)
    sys.exit(0)


# TODO : Add support for form layout
# TODO : Sanitize the PyScript Tag
# TODO : Add Multiple window support
# TODO : Add support for onTextChanged and for onChanged for radio buttons.

def parse_xml(file):
    tree = ET.parse(file)
    return tree.getroot()


def create_widget(element):
    """Create all the widgets in our Layout"""
    if element.tag == 'QLabel':
        return QLabel(element.attrib['text'])
    elif element.tag == 'LineText':
        return QLineEdit()
    elif element.tag == 'QButton':
        button = QPushButton(element.attrib['text'])
        button.clicked.connect(lambda: eval(element.attrib['onclick']))
        return button
    elif element.tag == 'QRadioButton':
        button = QRadioButton(element.attrib['text'])
        button.clicked.connect(lambda: eval(element.attrib['onclick']))
        return button

    return None


script_element_id_list = []


def load_scripts(elements):
    """Load scripts from PyScript tag"""
    global script_element_id_list
    for element in elements:
        if element.attrib["id"] in script_element_id_list:
            raise Exception("Duplicate elements detected")
        if element.tag == 'PyScript':
            with open(element.attrib["src"], "r") as script_file:
                exec(script_file.read(), globals())  # Execute script in global scope
            script_element_id_list.append(element.attrib["id"])


def build_layout(element) -> QGridLayout | QFormLayout:
    if element.tag == 'layout' and element.attrib['type'] == 'grid':
        layout = QGridLayout()
        for child in element:
            widget = create_widget(child)
            if widget:
                layout.addWidget(widget, int(child.attrib['row']), int(child.attrib['column']))
        return layout
    elif element.tag == 'layout' and element.attrib['type'] == 'form':
        layout = QFormLayout()
        # To be implemented
        return layout
    return None


def create_window(root) -> None:
    """Generate our window based on the layout received in XML"""
    app = QApplication([])
    window = QMainWindow()
    central_widget = QWidget()
    pre_script = root.findall('window/PyScript')
    load_scripts(pre_script)
    layout = build_layout(root.find('window/layout'))
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.setWindowTitle(root.find('window').attrib['title'])
    window.setWindowIcon(QIcon(root.find('window').attrib['iconfile']))
    window.setGeometry(500, 500, int(root.find('window').attrib['width']), int(root.find('window').attrib['height']))
    window.show()
    app.exec()


root = parse_xml('testui.xml')
create_window(root)
sys.exit(0)
