from krita import *
from PyQt5.QtWidgets import QMessageBox
import os
import subprocess

# https://docs.krita.org/en/user_manual/python_scripting/krita_python_plugin_howto.html

class MyExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("rustAction", "Rust plugin", "tools/scripts")
        action.triggered.connect(self.executePlugin)

    def executePlugin(self):
        # TODO: Write to stdin
        #   layer_width: u32(1)
        #   layer_height: u32(1)
        #   layer_data: u8(layer_width * layer_height * 4)
        manifest_path = os.path.dirname(__file__) + '/Cargo.toml'
        result = subprocess.run(['cargo', 'run', '--manifest-path', manifest_path], stdout=subprocess.PIPE)
        message = result.stdout.decode('utf-8')
        print('Rust plugin results: "' + message + '"')
        # TODO: Read from stdout
        #   layer_data: u8(layer_width * layer_height * 4)

Krita.instance().addExtension(MyExtension(Krita.instance()))
