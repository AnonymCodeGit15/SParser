"""SParser XML Based Parser for PyQT6
Support for QLabel , QButton , QRadioButton and many more widgets.
"""
try:
    import time
    import os
    import sys
    import xml.etree.ElementTree as ET
    from PyQt6.QtWidgets import *
    from PyQt6.QtGui import QIcon
    import argparse
except Exception as err:
    print("Error loading modules.")
    print(f"Error : {str(err)}")
    print("Now Quitting in 3 seconds")
    time.sleep(3)
    sys.exit(0)


# TODO : Sanitize the PyScript Tag (Not safe)
# TODO : Add Multiple window support
def parse_xml(file) -> ET:
    """Parse Layout XML File"""
    tree = ET.parse(file)
    return tree.getroot()


# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--load_ui", "-U", type=str, help="Specify XML UI file", action="store")
args = parser.parse_args()
ui_load_from_file = False
ui_xml_file = ""
if args.load_ui != None:
    ui_xml_file = args.load_ui
    ui_load_from_file = True

glob_scope = globals()
scripting_disabled = False


def create_widget(element) -> QLabel | QPushButton | QRadioButton | QLineEdit | QComboBox | None:
    """Create all the widgets in our Layout"""
    if element.tag == 'QLabel':
        return QLabel(element.attrib['text'])
    elif element.tag == 'LineText':
        l_e = QLineEdit()
        if 'ontextchanged' in element.attrib:
            scope_up = locals()  # Get local scope to pass on to eval
            # We pass local and global scope to eval to successfully connect lineedit textchange to its respective
            # function
            l_e.textChanged.connect(lambda: eval(element.attrib['ontextchanged'], scope_up, glob_scope))
        return l_e



    elif element.tag == 'QButton':
        button = QPushButton(element.attrib['text'])
        if 'onclick' in element.attrib:
            scope_up = locals()
            button.clicked.connect(lambda: eval(element.attrib['onclick'], scope_up, glob_scope))
        return button
    elif element.tag == 'QRadioButton':
        button = QRadioButton(element.attrib['text'])
        if 'onclick' in element.attrib:
            scope_up = locals()
            button.clicked.connect(lambda: eval(element.attrib['onclick'], scope_up, glob_scope))
        if 'onchanged' in element.attrib:
            button.toggled.connect(lambda: eval(element.attrib['onchanged'], scope_up, glob_scope))
        return button
    elif element.tag == 'QComboBox':
        combobox = QComboBox()
        combo_items = eval(element.attrib["items"])
        if 'oncurrentindexchanged' in element.attrib:
            scope_up = locals()
            # Connect our combobox item change to respective function
            combobox.currentIndexChanged.connect(
                lambda: eval(element.attrib['oncurrentindexchanged'], scope_up, glob_scope))
        for combo_item in combo_items:
            combobox.addItem(combo_item)
        return combobox

    return None


# Keep track of element ids to avoid conflicts
script_element_id_list = []


def load_scripts(elements) -> None:
    """Load scripts from PyScript tag"""
    global script_element_id_list, glob_scope
    for element in elements:
        if element.attrib["id"] in script_element_id_list:
            raise Exception("Duplicate elements detected")
        if element.tag == 'PyScript':
            with open(element.attrib["src"], "r") as script_file:
                exec(script_file.read(), globals())  # Execute script in global scope
            script_element_id_list.append(element.attrib["id"])


def build_layout(element) -> QGridLayout | QFormLayout | None:
    """Builds based on the layout specified"""
    if element.tag == 'layout' and element.attrib['type'] == 'grid':
        layout = QGridLayout()
        for child in element:
            widget = create_widget(child)
            if widget:
                layout.addWidget(widget, int(child.attrib['row']), int(child.attrib['column']))
        return layout
    elif element.tag == 'layout' and element.attrib['type'] == 'form':
        layout = QFormLayout()
        form_row_lst = element.findall('row')
        for form_row in form_row_lst:
            if form_row.find("Qlabeltext") is None:
                s_but = create_widget(form_row.find('QButton'))
                layout.addRow(s_but)
                continue
            label = QLabel(form_row.find('Qlabeltext').attrib['text'])
            ledt = create_widget(form_row.find('LineText'))
            layout.addRow(label, ledt)

        return layout
    return None


def create_window(root) -> None:
    """Generate our window based on the layout received in XML"""
    app = QApplication([])
    window = QMainWindow()
    central_widget = QWidget()
    pre_script = root.findall('window/PyScript')
    if not scripting_disabled:
        load_scripts(pre_script)
    layout = build_layout(root.find('window/layout'))
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.setWindowTitle(root.find('window').attrib['title'])
    window.setWindowIcon(QIcon(root.find('window').attrib['iconfile']))
    window.setGeometry(500, 500, int(root.find('window').attrib['width']), int(root.find('window').attrib['height']))
    window.show()
    app.exec()


# Check if custom UI file is specified ,otherwise just loading default XML file.
if ui_load_from_file:
    root = parse_xml(ui_xml_file)
else:
    root = parse_xml('TestGridUi01.xml')
create_window(root)
sys.exit(0)
