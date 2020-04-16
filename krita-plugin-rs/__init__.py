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
        if doc is None:
            return

        selection = doc.selection()
        if selection is not None:
            width, height = selection.width(), selection.height()
            sourcePixelData = doc.activeNode().pixelData(selection.x(), selection.y(), selection.width(), selection.height())
        else:
            width, height = doc.width(), doc.height()
            sourcePixelData = doc.pixelData(0, 0, doc.width(), doc.height())

        manifestPath = os.path.dirname(__file__) + '/Cargo.toml'
        process = subprocess.Popen(
            [
                'cargo', 'run',
                '--release',
                '--manifest-path', manifestPath,
                '--',
                str(width),
                str(height)
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=os.path.dirname(__file__)
        )
        process.stdin.write(sourcePixelData)

        resultPixelData = process.communicate()[0]
        if process.returncode != 0:
            return

        if selection is not None:
            doc.activeNode().setPixelData(resultPixelData, selection.x(), selection.y(), selection.width(), selection.height())
        else:
            newLayer = doc.createNode("rustLayer", "paintLayer")
            newLayer.setPixelData(resultPixelData, 0, 0, doc.width(), doc.height())
            doc.rootNode().addChildNode(newLayer, None)

        doc.refreshProjection()

Krita.instance().addExtension(RustExtension(Krita.instance()))
