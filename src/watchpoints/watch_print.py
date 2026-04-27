# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys
import threading
from objprint import objstr
import os.path
import zipfile


class WatchPrint:
    def __init__(self, file=sys.stderr, stack_limit=None, custom_printer=None):
        self.file = file
        self.stack_limit = stack_limit
        self.custom_printer = custom_printer

    def __call__(self, frame, elem, exec_info):
        p = self.printer
        p("====== Watchpoints Triggered ======")
        if threading.active_count() > 1:
            curr_thread = threading.current_thread()
            p(f"---- {curr_thread.name} ----")
        p("Call Stack (most recent call last):")

        curr_frame = frame.f_back
        frame_counter = 0
        trace_back_data = []
        while curr_frame and (self.stack_limit is None or frame_counter < self.stack_limit - 1):
            trace_back_data.append(self._frame_string(curr_frame))
            curr_frame = curr_frame.f_back
            frame_counter += 1

        for s in trace_back_data[::-1]:
            p(s)

        p(self._file_string(exec_info))
        if elem.alias:
            p(f"{elem.alias}:")
        elif elem.default_alias:
            p(f"{elem.default_alias}:")
        p(elem.prev_obj)
        p("->")
        p(elem.obj)
        p("")

    def _file_string(self, exec_info):
        pass

    def _frame_string(self, frame):
        pass

    def getsourceline(self, exec_info):
        pass

    def printer(self, obj):

        pass
