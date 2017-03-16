#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Doc."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import sublime

from base_utils import sys_info


class StPanel:
    """."""

    def __init__(self, name='stino_panel'):
        """."""
        self._name = name
        self._panel = None
        self._texts = []
        self._windows = []
        self._panels = []
        self._creat_panel()

    def _creat_panel(self):
        """."""
        self._window = sublime.active_window()
        python_version = sys_info.get_python_version()
        if python_version < 3:
            panel = self._window.get_output_panel(self._name)
        else:
            panel = self._window.create_output_panel(self._name)

        if self._panel:
            vector = self._panel.layout_extent()
            panel.window_to_layout(vector)
        else:
            view = self._window.active_view()
            color_scheme = view.settings().get('color_scheme', '')
            if not color_scheme:
                color_scheme = 'Packages/Color Scheme - Default/Eiffel.tmTheme'
            panel.settings().set('color_scheme', color_scheme)
            panel.settings().set('word_wrap', True)

        self._panel = panel
        self._panel.set_name(self._name)

        if self._window not in self._windows:
            self._windows.append(self._window)
            self._panels.append(self._panel)

    def write(self, text='', quiet=False):
        """."""
        if not text.endswith('\n'):
            text += '\n'
        if len(self._texts) > 201:
            self._texts.pop(0)
        self._texts.append(text)

        mode = 'insert'
        window = sublime.active_window()
        if window != self._window:
            if window in self._windows:
                self._window = window
                index = self._windows.index(window)
                panel = self._panels[index]
                vector = self._panel.layout_extent()
                panel.window_to_layout(vector)
                self._panel = panel
            else:
                self._creat_panel()
            text = ''.join(self._texts)
            mode = 'replace'

        view = self._window.active_view()
        self._panel.set_read_only(False)
        self._panel.run_command('stino_panel_write',
                                {'text': text, 'mode': mode})
        if not quiet:
            panel_name = 'output.' + self._name
            self._window.run_command("show_panel", {"panel": panel_name})
        self._panel.set_read_only(True)
        self._window.focus_view(view)
