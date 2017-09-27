'''
Created on 2017年9月6日

@author: rob
'''
#设置中文字体
from pylab import *
#from traitsui.image.image import time_stamp_for
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

import pymysql.cursors
#import datetime
import plotly.graph_objs as go
import plotly
import pandas as pd
print('start')
colors = ['#8dd3c7','#d62728','#ffffb3','#bebada',
          '#fb8072','#80b1d3','#fdb462',
          '#b3de69','#fccde5','#d9d9d9',
          '#bc80bd','#ccebc5','#ffed6f'];

colorsX =['#1f77b4','#d62728','#9467bd','#ff7f0e']

'''
connection=pymysql.connect(
    host="10.8.240.20",port=3306,user="store",
    passwd="store",db="station_inspection",charset="utf8",
    cursorclass = pymysql.cursors.SSCursor)
'''
connection=pymysql.connect(
    host="localhost",port=3306,user="root",
    db="station_inspection",charset="utf8",
    cursorclass = pymysql.cursors.SSCursor)

cursor=connection.cursor()
BATCH_SIZE = 5000

timegap = "AND bc.time_stamp >='2017-07-30 18:00:00' \
        AND bc.time_stamp <='2017-07-30 19:00:00' "
     
queryBmu="SELECT id_group,id_station ,I_aver ,time_stamp \
        ,V_cell01 ,V_cell02 ,V_cell03 ,V_cell04 ,V_cell05 ,V_cell06 \
        ,V_cell07 ,V_cell08 ,V_cell09 ,V_cell10 ,V_cell11 ,V_cell12 \
        ,SOC_goup\
    FROM bess_group_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND (bc.id_cluster ='DT-DT-0831-26-BC02' )"  \
        + timegap+ \
        "ORDER BY bc.time_stamp" 
'''
queryBmu01="SELECT id_group ,I_aver ,time_stamp \
        ,V_cell01 ,V_cell02 ,V_cell03 ,V_cell04 ,V_cell05 ,V_cell06 \
        ,V_cell07 ,V_cell08 ,V_cell09 ,V_cell10 ,V_cell11 ,V_cell12 \
        ,SOC_goup\
    FROM bess_group_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND (bc.id_group=168311326260101 )"  \
        + timegap+ \
        "ORDER BY bc.time_stamp" 
        
queryBmu02="SELECT id_group ,I_aver ,time_stamp \
        ,V_cell01 ,V_cell02 ,V_cell03 ,V_cell04 ,V_cell05 ,V_cell06 \
        ,V_cell07 ,V_cell08 ,V_cell09 ,V_cell10 ,V_cell11 ,V_cell12 \
        ,SOC_goup\
    FROM bess_group_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND (bc.id_group=168311326260102 )"\
        + timegap+ \
        "ORDER BY bc.time_stamp" 
'''        
query_DMU="SELECT \
        index_id \
        ,time_stamp \
        ,SOC_goup \
        ,id_dcdc \
        ,Ah_cluster \
        ,Vdc_cluster \
    FROM bess_parallel_cluster_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND (bc.id_cluster='DT-DT-0831-26-BC02' )"\
        + timegap
query1="SELECT \
        id_group \
        ,I_aver \
        ,time_stamp \
        ,V_cell01 \
    FROM bess_group_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND (bc.id_group=168311326260102 OR bc.id_group=168311322220101) \
        AND bc.time_stamp >='2017-07-30 18:00:00' \
        AND bc.time_stamp <='2017-07-30 19:00:00' \
         " 
count_sql = "SELECT count(*) FROM bess_group_data_07 bc \
        WHERE bc.id_station = '2c' \
        AND bc.time_stamp >='2017-07-30 18:00:00' \
        AND bc.time_stamp <='2017-07-30 19:00:00' \
         "
