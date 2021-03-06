import sublime, sublime_plugin, os, re

class WikiLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):        
        #find our current directory
        directory = os.path.split(self.view.file_name())[0]
        #find our current window
        window = self.view.window()
        slash = "\\" if sublime.platform() == "windows" else "/"
        #find the cursor
        location = self.view.sel()[0]
        
        #find the word under the cursor
        word = self.view.substr(self.view.word(location.a))
        
        #TODO: find a way to handle external links too; opening them in a browser window.
        #make sure the word under the cursor an internal link.

        internalLink = "link.internal.Wiki"
        if internalLink not in self.view.scope_name(location.a):
            #tell the user no
            sublime.status_message("WikiWords only, please.")
        else:
            #okay, we're good. Keep on keepin' on.        
            
            #compile the full file name and path.

            new_file = directory+slash+word+".wiki"
            #debug section: uncomment to write to the console
            # print "Location: %d" % location.a
            # print "Selected word is '%s'" % word
            # print "Full file path: %s" % new_file
            # print "Selected word scope is '%s'" % self.view.scope_name(location.a)
            # if internalLink in self.view.scope_name(location.a):
            #     print "this is an internal link"
            #end debug section

            if os.path.exists(new_file):
                #open the already-created page.
                new_view = window.open_file(new_file)
            else:
                #Create a new file and slap in the default text.
                new_view = window.new_file()
                new_edit = new_view.begin_edit()
                default_text = "{0}\nWrite about {0} here.".format(word)
                new_view.insert(new_edit,0,default_text)            
                new_view.end_edit(new_edit)
                new_view.set_name("%s.wiki" % word)
                new_view.set_syntax_file("Packages/Wiki/Wiki.tmLanguage")
