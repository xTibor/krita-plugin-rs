#!/usr/bin/python3

from krita import *
from PyQt5.QtWidgets import QMessageBox
import os
import subprocess

# https://docs.krita.org/en/user_manual/python_scripting/krita_python_plugin_howto.html
# https://api.kde.org/extragear-api/graphics-apidocs/krita/libs/libkis/html/index.html

class MyExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("rustAction", "Rust plugin", "tools/scripts")
        action.triggered.connect(self.executePlugin)

    def executePlugin(self):
        doc = Krita.instance().activeDocument()
        if doc is not None:
            manifest_path = os.path.dirname(__file__) + '/Cargo.toml'
            process = subprocess.Popen(['cargo', 'run', '--manifest-path', manifest_path, '--', str(doc.width()), str(doc.height())], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(doc.pixelData(0, 0, doc.width(), doc.height()))

            message = process.communicate()[0].decode('utf-8')
            print('Rust plugin results: "' + message + '"')
            # TODO: Read from stdout
            #   layer_data: u8(layer_width * layer_height * 4)

Krita.instance().addExtension(MyExtension(Krita.instance()))
