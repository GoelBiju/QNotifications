# -*- coding: utf-8 -*-

# Python3 compatibility.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from qtpy import QtWidgets, QtGui, QtCore
from QNotifications.abstractions import *

__author__ = u"Daniel Schreij"
__license__ = u"GPLv3"


class MessageLabel(QtWidgets.QLabel):
    """
    Subclass of QLabel, which re-implements the resizeEvent() function.
    This is necessary because otherwise the notifications take up too much vertical
    space when texts they display become longer. This is because normally the height of a notification
    is calculated as the minimum height necessary for the text when the widget is horizontally re-sized to
    its minimum.

    :inherits: QtWidgets.QLabel
    """

    def resizeEvent(self, event):
        """

        :param self:
        :param event:
        """
        super(MessageLabel, self).resizeEvent(event)
        if self.wordWrap() and self.sizePolicy().verticalPolicy() == QtWidgets.QSizePolicy.Minimum:
            new_height = self.heightForWidth(self.width())
            # if new_height < 1:
            #     return
            if new_height >= 1:
                self.setMaximumHeight(new_height)


class QNotification(QtWidgets.QWidget):
    """
    Class representing a single notification

    :inherits: QtWidgets.QWidget
    """

    # PyQt signal for click on the notification's close button.
    closeClicked = QtCore.Signal()

    def __init__(self, message, category, timeout=None, button_text=None, *args, **kwargs):
        """

        :param message: str the message to show.
        :param category: dict{'primary', 'success', 'info', 'warning', 'danger'} the type of notification.
                         Adheres to the bootstrap standard class which are {primary, success, info, warning, danger}.
        :param timeout: int (default: None)
        :param button_text: (default: None)
        :param args:
        :param kwargs:
        """
        super(QNotification, self).__init__(*args, **kwargs)
        # Store instance variables
        self.message = message
        self.category = category
        self.timeout = timeout

        # Set Object name for reference.
        self.setObjectName(category)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.setContentsMargins(0, 0, 0, 0)
        # self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)

        # Create a message area.
        # contents = QtWidgets.QWidget(self)
        messageArea = QtWidgets.QHBoxLayout()
        messageArea.setContentsMargins(0, 0, 0, 0)

        # Create the layout
        self.message_display = MessageLabel()
        self.message_display.setObjectName("message")
        self.message_display.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.message_display.setWordWrap(True)

        # Create a button that can close notifications
        # if button_text in (None, u''):
        if button_text is None or button_text == u'':
            close_button = QtWidgets.QPushButton(u"\u2715")
        else:
            close_button = QtWidgets.QPushButton(button_text)
            close_button.setStyleSheet(u'text-decoration: underline;')

        close_button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        close_button.setFlat(True)
        close_button.setObjectName("closeButton")
        close_button.clicked.connect(self.closeClicked)

        # Add everything together.
        messageArea.addWidget(self.message_display)
        # messageArea.addStretch(1)
        messageArea.addWidget(close_button)
        self.layout().addLayout(messageArea)

        # Initialize some variables.
        # self.setStyle(category)
        self.setVisible(False)

        # Flag that is set if notification is being removed. This can be used to
        # make sure that even though the notification has not been really removed
        # yet (because it is for example in an fade out animation), it is in the
        # process of being removed.
        self.isBeingRemoved = False

        self.__init_graphic_effects()

    def __init_graphic_effects(self):
        """ Initializes graphic effects. """
        # Opacity effect for fade in/out.
        self.opacityEffect = QtWidgets.QGraphicsOpacityEffect(self)

        # Movement animation.
        # self.movementAnimation = QtCore.QPropertyAnimation(self, safe_encode("geometry"))

        # Fade in animation.
        self.fadeInAnimation = QtCore.QPropertyAnimation(self.opacityEffect, safe_encode("opacity"))
        self.fadeInAnimation.setStartValue(0.0)
        self.fadeInAnimation.setEndValue(1.0)

        # Fade out animation
        self.fadeOutAnimation = QtCore.QPropertyAnimation(self.opacityEffect, safe_encode("opacity"))
        self.fadeOutAnimation.setStartValue(1.0)
        self.fadeOutAnimation.setEndValue(0.0)

    def display(self):
        """ Displays the notification. """
        self.message_display.setText(self.message)
        self.show()
        self.raise_()

    def close(self):
        """ Closes the notification. """
        super(QNotification, self).close()
        self.deleteLater()

    def fadeIn(self, duration):
        """
        Fades in the notification.

        :param duration: int the desired duration of the animation.

        :raises: TypeError if duration is not an integer.
        """
        if type(duration) != int:
            raise TypeError("duration should be an integer")
        self.setGraphicsEffect(self.opacityEffect)
        self.fadeInAnimation.setDuration(duration)
        self.display()
        self.fadeInAnimation.start()

    def fadeOut(self, final_callback, duration):
        """
        Fades out the notification.

        :param final_callback: callable the function to call after the animation has finished
                                (for instance to clean up the notifications).
        :param duration: int the desired duration of the animation.

        :raises: TypeError if the wrong data-type is specified for any of the parameters.
        """
        if not callable(final_callback):
            raise TypeError("finishedCallback should be a callable")
        if type(duration) != int:
            raise TypeError("duration should be an integer")

        self.setGraphicsEffect(self.opacityEffect)
        self.fadeOutAnimation.setDuration(duration)
        self.fadeOutAnimation.finished.connect(lambda: final_callback(self))
        self.isBeingRemoved = True
        self.fadeOutAnimation.start()

    # def slideIn(self, duration):
    #     """
    #
    #     :param duration:
    #     :return:
    #     """

    # def slideOut(self, duration):
    #     """
    #
    #     :param duration:
    #     :return:
    #     """

    def paintEvent(self, pe):
        """
        Makes class QNotification available in style sheets.
        Redefinition of paintEvent, do not call directly (internal Qt function).
        """
        o = QtWidgets.QStyleOption()
        o.initFrom(self)
        p = QtGui.QPainter(self)
        self.style().drawPrimitive(QtWidgets.QStyle.PE_Widget, o, p, self)

    # Property attributes:
    @property
    def message(self):
        """ The currently set message to display. """
        return self._message

    @message.setter
    def message(self, value):
        """ Sets the message to display. """
        self._message = value

    @property
    def category(self):
        """ The currently set category of this notification. """
        return self._category

    @category.setter
    def category(self, value):
        """
        Sets the category of this notification.

        :param value : dict{'primary', 'success', 'info', 'warning', 'danger'} the category specification.

        :raises: ValueError if the category is other than one of the expected values.
        """
        allowed_values = ['primary', 'success', 'info', 'warning', 'danger']
        if value not in allowed_values:
            raise ValueError(u'\"{}\" is not a valid value. Should be one of {}'.format(value, str(allowed_values)))
        self._category = value
