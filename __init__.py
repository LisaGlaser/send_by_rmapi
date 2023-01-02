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
  actual_plugin       = 'calibre_plugins.send_by_rmapi.main:SendByrmapiAction'


  def is_customizable(self):
    '''
    This method must return True to enable customization via
    Preferences->Plugins
    '''
    return True

  def config_widget(self):
    '''
    A little config Widget
    '''
    from calibre_plugins.send_by_rmapi.config import ConfigWidget
    return ConfigWidget()

  def about(self):
    # Get the about text from a file inside the plugin zip file
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



    