import threading
import os,re
import sublime,sublime_plugin
import subprocess

os.environ['GOPATH'] = os.environ["HOME"]+"/go"
def goInstall(iDir):
    try:
        # os.environ['GOPATH'] = os.environ["HOME"]+"/go"
        print (os.getcwd())
        o =  subprocess.Popen(["/usr/local/bin/go", "install"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p, err = o.communicate()
        print (p)
        print(err)
    except:
        return

# 保存时运行 go install 
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
            
# class GoGoDefCommand(sublime_plugin.TextCommand):
#     def run(self,edit):
#         view = self.view
#         view.run_command("gs_doc",{"mode":"goto"})
#         view.window().run_command("godef")

# 运行 go install
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

# BAIDU_AC = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=%s&json=1&p=3&sid=1431_19034_21121_17001_20718&req=2&csor=2&cb=jQuery110208435955665111006_1483665242750&_=1483665242754"
# import urllib,json
# # 百度找词,.md 时使用
# class BaiduAutocomplete(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
#         name = view.file_name()
#         if (not name.lower().endswith('.md')):
#             return
#         keyword = urllib.parse.quote(prefix)
#         # print(BAIDU_AC % keyword)
#         resp = urllib.request.urlopen(BAIDU_AC % keyword)
#         data = str(resp.read()[42:-2],"gbk")
#         # print(data)
#         p = json.loads(data)
#         sugs = [ [prefix+"("+s+")",s] for s in p["s"]]
#         return sugs

# 执行选中部分，并将输出按行替换
class SelectExecCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        view = self.view
        # run(ls)
        region = view.sel()[0]
        if region.a>region.b:
            region = sublime.Region(region.b,region.a)
        command = view.substr(region)
        if(command):
            iDir = re.sub("/[^/]+$","",view.file_name())
            os.chdir(iDir)
            line = view.line(region)
            a = sublime.Region(line.a,region.a)
            b = sublime.Region(region.b,line.b)
            a = view.substr(a).lstrip()
            b = view.substr(b).rstrip()
            # print(region.a,region.b)
            # print(">",a,b,"<")
            s = b+"\n"+a
            output = os.popen(command).read()
            output = output.replace("\n","$1"+s)[:-len(s)]
            view.run_command("insert_snippet",args={"contents": output})

class TestInuCommand(sublime_plugin.TextCommand):
    def run(self,edit):
        name = view.file_name()
        if (not name.lower().endswith('.go')):
            return
