import PySimpleGUI as sg
import numpy as np
from matplotlib.widgets import RectangleSelector
import matplotlib.figure as figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

# instantiate matplotlib figure
fig = figure.Figure()
ax = fig.add_subplot(111)
DPI = fig.get_dpi()
fig.set_size_inches(505 * 2 / float(DPI), 707 / float(DPI))

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

def line_select_callback(eclick, erelease):
    global x1, x2
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata

    rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
    ax.add_patch(rect)
    fig.canvas.draw()

    return x1, x2

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

# ------------------------------- PySimpleGUI CODE

layout = [
    [sg.Button('Start', key='-START-')],
    [sg.Button('Cancel', key='-CANCEL-')],
    [sg.Button('Submit', key='-SUBMIT-')],
    [sg.Canvas(key='-CONTROLS_CV-')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='-FIG_CV-',
                       # it's important that you set this size
                       size=(500 * 2, 700)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.Text("Vertical axis: Time (sec) ; Horizontal axis: Displacement (X-dir, mm)")],
    [sg.Text("Press 'Start' to show plot. Then use the mouse to hover over the desired starting point. "
             "Then left click and drag the mouse to the desired stopping point. Then unclick and press 'Submit'.")]
]

window = sg.Window('Select Region of Interest (ROI)', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == '-CANCEL-' or event == sg.WIN_CLOSED:
        break
    elif event == '-START-':
        # Matlibplot of data
        #raw_x_plt = ax.plot(time, raw_x)
        x = np.linspace(0, 2 * np.pi)
        y = np.sin(x)
        line, = ax.plot(x, y)
        rs = RectangleSelector(ax, line_select_callback,
                               drawtype='box', useblit=False, button=[1],
                               minspanx=5, minspany=5, spancoords='pixels',
                               interactive=True)
        draw_figure_w_toolbar(window['-FIG_CV-'].TKCanvas, fig, window['-CONTROLS_CV-'].TKCanvas)

    elif event == '-SUBMIT-':
        x_time_start = x1
        x_time_stop = x2
        break

window.close()