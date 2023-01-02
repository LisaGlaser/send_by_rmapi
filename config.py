from calibre.utils.config import JSONConfig
from qt.core import QWidget, QHBoxLayout, QLabel, QLineEdit,QPushButton

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/send_by_rmapi')

# Set defaults
## default_site_customization = 'rmapi ; /Books/Unread/Calibre;EPUB,PDF ; 1'
prefs.defaults['command_rmapi'] = 'rmapi'
prefs.defaults['folder_on_device'] = '/Books/Unread/Calibre'


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.l = QHBoxLayout()
        self.setLayout(self.l)

        self.label = QLabel('Command to run rmapi:')
        self.l.addWidget(self.label)

        self.msg0 = QLineEdit(self)
        self.msg0.setText(prefs['command_rmapi'])
        self.l.addWidget(self.msg0)
        self.label.setBuddy(self.msg0)


        self.l.addSpacing(5)
        self.label = QLabel('Folder on reMarkable to send files to:')
        self.l.addWidget(self.label)

        self.msg1 = QLineEdit(self)
        self.msg1.setText(prefs['folder_on_device'])
        self.l.addWidget(self.msg1)
        self.label.setBuddy(self.msg1)


    def save_settings(self):
        prefs['command_rmapi'] = self.msg0.text()
        prefs['folder_on_device'] = self.msg1.text()
