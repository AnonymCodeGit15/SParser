def l_changed(obj):
    print("\r" + obj.text(), end='')


def submitForm(obj):
    print('Form Submitted')


def button_pressed(obj):
    print('Radio Button state changed')


def combo_index_changed(obj):
    print('Combobox changed to ' + obj.currentText())


def check_box_changed(obj):
    print('Check box state changed to ' + str(obj.isChecked()))


def slider_value_changed(obj):
    print('Slider value changed to ' + str(obj.value()))
