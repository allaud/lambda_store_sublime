import sublime, sublime_plugin
import urllib
import json

settings = None

LIST_URL = '{}/list'
FUNC_URL = '{}/func/'

def resp(url):
    try:
        data = urllib.request.urlopen(url).read().decode("utf8")
        return json.loads(data)
    except Exception:
        return {}

class LambdaStoreInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, to_insert=""):
        self.view.insert(edit, self.view.sel()[0].begin(), to_insert)

class LambdaStoreCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.methods_list = resp(LIST_URL.format(settings.get('endpoint'))).get('functions', [])
        self.view.window().show_quick_panel(self.methods_list, lambda x:self.on_select(x))
    def on_select(self, index):
        if index < 0:
            return
        func_source = resp(FUNC_URL.format(settings.get('endpoint')) + self.methods_list[index]).get('func', '')
        self.view.run_command("lambda_store_insert", {'to_insert': func_source})

def plugin_loaded():
    global settings
    settings = sublime.load_settings('lambda_store.sublime-settings')

if int(sublime.version()) < 3000:
    plugin_loaded()
