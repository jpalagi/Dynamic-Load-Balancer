import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask

app = Flask(__name__)


@app.route('/plot-server-cputime.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():
    fig = Figure()
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.set_ylabel('load')
    ax1.set_xlabel('time')
    ax1.set_title('Load vs Time')

    graph_data = open('plot_server_load.csv', 'r').read()
    lines = graph_data.split('\n')
    xs1 = []
    xs2 = []
    xs3 = []
    xs4 = []

    ys1 = []
    ys2 = []
    ys3 = []
    ys4 = []
    for line in lines[1:]:
        if len(line) > 1:
            d = line.split(',')
            if d[1] == 'S1':
                xs1.append(float(d[0]))
                ys1.append(float(d[2]))
            elif d[1] == 'S2':
                xs2.append(float(d[0]))
                ys2.append(float(d[2]))
            elif d[1] == 'S3':
                xs3.append(float(d[0]))
                ys3.append(float(d[2]))
            else:
                xs4.append(float(d[0]))
                ys4.append(float(d[2]))
    ax1.clear()
    ax1.plot(xs1, ys1, 'r*-', label='Server 1')
    ax1.plot(xs2, ys2, 'g+--', label='Server 2')
    ax1.plot(xs3, ys3, 'b^-.', label='Server 3')
    ax1.plot(xs4, ys4, 'mp:', label='Server 4')

    ax1.legend(loc='best')

    return fig


if __name__ == '__main__':
    app.run(debug=True)
