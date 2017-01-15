"""
An individual example of how to create single notification.

This is how it is described in the documentation of QNotifications
(http://dschreij.github.io/QNotifications/main.html#example).

Instead of using qtPy, I have decided to use the original PyQt4 library.
"""

import sys

from PyQt4 import QtGui, QtCore

from QNotifications import QNotificationArea


class NotificationsWidget(QtGui.QWidget):
    """ Example target widget for notifications. """

    notifications = QtCore.pyqtSignal(str, str, int)

    def __init__(self, parent=None):
        """

        """
        super(NotificationsWidget, self).__init__(parent)

        # Create a widget to render the notifications on.
        self.setWindowTitle('Notifications Widget')
        self.setGeometry(250, 150, 800, 50)

        # Create a new notifications area, and pass it the target widget.
        self.__notifications_area = QNotificationArea(self)

        # If we use the signal, we need to connect the functions.
        self.notifications.connect(self.__notifications_area.display)
        # self.notifications.emit('Initialised', 'info', 10000)

        # Show the target widget.
        self.show()

    def display_notification(self, message, duration=None, style='primary', fade_in=False, fade_out=False,
                             fade_in_duration=None, fade_out_duration=None):
        """
        Show a styled notification for the duration given to the function.

        :param message:
        :param duration:
        :param style:
        :param fade_in:
        :param fade_out:
        :param fade_in_duration:
        :param fade_out_duration:
        """
        # Handle effects for this notification.
        # if fade_in is True:
        #     self.__notifications_area.setEntryEffect('fadeIn', fade_in_duration)

        # if fade_out is True:
        #     self.__notifications_area.setExitEffect('fadeOut', fade_out_duration)

        self.__notifications_area.display(message, style, duration)

        # Make sure we disable the effects if they were enabled for this message.

# Create a QApplication to run the widget on its own.
app = QtGui.QApplication(sys.argv)
# Start the notifications widget.
target_widget = NotificationsWidget()

# Display a notification stating "Hey!" which has the style of "success" and lasts for 5 seconds.
target_widget.display_notification('Hey!', style='space-grey')

# Make sure script exits as soon as the application does.
sys.exit(app.exec_())
