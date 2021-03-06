# -*- coding: utf-8 -*-
"""
@author: Daniel Schreij

This file is part of QNotifications.

QNotifications is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

QNotifications is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GPLv3 License
along with this module.
"""

# Python3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
# from qtpy import QtWidgets, QtCore
from PyQt4 import QtCore, QtGui
import QNotifications

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"


class Example(QtCore.QObject):
    """
    Example showing off the notifications.

    :inherits: QtCore.QObject
    """
    # notify = QtCore.Signal(['QString', 'QString', int], ['QString', 'QString', int, 'QString'])
    notify = QtCore.pyqtSignal(['QString', 'QString', int], ['QString', 'QString', int, 'QString'])

    def __init__(self):
        super(Example, self).__init__()
        self.display_widget = self.__setup_widget()
        self.notification_area = self.__setup_notification_area(self.display_widget)
        self.display_widget.show()

    def __setup_widget(self):
        display_widget = QtGui.QWidget()  # QtWidgets.QWidget()
        display_widget.setGeometry(300, 100, 800, 500)
        display_widget.setLayout(QtGui.QVBoxLayout())  # QtWidgets.QVBoxLayout()

        inputLayout = QtGui.QFormLayout()  # QtWidgets.QFormLayout()
        inputLayout.setFieldGrowthPolicy(inputLayout.ExpandingFieldsGrow)

        # Notification message.
        # message_label = QtWidgets.QLabel("Send notification: ", display_widget)
        message_label = QtGui.QLabel("Send Notification: ", display_widget)
        # self.message_textbox = QtWidgets.QLineEdit(display_widget)
        self.message_textbox = QtGui.QLineEdit(display_widget)

        # Notification type
        # type_label = QtWidgets.QLabel("Notification type: ", display_widget)
        type_label = QtGui.QLabel("Notification type: ", display_widget)
        # self.type_dropdown = QtWidgets.QComboBox(display_widget)
        self.type_dropdown = QtGui.QComboBox(display_widget)
        self.type_dropdown.addItems(["primary", "success", "info", "warning", "danger"])

        # Notification duration.
        # duration_label = QtWidgets.QLabel("Display duration: (ms)", display_widget)
        duration_label = QtGui.QLabel("Display duration: (ms)", display_widget)
        # self.message_duration = QtWidgets.QSpinBox(display_widget)
        self.message_duration = QtGui.QSpinBox(display_widget)
        self.message_duration.setRange(500, 5000)
        self.message_duration.setValue(5000)
        self.message_duration.setSingleStep(50)

        # Entry effect
        # entryeffect_label = QtWidgets.QLabel("Entry effect: ", display_widget)
        entryeffect_label = QtGui.QLabel("Entry effect: ", display_widget)
        # self.entry_dropdown = QtWidgets.QComboBox(display_widget)
        self.entry_dropdown = QtGui.QComboBox(display_widget)
        self.entry_dropdown.addItems(["None", "fadeIn"])
        try:
            self.entry_dropdown.currentTextChanged.connect(self.__process_combo_change)
        except AttributeError:
            self.entry_dropdown.editTextChanged.connect(self.__process_combo_change)

        # Entry effect duration
        # self.entryduration_label = QtWidgets.QLabel("Effect duration: (ms)", display_widget)
        self.entryduration_label = QtGui.QLabel("Effect duration (ms): ", display_widget)
        # self.entryduration = QtWidgets.QSpinBox(display_widget)
        self.entryduration = QtGui.QSpinBox(display_widget)
        self.entryduration.setRange(100, 1000)
        self.entryduration.setSingleStep(50)

        # Exit effect
        # exiteffect_label = QtWidgets.QLabel("Exit effect: ", display_widget)
        exiteffect_label = QtGui.QLabel("Exit effect: ", display_widget)
        # self.exit_dropdown = QtWidgets.QComboBox(display_widget)
        self.exit_dropdown = QtGui.QComboBox(display_widget)
        self.exit_dropdown.addItems(["None", "fadeOut"])

        # Qt5
        try:
            self.exit_dropdown.currentTextChanged.connect(self.__process_combo_change)
        except AttributeError:
            self.exit_dropdown.editTextChanged.connect(self.__process_combo_change)

        # Exit effect duration
        # self.exitduration_label = QtWidgets.QLabel("Effect duration: (ms)", display_widget)
        self.exitduration_label = QtGui.QLabel("Effect duration: (ms)", display_widget)
        # self.exitduration = QtWidgets.QSpinBox(display_widget)
        self.exitduration = QtGui.QSpinBox(display_widget)
        self.exitduration.setRange(100, 1000)
        self.exitduration.setSingleStep(50)

        # self.buttontext_label = QtWidgets.QLabel("Button text", display_widget)
        self.buttontext_label = QtGui.QLabel("Button text: ", display_widget)
        # self.buttontext_textbox = QtWidgets.QLineEdit(display_widget)
        self.buttontext_textbox = QtGui.QLineEdit(display_widget)

        # Send button.
        # send_button = QtWidgets.QPushButton("Send", display_widget)
        send_button = QtGui.QPushButton("Send", display_widget)

        inputLayout.addRow(message_label, self.message_textbox)
        inputLayout.addRow(type_label, self.type_dropdown)
        inputLayout.addRow(duration_label, self.message_duration)
        inputLayout.addRow(entryeffect_label, self.entry_dropdown)
        inputLayout.addRow(self.entryduration_label, self.entryduration)
        inputLayout.addRow(exiteffect_label, self.exit_dropdown)
        inputLayout.addRow(self.exitduration_label, self.exitduration)
        inputLayout.addRow(self.buttontext_label, self.buttontext_textbox)
        inputLayout.addRow(QtGui.QWidget(), send_button)  # QtWidgets

        self.entryduration_label.setDisabled(True)
        self.entryduration.setDisabled(True)
        self.exitduration_label.setDisabled(True)
        self.exitduration.setDisabled(True)

        display_widget.layout().addWidget(QtGui.QLabel("<center><u><h1>QNotifications Example</h2></u></center>",
                                                       display_widget))  # QtWidgets
        display_widget.layout().addLayout(inputLayout)

        self.message_textbox.returnPressed.connect(send_button.click)
        self.buttontext_textbox.returnPressed.connect(send_button.click)
        send_button.clicked.connect(self.__submit_message)

        return display_widget

    def __setup_notification_area(self, target_widget):
        # notification_area = QNotifications.QNotificationArea(target_widget)
        notification_area = QNotifications.QNotificationArea(target_widget)

        self.notify['QString', 'QString', int].connect(notification_area.display)
        self.notify['QString', 'QString', int, 'QString'].connect(notification_area.display)

        return notification_area

    def __process_combo_change(self, val):
        if self.sender() == self.entry_dropdown:
            if val == "None":
                self.entryduration_label.setDisabled(True)
                self.entryduration.setDisabled(True)
            else:
                self.entryduration_label.setDisabled(False)
                self.entryduration.setDisabled(False)

        elif self.sender() == self.exit_dropdown:
            if val == "None":
                self.exitduration_label.setDisabled(True)
                self.exitduration.setDisabled(True)
            else:
                self.exitduration_label.setDisabled(False)
                self.exitduration.setDisabled(False)

    def __submit_message(self):
        text_value = self.message_textbox.text().strip()
        type_value = self.type_dropdown.currentText()

        if text_value:
            duration = self.message_duration.value()
            entry_effect = self.entry_dropdown.currentText()
            exit_effect = self.exit_dropdown.currentText()

            if entry_effect != "None":
                self.notification_area.setEntryEffect(entry_effect, self.entryduration.value())
            else:
                self.notification_area.setEntryEffect(None)

            if exit_effect != "None":
                self.notification_area.setExitEffect(exit_effect, self.exitduration.value())
            else:
                self.notification_area.setExitEffect(None)

            button_text = self.buttontext_textbox.text().strip()
            if button_text:
                self.notify['QString', 'QString', int, 'QString'].emit(text_value, type_value, duration, button_text)
            else:
                self.notify.emit(text_value, type_value, duration)

if __name__ == "__main__":
    # app = QtWidgets.QApplication(sys.argv)
    app = QtGui.QApplication(sys.argv)

    print('QNotifications Example.')
    print('PyQt Version:', QtCore.PYQT_VERSION_STR)

    # Enable High DPI display with PyQt5.
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    example = Example()

    exitcode = app.exec_()
    print("App exiting with code {}".format(exitcode))
    del(example)
    sys.exit(exitcode)

