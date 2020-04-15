#!/usr/bin/python3

from krita import *
import os
import subprocess

# https://docs.krita.org/en/user_manual/python_scripting/krita_python_plugin_howto.html
# https://api.kde.org/extragear-api/graphics-apidocs/krita/libs/libkis/html/index.html

class RustExtension(Extension):
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
            manifestPath = os.path.dirname(__file__) + '/Cargo.toml'
            process = subprocess.Popen(
                [
                    'cargo', 'run',
                    '--manifest-path', manifestPath,
                    '--',
                    str(doc.width()),
                    str(doc.height())
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE
            )
            process.stdin.write(doc.pixelData(0, 0, doc.width(), doc.height()))

            resultPixelData = process.communicate()[0]

            newLayer = doc.createNode("rustLayer", "paintLayer")
            newLayer.setPixelData(resultPixelData, 0, 0, doc.width(), doc.height())
            doc.rootNode().addChildNode(newLayer, None)
            doc.refreshProjection()

Krita.instance().addExtension(RustExtension(Krita.instance()))
