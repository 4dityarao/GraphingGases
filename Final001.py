import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
class param:
  #object for different parameters' name and hazardous value 
  name='Null'
  haz='0'
def sendemail(defaulter,conc,time_data):
#email
    host="smtp.gmail.com"
    port=587
    username="industrysafetytechnovation@gmail.com"
    password="Technovation@123"
    from_email='industrysafetytechnovation@gmail.com'
    to_list=['2017.aditya.rao@ves.ac.in']
    message=MIMEMultipart("alternative")
    message['Subject']='Critical Emission Reported'
    message['From']=from_email
    message['To']=to_list[0]
    message_attach='Critical! Emission levels of '+str(defaulter.name)+' were '+str(conc)+' at '+str(time_data)+'.\nPlease make necessary changes to keep emissions below'+str(defaulter.haz)
    email_conn=smtplib.SMTP(host,port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(username,password)
    part1=MIMEText(message_attach,'plain')
    message.attach(part1)
    email_conn.sendmail(from_email,to_list,message.as_string())
    email_conn.quit()

app=dash.Dash()
   
colors = {
    'background': '#383838',
    'text': '#7FDBFF'
}

app.layout=html.Div(html.Div(children=[
    
    html.Div(html.H1('GAS CONCENTRATIONS'),style={'text-align':'center','color':'white','text-shadow':'2px 2px #ff0000','backgroundColor':colors['background']}),
    
   
    html.Div(children=html.Div(id='graphs'),style={'backgroundColor':'white'}),
    
    dcc.Interval(id='interval_div',interval=1000,n_intervals=1),
    ],style={'margin-left':'20%','margin-right':'20%'}),style={'backgroundColor': colors['background']})
    
 

@app.callback(Output('graphs','children'),
              [Input('interval_div','n_intervals')])
def update_graph(n):
 
  graphs=[]
  df=pd.read_csv('putty.csv',skiprows=[0,1],names=['Time','CO2','CO','Temperature','Humidity'])

  # print(df)
  df2=df.iloc[:n]
  #print(df2)


  parameters=[]
  for i in range(4):
    parameters.append(param())
  parameters[0].name='CO2'
  parameters[0].haz=500
  parameters[1].name='CO'
  parameters[1].haz=25
  parameters[2].name='Temperature'
  parameters[2].haz=30
  parameters[3].name='Humidity'
  parameters[3].haz=30



  '''if n<=df2['Time'].count():
    #calls email function
    for b in parameters:

      if df2[b.name].iloc[-1] >b.haz:
          
          defaulter=b
          conc=df2[b.name].iloc[-1]
          time_data=df2['Time'].iloc[-1]
          sendemail(defaulter,conc,time_data) '''
  for b in parameters:
    
  
    df_trace1=df2[df2[b.name]>b.haz]
    #print(df_trace1)
    trace1=go.Scatter(x=df_trace1['Time'],y=df_trace1[b.name],name='Hazardous Instance of '+b.name,
                        mode='markers',marker=dict(color='red',size=15))

    trace2=go.Scatter(x=df2['Time'],y=df2[b.name],
                       name='Concentrations of '+b.name,
                       mode='lines',
                       marker=dict(color='green'))
    data=[trace2,trace1]
    layout=go.Layout(title=b.name,xaxis={'title':'Time'},yaxis={'title':'Level of '+b.name},
      annotations=[dict(text='Highest Recorded Conc',x=df2['Time'][df2[b.name].idxmax()],y=df2[b.name].max(),bordercolor='red')]
      )

    
    fig=go.Figure(data=data,layout=layout)

    graphs.append(html.Div([html.H6('Mean Concentration of '+b.name+' : '+str(df[b.name].mean())),dcc.Graph(id=b.name,figure=fig)],style={'margin':'0px','padding':'0','border':'4px solid black','box-shadow':'5px 10px 8px 10px #888888'}))
  return graphs


'''external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({"external_url": js})
 
    app.css.append_css({
         "external_url":"https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
         })
    
    
    html.Img(
            src="file:///C:/Users/ankus/.spyder-py3/Safety.jpg",
            style={
                    'height':'10%',
                    'width':'10%',
                    'float':'right',
                    'position':'relative'},
                    ),'''
    
if __name__=='__main__':
    app.run_server()
