#!/usr/bin/env python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from calibre.customize import InterfaceActionBase
import subprocess
### actually using the gui
### customisations for the user

class ActionSendByrmapi(InterfaceActionBase):
  name                = 'Send by rmapi'
  description         = 'Send book(s) to the remarkable tablet using rmapi'
  supported_platforms = ['linux'] # Platform I tested this on
  author              = 'l glaser'
  version             = (0, 0, 5)

  default_site_customization = 'rmapi ; /Books/Unread/Calibre;EPUB,PDF ; 1'

  def __init__(self, path_to_plugin):
    InterfaceActionBase.__init__(self, path_to_plugin)
    from calibre.customize.ui import customize_plugin,plugin_customization
    if not plugin_customization(self):
      customize_plugin(self, self.default_site_customization)

  def customization_help(self, gui=1):
    # this is rather ugly; more fields input would be nicer...
    message = []
    message.append( "This plugin uses rmapi")
    message.append( "Example (using the default values:\n" )
    message.append( "rmapi ; /Books/Unread/Calibre/;EPUB,PDF" )
    message.append( "You might need to restart Calibre for the changes to take effect." )
    return ''.join(message)

  # def config_widget(self):
  #       '''
  #       Implement this method and :meth:`save_settings` in your plugin to
  #       use a custom configuration dialog.

  #       This method, if implemented, must return a QWidget. The widget can have
  #       an optional method validate() that takes no arguments and is called
  #       immediately after the user clicks OK. Changes are applied if and only
  #       if the method returns True.

  #       If for some reason you cannot perform the configuration at this time,
  #       return a tuple of two strings (message, details), these will be
  #       displayed as a warning dialog to the user and the process will be
  #       aborted.

  #       The base class implementation of this method raises NotImplementedError
  #       so by default no user configuration is possible.
  #       '''
  #       # It is important to put this import statement here rather than at the
  #       # top of the module as importing the config class will also cause the
  #       # GUI libraries to be loaded, which we do not want when using calibre
  #       # from the command line
  #       from calibre_plugins.send_by_rmapi.config import ConfigWidget
  #       return ConfigWidget()

  def about(self):
        # Get the about text from a file inside the plugin zip file
    # The get_resources function is a builtin function defined for all your
    # plugin code. It loads files from the plugin zip file. It returns
    # the bytes from the specified file.
    #
    # Note that if you are loading more than one file, for performance, you
    # should pass a list of names to get_resources. In this case,
    # get_resources will return a dictionary mapping names to bytes. Names that
    # are not found in the zip file will not be in the returned dictionary.
    text = get_resources('about.txt')
    QMessageBox.about(self, 'About the Interface Plugin Demo',
            text.decode('utf-8'))

  def load_actual_plugin(self, gui):
    from calibre.gui2.actions import InterfaceAction
    from calibre.gui2 import error_dialog,info_dialog


    class SendByrmapiAction(InterfaceAction):
      name = 'Send by rmapi'
      action_spec = (_('Send by rmapi'), None, None, _('Ctrl+Shift+S'))
      action_type = 'current'

      rmapi_path='rmapi'
      remote_dir='/Books/Unread/Calibre'
      formats=('epub','pdf')

      def __init__(self, gui, site_customization):
        
        InterfaceAction.__init__(self, gui, site_customization)
        # parse the user's customized input
        if site_customization:
          user_args = site_customization.split(';')
          user_args = [ usr_arg.strip()  for usr_arg in user_args ]
          if user_args:
            self.rmapi_path=user_args[0]
            self.remote_dir=user_args[1]
            try:
              self.formats=user_args[2].split(',')
            except:
              pass

      def genesis(self):
        self.qaction.triggered.connect(self.send_by_rmapi)

      def send_by_rmapi(self,  ):
        rows = self.gui.library_view.selectionModel().selectedRows()
        if not rows or len(rows) == 0:
            return error_dialog(self.gui, 'Cannot send books',
                             'No books selected', show=True)
        # Map the rows to book ids
        ids = list(map(self.gui.library_view.model().id, rows))
        count=0
        errors=[]
        files=[]
        for book_id in ids:
          count+=1
          print("Sending file {} of {}".format(count,len(ids)))
          path_to_file = None

          print('debug -1')
        
          for format in self.formats:
            try:
              path_to_file = self.gui.library_view.model().db.format_abspath(book_id, format, index_is_id=True)
            except:
              pass
            else:
              if path_to_file is not None:
                break
          # Confirm we have defined the path etc
          print("Ready to send {0} to {1}".format(path_to_file,self.remote_dir))
          p = subprocess.Popen(['rmapi','put',path_to_file,self.remote_dir],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
          out, err = p.communicate()
          print( "Standard Output:", out)
          print( "Standard Error Output:", err)
          print( "Return Code:", p.returncode)
          info=p.returncode
          ## if the transfer failed we will keep going, but save which file failed and why
          if not info == 0:
                errors.append(err)
                files.append(path_to_file.split('/')[-1])
        
        for f,e in zip(files,errors):
            print(e)
        for f,e in zip(files,errors):
          error_dialog(self.gui, 'Cannot send book {}'.format(f),'rmapi sends an error \n {}'.format(e), show=True)

    #end of SendByrmapiAction class

    return SendByrmapiAction(gui, self.site_customization)
