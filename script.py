from flask import Flask,render_template
import datetime
from pandas_datareader import data
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)

@app.route('/plot/')
def plot():

    ### Starting and ending dates
    st = datetime.datetime(2019,10,11)
    en = datetime.datetime(2019,12,24)

    ### Gets the stock market data as a DataFrame
    df = data.DataReader(name="AAPL", data_source="yahoo", start=st, end=en)

    ### Creates the graph
    fig = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")

    ### Graph title
    fig.title.text = "Candlestick Chart"

    ### Graph and title features
    fig.grid.grid_line_alpha = 0.3
    fig.title.text_font_size = "30px"
    fig.title.align = "center"

    ### The function that compares opening and closing prices and evaluates them
    def inc_or_dec(c, o):
        if c > o:
            status = "Increase"
        elif c < o:
            status = "Decrease"
        else:
            status = "Equal"
        return status

    ### The column that shows the "Increase","Decrease" and "Equal" conditions in price
    df["Status"] = [inc_or_dec(c, o) for c, o in zip(df.Close, df.Open)]

    ### Y axis of "Increase" and "Decrease" rectangle graphs
    df["Middle"] = (df.Open + df.Close) / 2

    ### Height of "Increase" and "Decrease" rectangle graphs
    df["Height"] = abs(df.Open - df.Close)

    ### Width of "Increase" and "Decrease" rectangle graphs (as milliseconds)
    width = 12*60*60*1000

    ### Highest and lowest prices shown as segment graph
    fig.segment(df.index, df.High, df.index, df.Low, color="black")

    ### "Increase" rectangle graph
    fig.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], width, df.Height[df.Status=="Increase"], fill_color="#CCFFFF", line_color="black")

    ### "Decrease" rectangle graph
    fig.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], width, df.Height[df.Status=="Decrease"], fill_color="#E92121", line_color="black")

    ### Components of the graph
    script1, div1 = components(fig)

    ### Contains javascript files
    cdn_js = CDN.js_files[0]

    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)

### Home page
@app.route('/')
def home():
    return render_template("home.html")

### About page
@app.route('/about/')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)