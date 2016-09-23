from pgu import gui
import os

widget = gui.Button("Testing")

app = gui.App(theme = gui.Theme('clean'))
app.init(widget=widget)
app.run()