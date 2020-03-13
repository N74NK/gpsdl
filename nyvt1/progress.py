# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import time

# Progress bar from clint module

STREAM = sys.stderr
BAR_TEMPLATE = '  %s [%s%s]\r'
BAR_FILLED_CHAR = '-'
BAR_EMPTY_CHAR = ' '
ETA_INTERVAL = 1
ETA_SMA_WINDOW = 9

class Bar(object):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done()
        return False

    def __init__(self, label='', width=35, hide=None, empty_char=BAR_EMPTY_CHAR,
                 filled_char=BAR_FILLED_CHAR, expected_size=None, every=1):
        self.label = label
        self.width = width
        self.hide = hide
        if hide is None:
            try:
                self.hide = not STREAM.isatty()
            except AttributeError:  # output does not support isatty()
                self.hide = True
        self.empty_char =    empty_char
        self.filled_char =   filled_char
        self.expected_size = expected_size
        self.every =         every
        self.start =         time.time()
        self.ittimes =       []
        self.eta =           0
        self.etadelta =      time.time()
        self.etadisp =       self.format_time(self.eta)
        self.last_progress = 0
        if (self.expected_size):
            self.show(0)

    def show(self, progress, count=None):
        if count is not None:
            self.expected_size = count
        if self.expected_size is None:
            raise Exception("expected_size not initialized")
        self.last_progress = progress
        if (time.time() - self.etadelta) > ETA_INTERVAL:
            self.etadelta = time.time()
            self.ittimes = \
                self.ittimes[-ETA_SMA_WINDOW:] + \
                    [-(self.start - time.time()) / (progress+1)]
            self.eta = \
                sum(self.ittimes) / float(len(self.ittimes)) * \
                (self.expected_size - progress)
            self.etadisp = self.format_time(self.eta)
        x = int(self.width * progress / self.expected_size)
        if not self.hide:
            if ((progress % self.every) == 0 or      # True every "every" updates
                (progress == self.expected_size)):   # And when we're done
                STREAM.write(BAR_TEMPLATE % (
                    self.label, self.filled_char * x,
                    self.empty_char * (self.width - x)))
                STREAM.flush()

    def done(self):
        self.elapsed = time.time() - self.start
        elapsed_disp = self.format_time(self.elapsed)
        if not self.hide:
            STREAM.write(BAR_TEMPLATE % (
                self.label, self.filled_char * self.width,
                self.empty_char * 0))
            STREAM.write('\n')
            STREAM.flush()

    def format_time(self, seconds):
        return time.strftime('%Ss', time.gmtime(seconds))


def bar(it, label='', width=35, hide=None, empty_char=BAR_EMPTY_CHAR,
        filled_char=BAR_FILLED_CHAR, expected_size=None, every=1):
    count = len(it) if expected_size is None else expected_size

    with Bar(label=label, width=width, hide=hide, empty_char=BAR_EMPTY_CHAR,
             filled_char=BAR_FILLED_CHAR, expected_size=count, every=every) \
            as bar:
        for i, item in enumerate(it):
            yield item
            bar.show(i + 1)