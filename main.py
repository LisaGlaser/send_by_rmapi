import subprocess
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import error_dialog,info_dialog

class SendByrmapiAction(InterfaceAction):
  name = 'Send by rmapi'
  action_spec = (_('Send by rmapi'), None, None, _('Ctrl+Shift+S'))
  action_type = 'current'

  rmapi_path='rmapi'
  remote_dir='/Books/Unread/Calibre'
  formats=('epub','pdf')

  #def __init__(self, gui, site_customization):
    
    # InterfaceAction.__init__(self, gui, site_customization)
    # # parse the user's customized input
    # if site_customization:
    #   user_args = site_customization.split(';')
    #   user_args = [ usr_arg.strip()  for usr_arg in user_args ]
    #   if user_args:
    #     self.rmapi_path=user_args[0]
    #     self.remote_dir=user_args[1]
    
  def is_customizable(self):
    '''
    This method must return True to enable customization via
    Preferences->Plugins
    '''
    return True

  def config(self):
    # Apply the changes
    from calibre_plugins.send_by_rmapi.config import prefs
    self.rmapi_path=prefs['command_rmapi']
    self.remote_dir=prefs['folder_on_device']
    print("User configuration applied")


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
    ### in theory I could check if the error is that the folder does  not exist and create it but maybe not now

    for f,e in zip(files,errors):
        print(e)
    for f,e in zip(files,errors):
      error_dialog(self.gui, 'Cannot send book {}'.format(f),'rmapi sends an error \n {}'.format(e), show=True)

  #end of SendByrmapiAction class
  
