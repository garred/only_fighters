from pgu import gui

widget = gui.Button("Testing")

app = gui.App(theme = gui.Theme('clean'))
app.connect(gui.QUIT, app.quit, None)

app.run(widget=widget)