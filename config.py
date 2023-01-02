from calibre.utils.config import JSONConfig
from qt.core import QWidget, QFormLayout, QLabel, QLineEdit,QPushButton

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/send_by_rmapi')

# Set defaults
prefs.defaults['command_rmapi'] = 'rmapi'
prefs.defaults['folder_on_device'] = '/Books/Unread/Calibre'


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # creating line edits
        self.command = QLineEdit()
        self.command.setText(prefs['command_rmapi'])
    
        self.folder = QLineEdit()
        self.folder.setText(prefs['folder_on_device'])
        
        # creating a form layout
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(layout.AllNonFixedFieldsGrow)
        # adding rows
        layout.addRow(QLabel("Command to run rmapi"), self.command)
        layout.addRow(QLabel("The command you would type on the shell."))
        layout.addRow(QLabel("Folder on reMarkable to send files to:"), self.folder)
        ## this could also be a setting, a checkbox if we want to create non-existing folders
        layout.addRow(QLabel('If the folder does not exist rmapi will send an error.'),)
        self.setLayout(layout)


    def save_settings(self):
        prefs['command_rmapi'] = self.command.text()
        prefs['folder_on_device'] = self.folder.text()
