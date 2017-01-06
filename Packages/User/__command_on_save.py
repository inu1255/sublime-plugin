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

BAIDU_AC = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=%s&json=1&p=3&sid=1431_19034_21121_17001_20718&req=2&csor=2&cb=jQuery110208435955665111006_1483665242750&_=1483665242754"
import urllib,json

class BaiduAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        name = view.file_name()
        if (not name.lower().endswith('.md')):
            return
        keyword = urllib.parse.quote(prefix)
        # print(BAIDU_AC % keyword)
        resp = urllib.request.urlopen(BAIDU_AC % keyword)
        data = str(resp.read()[42:-2],"gbk")
        # print(data)
        p = json.loads(data)
        sugs = [ [prefix+"("+s+")",s] for s in p["s"]]
        return sugs
