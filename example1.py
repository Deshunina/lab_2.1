from spyre import server
import pandas as pd 
import urllib2
from matplotlib import pyplot as plt


class StockExample(server.App):
    title = "VCI, TCI, VHI indexes"

    inputs = [{     "input_type":'dropdown',
                    "label": 'VCI, TCI, VHI Indexes', 
                    "options" : [ {"label": "VCI", "value":'VCI'},
                                  {"label": "TCI" , "value":'TCI'},
                                  {"label": "VHI", "value":'VHI'},
                                  ],
                    "variable_name": 'index', 
                    "action_id": "update_data" },

              {     "input_type":'dropdown',
                    "label": 'Regions of data', 
                    "options" : [ {"label": "Vinnytsia", "value":'01'},
                                  {"label": "Volyn" , "value":'02'},
                                  {"label": "Dniprovska", "value":'03'},
                                  {"label": "Donetska", "value":'04'},
                                  {"label": "Zhitomirska", "value":'05'},
                                  {"label": "Zakarpatska", "value":'06'},
                                  {"label": "Zap", "value":'07'},
                                  {"label": "Ivan", "value":'08'},
                                  {"label": "Kiev", "value":'09'},
                                  {"label": "Kirov" , "value":'10'},
                                  {"label": "Luh", "value":'11'},
                                  {"label": "Lviv" , "value":'12'},
                                  {"label": "Mikola" , "value":'13'},
                                  {"label": "Odessa" , "value":'14'},
                                  {"label": "Poltava", "value":'15'},
                                  {"label": "Rovno", "value":'16'},
                                  {"label": "Sum" , "value":'17'},
                                  {"label": "Tern" , "value":'18'},
                                  {"label": "Hark" , "value":'19'},
                                  {"label": "Her", "value":'20'},
                                  {"label": "Hmel", "value":'21'},
                                  {"label": "Cherk" , "value":'22'},
                                  {"label": "Chern" , "value":'23'},
                                  {"label": "Chernih" , "value":'24'},
                                  {"label": "Crimea" , "value":'25'},
                                  ],
                    "variable_name": 'region',
                    "action_id": "update_data" }, 

                {   "input_type":'text',
                    "label":'Year',
                    "value": 1985 ,
                    "variable_name": 'one_year',
                    "action_id":"update_data"},

                {   "input_type":'text',
                    "label":'Week from',
                    "value": 0 ,
                    "variable_name": 'week_from',
                    "action_id":"update_data"},
                
                {   "input_type":'text',
                    "label":'Week to',
                    "value":52 ,
                    "variable_name": 'week_to',
                    "action_id":"update_data"}]
    
    controls = [{   "control_type" : "hidden",  
                    "label" : "get historical stock prices",
                    "control_id" : "update_data"}]
    
    tabs = ["Plot", "Table"]
    
    outputs = [{    "output_type" : "plot",
                    "output_id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot", 
                    "on_page_load" : True },
               
               {   "output_type" : "table",
                    "output_id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]
    
    

    def getData(self,params):
        URL = "http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R{}.txt" 
        region = params['region']
        url = URL.format(region)           
        vhi_url = urllib2.urlopen(url)
        out = open('vhi_id.csv','wb') 
        out.write(vhi_url.read())
        out.close()
        df = pd.read_csv( 'vhi_id.csv', names=['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'VHI<15', 'VHI<35'], header=1)
        return df.loc[df['VHI']>0]
        
    def getPlot(self,params):
        df = self.getData(params)
        x = df[(df['Year']==int(params['one_year']))]
        x = x[(x['Week']>=int(params['week_from']))]
        x = x[(x['Week']<=int(params['week_to']))]
        plt_y = x[params['index']]
        plt_x = x['Week']
        plt.xlabel('Year ' + params['one_year'])
        plt.ylabel(params['index'])
        plt.plot(plt_x, plt_y, 'm')
        plt.axis([1, 52, 0, 100])
        return plt.gcf()
    
app = StockExample()
app.launch(port=9093)