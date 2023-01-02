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
  #: This field defines the GUI plugin class that contains all the code
  #: that actually does something. Its format is module_path:class_name
  #: The specified class must be defined in the specified module.
  actual_plugin       = 'calibre_plugins.send_by_rmapi.main:SendByrmapiAction'


  def __init__(self, path_to_plugin):
    InterfaceActionBase.__init__(self, path_to_plugin)
    from calibre.customize.ui import customize_plugin,plugin_customization
    if not plugin_customization(self):
      customize_plugin(self, self.default_site_customization)
 
  def is_customizable(self):
    '''
    This method must return True to enable customization via
    Preferences->Plugins
    '''
    return True


  # def customization_help(self, gui=1):
  #   # this is rather ugly; more fields input would be nicer...
  #   message = []
  #   message.append( "This plugin uses rmapi")
  #   message.append( "Example (using the default values:\n" )
  #   message.append( "rmapi ; /Books/Unread/Calibre/;EPUB,PDF" )
  #   message.append( "You might need to restart Calibre for the changes to take effect." )
  #   return ''.join(message)

  def config_widget(self):
    '''
    Implement this method and :meth:`save_settings` in your plugin to
    use a custom configuration dialog.

    This method, if implemented, must return a QWidget. The widget can have
    an optional method validate() that takes no arguments and is called
    immediately after the user clicks OK. Changes are applied if and only
    if the method returns True.

    If for some reason you cannot perform the configuration at this time,
    return a tuple of two strings (message, details), these will be
    displayed as a warning dialog to the user and the process will be
    aborted.

    The base class implementation of this method raises NotImplementedError
    so by default no user configuration is possible.
    '''
    # It is important to put this import statement here rather than at the
    # top of the module as importing the config class will also cause the
    # GUI libraries to be loaded, which we do not want when using calibre
    # from the command line
    from calibre_plugins.send_by_rmapi.config import ConfigWidget
    return ConfigWidget()

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

  def save_settings(self, config_widget):
    '''
    Save the settings specified by the user with config_widget.

    :param config_widget: The widget returned by :meth:`config_widget`.
    '''
    config_widget.save_settings()
    ac = self.actual_plugin_
    if ac is not None:
      ac.config()



    