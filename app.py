from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
import plotly.io as pio
from flask_socketio import SocketIO, emit
from model import *
import os
import hvplot.pandas  
import pandas as pd
import holoviews as hv
from holoviews import opts
import plotly.graph_objs as go

hv.extension('bokeh')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///manager.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)

class riskM(db.Model):
    sno = db.Column(db.Integer,primary_key=True)
    entryPrice = db.Column(db.Integer,nullable = False)
    takeProfit = db.Column(db.Integer,nullable = False)
    stopLoss = db.Column(db.Integer,nullable = False)
    #volume = db.Column(db.Integer,nullable=False)
    comission = db.Column(db.Integer,nullable=False)
    swap = db.Column(db.Integer,nullable=False)
    riskTollerance = db.Column(db.Integer,nullable=False)
    positionSize = db.Column(db.Integer,nullable=False)
    riskExposure = db.Column(db.Integer)
    riskRewardRatio = db.Column(db.Integer)
    senarioAExitPrice = db.Column(db.Integer)
    senarioAGrossProfit = db.Column(db.Integer)
    senarioANetProfit = db.Column(db.Integer)
    senarioBExitPrice = db.Column(db.Integer)
    senarioBGrossLoss = db.Column(db.Integer)
    senarioBNetLoss = db.Column(db.Integer)
    
    def __repr__(self)->str:
        return f"{self.sno} - {self.entryPrice} - {self.takeProfit} - {self.stopLoss} -  {self.comission} -{self.swap} -{self.riskTollerance} - {self.positionSize} -{self.riskExposure} -{self.riskRewardRatio} - {self.senarioAExitPrice} - {self.senarioAGrossProfit} - {self.senarioANetProfit} -{self.senarioBExitPrice} - {self.senarioBGrossLoss} - {self.senarioBNetLoss}"
        #{self.volume} -
