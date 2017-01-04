import threading
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

class SaveAndInstall(sublime_plugin.EventListener):
    def on_post_save_(self, view):
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
            
class GoGoDefCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        view = self.view
        view.run_command("gs_doc",{"mode":"goto"})
        view.window().run_command("godef")

class GoGoInstallCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        view = self.view
        name = view.file_name()
        if (not name.lower().endswith('.go')):
            return
        iDir = re.sub("/[^/]+$","",name)
        os.chdir(iDir)
        t = threading.Thread(target=goInstall(iDir))
        t.daemon = True
        t.start() 