# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from bdb import BdbQuit
import inspect
import pdb
import sys
import threading
from .util import getargnodes
from .watch_element import WatchElement
from .watch_print import WatchPrint


class Watch:
    def __init__(self):
        self.watch_list = []
        self.tracefunc_stack = []
        self.enable = False
        self.set_lock = threading.Lock()
        self.tracefunc_lock = threading.Lock()
        self.restore()

    def __call__(self, *args, **kwargs):
        with self.set_lock:
            frame = inspect.currentframe().f_back
            argnodes = getargnodes(frame)
            for node, name in argnodes:
                self.watch_list.append(
                    WatchElement(
                        frame,
                        node,
                        alias=kwargs.get("alias", None),
                        default_alias=name,
                        callback=kwargs.get("callback", None),
                        track=kwargs.get("track", ["variable", "object"]),
                        when=kwargs.get("when", None),
                        deepcopy=kwargs.get("deepcopy", False),
                        cmp=kwargs.get("cmp", None),
                        copy=kwargs.get("copy", None),
                        watch_print=WatchPrint(
                            file=kwargs.get("file", self.file),
                            stack_limit=kwargs.get("stack_limit", self.stack_limit),
                            custom_printer=kwargs.get("custom_printer", self.custom_printer)
                        )
                    )
                )

            if not self.enable and self.watch_list:
                self.start_trace(frame)

            del frame

    def start_trace(self, frame):
        pass

    def stop_trace(self, frame):
        if self.enable:
            self.enable = False
            tf = self.tracefunc_stack.pop()
            while frame:
                frame.f_trace = tf
                frame = frame.f_back

            sys.settrace(tf)
            threading.settrace(tf)

    def unwatch(self, *args):
        if self.enable:
            frame = inspect.currentframe().f_back
            if not args:
                self.watch_list = []
            else:
                self.watch_list = [elem for elem in self.watch_list if not elem.belong_to(args)]

            if not self.watch_list:
                self.stop_trace(frame)

            del frame

    def config(self, **kwargs):
        pass

    def restore(self):
        pass

    def install(self, func="watch"):
        pass

    def uninstall(self, func="watch"):
        pass

    def tracefunc(self, frame, event, arg):
        pass

    def _default_callback(self, frame, elem, exec_info):
        pass