try:
    
    cursor.execute(count_sql)
    count=0
    for row1 in cursor:
        #do_thing()
        count=row1[0]
        print("count=",count)
       
    '''组织Pandas数据表格'''
    '''数据库取数据''' 
    dfDMU = pd.read_sql(query_DMU,connection,index_col="time_stamp")    
    df = pd.read_sql(queryBmu,connection,index_col="time_stamp")
    print(df)
    #df2 = pd.read_sql(queryBmu02,connection,index_col="time_stamp")
    
    '''直接文件取数据
    path_a='/Users/rob/Documents/国内储能/同达电厂/backdata9-26/bess_parallel_cluster_data_07-(20170921-20170922).txt'
    df_headlist=['index_id',  'SOC_goup', 'SOH_group', 'id_cluster', 'id_dcdc', 'id_bms', 'id_station', 'ord', 'type', 'Vdc_cluster', 'online', 'Ah_cluster', 'warnSt', 'protSt', 'usedEnergy', 'leftEnergy', 'charge_ah', 'discharge_ah', 'store_time']
    print('read DMU.')
    data =pd.read_csv(path_a, sep=',', header=None,  na_filter=False,index_col=1)
    data.columns = df_headlist
    data.index.name = 'time_stamp'
    #dfDMU=data[(data['id_cluster']=='DT-DT-0831-26-BC02') & (data.index<'2017-08-31 00:00:00')]
    dfDMU=data[(data['id_cluster']=='DT-DT-0831-26-BC02') & (data.index<'2017-09-22 00:00:00')]
    #dfDMU.reset_index(drop=True)
    #dfDMU.sort_values(by=['time_stamp'])#按列进行排序
    #dfDMU.set_index('time_stamp')
    dfDMU.sort_index()
    #print(dfDMU)
    print('read BMU.')
    path_b='/Users/rob/Documents/国内储能/同达电厂/backdata9-26/bess_group_data_12-(20170921-20170922).txt'
    df_headlist2 = ['index_id', 'id_group', 'id_cluster', 'id_dcdc', 'id_bms', \
                    'id_station', 'ord', 'channel', 'address', 'type', \
                    'Vdc_group', 'AH_group', 'I_group', 'T_group', 'I_aver', \
                    'online', 'SOC_goup', 'SOH_group',  'store_time', \
                    'V_cell01', 'V_cell02', 'V_cell03', 'V_cell04', 'V_cell05', 'V_cell06', 'V_cell07', 'V_cell08', 'V_cell09', 'V_cell10', 'V_cell11', 'V_cell12', 'V_cell13', 'V_cell14', 'V_cell15', 'warn', 'Tmin_cell', 'Tmax_cell', 'warn_data', 'Vmax', 'Vmin', 'T_01', 'T_02', 'T_03', 'T_04', 'T_05', 'T_06', 'T_07', 'T_08', 'T_09', 'T_10', 'T_11', 'T_12', 'T_13', 'T_14', 'T_15', 'T_16']
    data2 =pd.read_csv(path_b, sep=',', header=None,  na_filter=False,index_col=18)
    data2.columns = df_headlist2
    print('.')
    data2.index.name = 'time_stamp'
    #df = data2[(data2['id_station'] == '2c') & (data2['id_cluster']=='DT-DT-0831-26-BC02' ) & (data2.index<'2017-08-31 00:00:00')]
    df = data2[(data2['id_station'] == '2c') & (data2['id_cluster']=='DT-DT-0831-26-BC02' ) & (data2.index<'2017-09-22 00:00:00')]
    print('...')
    #df2 = data2[(data2['id_station'] == '2c') & (data2['id_group']==1683113262602017 ) & (data2.index<'2017-08-31 00:00:00')]
    #id_groups = df.pop('id_group')
    #id_groups.columns=['id_group']
    
    #print(type(id_groups))
    #igd = df.drop_duplicates()
    #print(igd)
    '''
    ig = df.drop_duplicates(['id_group'])
    #print (ig)
    id_groups = list(ig.pop('id_group'))
    print(id_groups)
    groupNum = len(id_groups)
    print('groupNum=',groupNum)
    
    df0 = df[(df['id_station'] == '2c') & (df['id_group']==id_groups[1] ) & (df.index<'2017-07-30 19:00:00')]
    for iGroup in range(2,groupNum):
        df2 = df[(df['id_station'] == '2c') & (df['id_group']==id_groups[iGroup] ) & (df.index<'2017-07-30 19:00:00')]

        for k in range(1, 13):
            newhead = 'V_cell'+'%d' %((k)+(iGroup-1)*12)
            oldhead = ('V_cell0'+'%d'%k) if k<10 else('V_cell'+'%d' %k)
            out1 = df2.pop(oldhead)
            #print(out1)
            df0[newhead] = out1
    #df.reset_index()
    df0.sort_index()#按列进行排序
    df0.to_csv('data_bmu1.csv')
    print('data saved to data_bmu1.csv')
    #print(df)
    
    '''利用Pandas数据表格进行画图工作'''
    #print(df0['V_cell16'])
    
    traces = []
    '''定义trace曲线数据,在第一个y轴上画一个族的电芯电压'''
    for i in range(1, (groupNum-1)*12+1):
        hd=('V_cell0'+'%d'%i) if i<10 else('V_cell'+'%d' %i)
        nm ="第...102"+"P"+"第"+hd[6:]+'颗'+'电压(V)'
        i1 = int( i/24)
        i2 = i%24
        nm ="第"+hd[6:]+'颗'+'电压(V)'\
            '%dp'%i1+'%ds'%i2
        #print(nm)
        traces.append(go.Scatter(
            #mode='lines',line=dict(color='rgba(0,255,0,0)', width=0.5),
            mode='lines',line=dict(color=colorsX[0], width=0.1),
            connectgaps=False,      #对于缺数据断点是否连接曲线  #x=df['time_stamp'],     对x轴利用Pandas赋值
            x=df0.index,
            y=df0[hd] ,              #对y轴利用Pandas赋值
            yaxis='电芯电压(V)',     #标注轴名称
            name=nm,                #标注鼠标移动时的显示点信息
            ))
    '''在第二个y轴上画SOC'''
    trace2=(go.Scatter(
        mode='lines',line=dict(color=colorsX[1], width=0.5),
        connectgaps=False,
        #x=df0DMU['time_stamp'],
        x=df0.index,
        y=dfDMU['SOC_goup'],
        #曲线标签名称,dfDMU['id_cluster']+
        name='簇SOC',
        #hoverinfo='name',
        #决定y轴取那个轴，y2——>yaxis2,
        yaxis='y2'
            )       
        )    
    '''在第三个y轴上画电压''' 
    trace3=(go.Scatter(
        mode='lines',line=dict(color=colorsX[2], width=0.5),
        connectgaps=False,
        #x=dfDMU['time_stamp'],
        x=df0.index,
        y=dfDMU['Vdc_cluster'],
        #曲线标签名称,dfDMU['id_cluster']+
        name='簇电压V',
        #hoverinfo='name',
        #决定y轴取那个轴，y2——>yaxis2,
        yaxis='y3'
            )       
        )    
    '''在第四个y轴上画电流''' 
    trace4=(go.Scatter(
        mode='lines',line=dict(color=colorsX[3], width=0.5),
        connectgaps=False,
        #x=dfDMU['time_stamp'],
        x=df0.index,
        y=dfDMU['Ah_cluster'],
        #曲线标签名称,dfDMU['id_cluster']+
        name='簇电流A',
        #hoverinfo='name',
        #决定y轴取那个轴，y2——>yaxis2,
        yaxis='y4'
            )       
        )
    #将所有traces曲线打包
    traces.append(trace2)
    traces.append(trace3)
    traces.append(trace4)
    #start=datetime('2017-8-7 00:00')
    #print(start)
    #stop=datetime('2017-8-7 23:59')
    '''定义layout'''
    layout = go.Layout(
        width=1280,
        xaxis=dict(
            domain=[0.1, 0.9],
            showline=True,
            showgrid=True,
            showticklabels=True,
            #linecolor=colorsX[0],
            linewidth=2,
            autotick=True,
            ticks='outside',
            #tickcolor=colorsX[0],
            tickwidth=2,
            ticklen=5,
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        #第一个y轴
        yaxis=dict(
            title='电芯电压(V)',
            linecolor=colorsX[0],
            showgrid=True,
            zeroline=False,     #是否显示基线,即沿着(0,0)画出x轴和y轴
            showline=True,
            showticklabels=True,
            titlefont=dict(color=colorsX[0]),
            tickfont=dict(color=colorsX[0]),
        ),
        #第二个y轴
        yaxis2=dict(
            title='簇SOC',
            linecolor=colorsX[1],
            showgrid=True,
            zeroline=False,     #是否显示基线,即沿着(0,0)画出x轴和y轴
            showline=True,
            showticklabels=True,
            titlefont=dict(color=colorsX[1]),
            tickfont=dict(color=colorsX[1]),
            range=[0, 100],
            anchor='x',
            overlaying='y',
            side='right',
            #position=0.85
        ),               
        #第三个y轴
        yaxis3=dict(
            title='簇电压V_aver',
            linecolor=colorsX[2],
            showgrid=True,
            zeroline=False,     #是否显示基线,即沿着(0,0)画出x轴和y轴
            showline=True,
            showticklabels=True,
            titlefont=dict(color=colorsX[2]),
            tickfont=dict(color=colorsX[2]),
            anchor='free',
            overlaying='y',
            side='left',
            position=0.05
        ),   
        #第四个y轴
        yaxis4=dict(
            title='簇电流I_aver',
            linecolor=colorsX[3],
            showgrid=True,
            zeroline=False,  #是否显示基线,即沿着(0,0)画出x轴和y轴
            showline=True,
            showticklabels=True,
            titlefont=dict(color=colorsX[3]),
            tickfont=dict(color=colorsX[3]),
            anchor='free',
            overlaying='y',
            side='right',
            position=0.95
        ),                
        #autosize=True,
        margin=dict(
            autoexpand=False,
            l=20,
            r=20,
            t=100,
        ),
        showlegend=False,
    )
    
    annotations = []
    '''增加annotations注释的文本格式'''
    # Title
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='left', yanchor='bottom',
                              text='多轴电芯分析图',
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                              xanchor='center', yanchor='top',
                              text='数据来源: 同达电厂储能AGC & ' +
                                   '调频数据',
                              font=dict(family='Arial',
                                        size=12,
                                        color='rgb(150,150,150)'),
                              showarrow=False))
    layout['annotations'] = annotations
    fig = go.Figure(data=traces, layout=layout)
    plot_url = plotly.offline.plot(fig)
except pymysql.Error as err:
    print("query table 'mytable' failed.")
    print("Error: {}".format(err.msg))
    sys.exit()
    
#cursor.close()
#connection.close()