@app.route('/',methods=['GET','POST'])
def hello_world():
    pie_chart_html = "" 
    ratio_figure_html= ""
    if request.method=='POST':
        entryPrice =float(request.form['entryPrice'])
        takeProfit =float(request.form['takeProfit'])
        stopLoss =float(request.form['stopLoss'])
        #volume =float(request.form['volume'])
        comission =float(request.form['comission'])
        swap =float(request.form['swap'])
        riskTolerance =float(request.form['riskTollerance'])
        positionSize = float(request.form['positionSize'])
        
        risk_tolerance = riskTolerance  # 2% risk tolerance
        position_size = positionSize    # 10% position size
        entry_price = entryPrice
        take_profit = takeProfit
        stop_loss = stopLoss
        Volume = position_size
        commission = comission
        Swap = swap
        
        potential_profit = model_profit.predict([[entry_price, stop_loss, take_profit]])[0]
        potential_loss = model_loss.predict([[entry_price, stop_loss, take_profit]])[0]
        
        # Calculate risk exposure based on position size
        risk_exposure = position_size * entry_price #* Volume
        
        # Calculate risk-reward ratio
        risk_reward_ratio = potential_profit / potential_loss
        
        
        # Initialize variables net_profit_a and net_loss_b
        
        net_profit_a = 0
        net_loss_b = 0
        
        # Scenario A (Take Profit is Hit)
        if potential_profit >= risk_exposure:
            net_profit_a = potential_profit - risk_exposure
        
        # Scenario B (Stop Loss is Hit)
        if potential_loss <= risk_exposure:
            net_loss_b = risk_exposure - potential_loss
        #pie chart simulation
        
        totalCapital = risk_exposure / risk_tolerance
        
        pie_chart_data = pd.DataFrame({
            'Category': ['RiskExposure', 'TotalCapital'],
            'Value': [risk_exposure, totalCapital]
        })
         # Create the pie chart using Plotly Express
        fig = px.pie(pie_chart_data, values='Value', names='Category',title='Risk Exposure vs Total Capital', width=400, height=400)
        # Save the pie chart as an HTML file
        pie_chart_html = fig.to_html(include_plotlyjs=False, full_html=False)
        file_path = os.path.join(app.root_path, 'static', 'pieChart.html')
        with open(file_path, 'w') as file:
            file.write(pie_chart_html)
            
        #bar graph simulation
        if net_loss_b == 0:
            x_values = ['Scenario A Exit Price', 'Scenario A Gross Profit', 'Scenario A Net Profit']
            y_values = [take_profit, potential_profit, net_profit_a]
        else:
            x_values = ['Scenario B Exit Price', 'Scenario B Gross Loss', 'Scenario B Net Loss']
            y_values = [stop_loss, potential_loss, net_loss_b]

        bar_data = {'Indicator': x_values, 'Amount': y_values}
        # Create the bar graph
        fig = px.bar(bar_data, x='Indicator', y='Amount', title='Simulation Result')
        # Convert the figure to HTML
        bar_graph_html = pio.to_html(fig, include_plotlyjs='cdn')
        # Define the file path within the static folder
        file_path = os.path.join(app.root_path, 'static', 'bar_graph.html')
        # Write the HTML to the file
        with open(file_path, 'w') as file:
            file.write(bar_graph_html)

        #scatter plot simulation
        
        # Create scatter plot and line plot
        #scatter_data = risk_m.query.first()  # Assuming you have a way to query the data
        scatter_data = pd.DataFrame([
        ['EntryPrice', entryPrice],
        ['TakeProfit', takeProfit],
        ['StopLoss', stopLoss],
        ['ScenarioAExitPrice', take_profit],
        ['ScenarioAGrossProfit', potential_profit],
        ['ScenarioANetProfit', net_profit_a],
        ['ScenarioBExitPrice', stop_loss],
        ['ScenarioBGrossLoss', potential_loss],
        ['ScenarioBNetLoss', net_loss_b],
        ], columns=['Attribute', 'Value'])

        scatter_plot = scatter_data.hvplot.scatter(
            x='Attribute',
            y='Value',
            title='Trade Parameters',
            ylabel='Amount',
            width=1200,
            height=400,
            color='blue',
        ).opts(opts.Scatter(size=8))  # Apply the Scatter style options

        

        
        # Define the file path within the static folder
        scatter_file_path = os.path.join(app.root_path, 'static', 'scatter_plot.html')

        # Save the scatter plot to the file
        hv.save(scatter_plot, scatter_file_path)

            
        #Tile simulation
        risk_reward_result = risk_reward_ratio   # Replace with the actual risk_reward_ratio value
        ratio_figure = go.Figure(data=[go.Indicator(
            mode="number+delta",
            value=risk_reward_result,
            title={"text": "Risk-to-Reward Ratio"},
        )])
           # Convert the figure to HTML using plotly.io
        ratio_figure_html = pio.to_html(ratio_figure, include_plotlyjs='cdn')
        
        risk_m = riskM(entryPrice = entryPrice,takeProfit = takeProfit ,stopLoss = stopLoss,comission = comission,swap =swap,riskTollerance = risk_tolerance, positionSize =positionSize  ,riskExposure = risk_exposure ,  riskRewardRatio = risk_reward_ratio ,senarioAExitPrice = take_profit,  senarioAGrossProfit = potential_profit,senarioANetProfit = net_profit_a , senarioBExitPrice = stop_loss , senarioBGrossLoss =potential_loss , senarioBNetLoss = net_loss_b)
        #   volume=volume,
        db.session.add(risk_m)
        db.session.commit()
    
        
    allRisk = riskM.query.all()
    return render_template('index.html',allRisk=allRisk, pie_chart_html=pie_chart_html, ratio_figure_html=ratio_figure_html  )

@app.route('/show')
def products():
    allRisk = riskM.query.all()
    print(allRisk)
    return 'this is products page'

@app.route('/delete/<int:sno>')
def delete(sno):
    risk = riskM.query.filter_by(sno=sno).first()
    db.session.delete(risk)
    db.session.commit()
    return redirect("/")


if __name__=="__main__":
    app.run()


 