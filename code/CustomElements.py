from tkinter import *

class CustomText(Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.listes = list()
        self.colors = list()
        self.regs = list()

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

    def highlight_pattern_from_list(self, pattern_list, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        for pattern in pattern_list:
            start = self.index(start)
            end = self.index(end)
            self.mark_set("matchStart", start)
            self.mark_set("matchEnd", start)
            self.mark_set("searchLimit", end)
            count = IntVar()
            while True:
                index = self.search(pattern, "matchEnd","searchLimit",
                                    count=count, regexp=regexp)
                if index == "": break
                if count.get() == 0: break # degenerate pattern which matches zero-length strings
                self.mark_set("matchStart", index)
                self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.tag_add(tag, "matchStart", "matchEnd")

    def load_list(self, list, color, reg):
        self.listes.append(list)
        self.colors.append(color)
        self.regs.append(reg)

    def update(self):
        for i in range(len(self.listes)):
            self.highlight_pattern_from_list(self.listes[i], self.colors[i], regexp=self.regs[i])

###################################################################################################################################
