'''
Simple example showing:
- Change to a custom theme.
- Using Table widget to arrange the menu.
'''

from pgu import gui


if __name__ == '__main__':
    # Creating an App
    app = gui.Desktop(theme = gui.Theme('clean'))

    # Creating the widgets
    label1 = gui.Label('Mi super juego')
    #label1.background = gui.Color((255,255,255), width=100,height=100)
    button1 = gui.Button('Testing')
    button2 = gui.Button('Quit')

    # Adding widgets to a container
    container = gui.Table(width=500, height=500)
    container.tr(); container.td(label1)
    container.tr(); container.td(button1)
    container.tr(); container.td(gui.Spacer(10, 50))
    container.tr(); container.td(button2)

    # Enabling quit, connecting the "quit" button's click event to the app's quit function.
    button2.connect(gui.CLICK, app.quit, None)
    app.connect(gui.QUIT, app.quit, None) # Or clicking in the top-right corner

    # More things
    dialog = gui.Dialog(gui.Label('Hola mundo'), gui.Table(width=50, height=50))
    button1.connect(gui.CLICK, dialog.open, None)


    app.run(widget=container)