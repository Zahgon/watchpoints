# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .ast_monkey import ast_parse_node
from .watch_print import WatchPrint
import copy

try:
    import pandas as pd
except ImportError:  # pragma: no cover
    pd = None


class WatchElement:
    def __init__(self, frame, node, **kwargs):
        code = compile(ast_parse_node(node), "<string>", "exec")
        f_locals = frame.f_locals
        f_globals = frame.f_globals
        exec(code, f_globals, f_locals)
        self.frame = frame
        self.obj = f_locals.pop("_watchpoints_obj")
        self.prev_obj = self.obj
        self.prev_obj_repr = self.obj.__repr__()
        self.localvar = None
        self.parent = None
        self.subscr = None
        self.attr = None
        for var in ("_watchpoints_localvar", "_watchpoints_parent", "_watchpoints_subscr", "_watchpoints_attr"):
            if var in f_locals:
                setattr(self, var.replace("_watchpoints_", ""), f_locals.pop(var))
        self.alias = kwargs.get("alias", None)
        self.default_alias = kwargs.get("default_alias", None)
        self._callback = kwargs.get("callback", None)
        self.exist = True
        self.track = kwargs.get("track", ["variable", "object"])
        self.when = kwargs.get("when", None)
        self.deepcopy = kwargs.get("deepcopy", False)
        self.cmp = kwargs.get("cmp", None)
        self.copy = kwargs.get("copy", None)
        self.watch_print = kwargs.get("watch_print", WatchPrint())
        self.update()

    @property
    def track(self):
        pass

    @track.setter
    def track(self, val):
        pass

    def changed(self, frame):
        """
        :return (changed, exist):
        """
        pass

    def obj_changed(self, other):
        pass

    def update(self):
        pass

    def same(self, other):
        if type(other) is str:
            return self.alias and self.alias == other
        else:
            return other is self.obj

    def belong_to(self, lst):
        return any((self.same(other) for other in lst))
