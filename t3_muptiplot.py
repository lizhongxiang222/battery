'''
Created on 2017年8月20日

@author: rob
'''
# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import numpy as np
import pandas as pd
#py.sign_in('matterphiz', '3eu3YK0Rjn56EzoOWvgx')  #Streaming API Tokens:g5sptjri5x
dates = pd.date_range('20160101',periods=60) 
print(dates)
df = pd.DataFrame(np.random.rand(60,4),index=dates,columns=list('ABCD'))
        #    DataFrame 不可以小写
        #     np.random.rand(6,4),随机生成一个6*4的矩阵，其元素介于0-1之间
        #    index=dates 索引按照dates的日期元素作为索引
        #    columns=list('ABCD'),列名为A,B,C,D
print(df)
trace1 = go.Scatter(
    x=df.index,
    y=df['A'],
    name='yaxis1 data'
)
trace2 = go.Scatter(
    x=df.index,
    y=10*df['B'],
    name='yaxis2 data',
    yaxis='y2'
)
trace3 = go.Scatter(
    x=df.index,
    y=100*df['C'],
    name='yaxis3 data',
    yaxis='y3'
)
trace4 = go.Scatter(
    x=df.index,
    y=1000*df['D'],
    name='yaxis4 data',
    yaxis='y4'
)
data = [trace1, trace2, trace3, trace4]
layout = go.Layout(
    title='多轴数据示范',
    width=1280,
    xaxis=dict(
        domain=[20160101, 20160301]
    ),
    yaxis=dict(
        title='yaxis title',
        titlefont=dict(
            color='#1f77b4'
        ),
        tickfont=dict(
            color='#1f77b4'
        )
    ),
    yaxis2=dict(
        title='yaxis2 title',
        titlefont=dict(
            color='#ff7f0e'
        ),
        tickfont=dict(
            color='#ff7f0e'
        ),
        anchor='free',
        overlaying='y',
        side='left',
        position=0.15
    ),
    yaxis3=dict(
        title='yaxis4 title',
        titlefont=dict(
            color='#d62728'
        ),
        tickfont=dict(
            color='#d62728'
        ),
        anchor='x',
        overlaying='y',
        side='right'
    ),
    yaxis4=dict(
        title='yaxis5 title',
        titlefont=dict(
            color='#9467bd'
        ),
        tickfont=dict(
            color='#9467bd'
        ),
        anchor='free',
        overlaying='y',
        side='right',
        position=0.85
    )
)
fig = go.Figure(data=data, layout=layout)
#plot_url = py.plot(fig, filename='multiple-axes-multiple')
plot_url = plotly.offline.plot(fig)
