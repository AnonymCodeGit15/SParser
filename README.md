# SParser

SParser is a Python-based tool that automatically generates a PyQt6 UI  with functioning elements using a custom DOM system with support for various Qt Widgets and two layouts.
## Features
 - **Widget Support** : Use various Qt elements such as `QLabel`, `QLineEdit`, `QComboBox`, and various other elements.  
 - **Event Handling Support** :  Supports handling events such as `onClick`,`onTextChanged`,`onToggled` and various other Qt widget events for supported widgets.
- **Script execution** : Support for running Python scripts specified in markup using a custom `<PyScript>` tag.
- **Layout Support** : `QGridLayout` and `QFormLayout` are currently supported.
## Installation
1. Clone the repository : 

```
git clone https://github.com/AnonymCodeGit15/SParser.git
cd SParser
```
2. Install the dependencies
`pip install -r requirements.txt`

3. Run `QtXMLParser.py` without arguments to load default test XML file or run with argument  `--load_ui` to use custom XML files.

## Usage 
`python QtXMLParser.py --load_ui myUIFile.xml`
## XML Markup Tag Table
| Qt Widget    | Markup Tag      | Supported Attributes                    |
|--------------|-----------------|-----------------------------------------| 
| QLabel       | \<QLabel>       | id, text ,onclick ,row ,column          |
| QPushButton  | \<QButton>      | id, text ,onclick ,row ,column          |
| QRadioButton | \<QRadioButton> | id, text ,onclick ,row ,column          |
| QLineEdit    | \<LineText>     | id ,ontextchanged , row ,column         |
| QComboBox    | \<QComboBox>    | id ,oncurrentindexchanged , row ,column |
| QCheckBox    | \<QCheckBox>    | id, text ,statechanged ,row ,column     |
### Custom Markup Tags
| Markup Tag  | Usage                                      | Supported Attributes |
|-------------|--------------------------------------------| ------- | 
| \<PyScript> | Runs Python Script in global scope         | id ,src
| \<ui>       | UI File                                    | |
| \<window>   | Set Window dimensions and other attributes | title ,width ,height ,iconfile |
> [!NOTE]
> The script specified in the PyScript tag can be used to define the onclick functions with the widget object passed as a specially named parameter.

> [!WARNING]
> The script file specified in the PyScript tag is loaded directly allowing execution of any arbitrary python file.

| Qt Widget    | Parameter Name |
|--------------| ------- |
| QPushButton  | button |
| QCheckBox    | button |
| QRadioButton | button |
| QLineEdit    | l_e |
| QComboBox    | combobox   |

## Example UI File with Grid Layout
```
<ui>
    <window title="Test Window" width="500" height="600" iconfile="SParser.png">
        <PyScript src="OnClickLoader.py" id="1"/>
        <layout type="grid">
            <QLabel row="0" column="0" text="Name:"/>
            <LineText row="0" column="1" id="name" ontextchanged="l_changed(l_e)"/>
            <QLabel row="1" column="0" id="User_ID" text="User ID"/>
            <LineText row="1" column="1" id="idno" ontextchanged="l_changed(l_e)"/>
            <QButton row="2" column="0" columnspan="2" text="Submit" onclick="submitForm(button)"/>
            <QRadioButton row="3" column="0" id="qradio0" text="Testing" onclick="button_pressed(button)"/>
            <QComboBox row="4" column="0" id="qcombo0" items="['Apple','Banana','Orange']" oncurrentindexchanged="combo_index_changed(combobox)"/>
            <QCheckBox row="4" column="1" id="qcheck0" text="Checkbox" onstatechanged="check_box_changed(button)"/>
        </layout>
    </window>
</ui>
```
## Example UI File with Form Layout
```
<ui>
    <window title="Test Window" width="500" height="600" iconfile="SParser.png">
        <PyScript src="OnClickLoader.py" id="1"/>
        <layout type="form">
            <row>
                <Qlabeltext text="Name"/>
                <LineText id="lt01" ontextchanged="l_changed(l_e)"/>
            </row>
            <row>
                <Qlabeltext text="User_ID"/>
                <LineText id="lt02" ontextchanged="l_changed(l_e)"/>
            </row>
            <row>
                <QButton text="Submit" onclick="submitForm(button)"/>
                <LineText id="lt03" ontextchanged="l_changed(l_e)"/>
            </row>
        </layout>
    </window>
</ui>
```

## Corresponding Example Script File
```
def l_changed(obj):
    print("\r"+obj.text(),end='')


def submitForm(obj):
    print('Form Submitted')


def button_pressed(obj):
    print('Radio Button state changed')

def combo_index_changed(obj):
    print('Combobox changed to '+obj.currentText())
```
## License
[GNU LGPLv3](https://choosealicense.com/licenses/lgpl-3.0/)
