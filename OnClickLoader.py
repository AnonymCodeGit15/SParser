def l_changed(obj):
    print("\r"+obj.text(),end='')


def submitForm(obj):
    print('Form Submitted')


def button_pressed(obj):
    print('Radio Button state changed')

def combo_index_changed(obj):
    print('Combobox changed to '+obj.currentText())