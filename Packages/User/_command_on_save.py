import threading
import time
import os
import re
import sublime_plugin
import subprocess
def goInstall(iDir):
    try:
        os.environ['GOPATH'] = os.environ["HOME"]+"/go"
        print (os.getcwd())
        o =  subprocess.Popen(["/usr/local/bin/go", "install"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p, err = o.communicate()
        print (p)
        print(err)
    except:
        return

class TrimTrailingWhiteSpace(sublime_plugin.EventListener):
    def on_post_save(self, view):
        name = view.file_name()
        if (not name.lower().endswith('.go')):
            return

        iDir = re.sub("/[^/]+$","",name)
        os.chdir(iDir)

        # If we don't have everything set then print a message and exit.
        # this doesn't take into account any environmental variables 
        # set outside of sublime, sorry.
        t = threading.Thread(target=goInstall(iDir))
        t.daemon = True
        t.start() 
            