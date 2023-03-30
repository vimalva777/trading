from django.shortcuts import render,redirect
from urllib.request import urlopen 
import requests
import json
import math
import pandas as pd
import xlwings as xw
import time
from datetime import datetime,timedelta
from dateutil import parser
import numpy as np

from trading_app.models import Order_db
from trading_app.models import Intruction_db
from trading_app.models import mood_thought_status_db

from smartapi import SmartConnect #for from smartapi.smartConnect import SmartConnect
import smartapi.smartExceptions 
import pyotp

from nsepython import *   

from datetime import datetime
now = datetime.now()

print("now =", now)
dt_string = now.strftime("%m/%d/%Y, %H:%M:%S")


print("date and time =", dt_string)
symbol_token= ""
symbol=""
exch_seg=""
qty=""
Main_orderId=""
# Expiry_date="16-Mar-2023"
# formated_dt = "16MAR23"
Expiry_date="29-Mar-2023"
formated_dt = "29MAR23"

option_df=''

token="ANHFDQW2SOZPMXCWKCLRLU7MQQ"
totp=pyotp.TOTP(token).now()
print(totp)
trading_api="VkV7kXqE"
                #create object of call
obj=SmartConnect(api_key=trading_api)
                                
Client_id="v89401"
mipn="0000"
Password=mipn
data = obj.generateSession(Client_id,Password,totp)
                #login api 252
                #place orde
try:
                        refreshToken= data['data']['refreshToken']
except Exception as error:
                        print("Login error:",error)
if refreshToken:
        feedToken=obj.getfeedToken()
        userProfile= obj.getProfile(refreshToken)
        refreshToken= data['data']['refreshToken']
                #fetch the feedtoken
feedToken=obj.getfeedToken()
                #fetch User Profile
userProfile= obj.getProfile(refreshToken)  


mood_data=mood_thought_status_db.objects.all()
for i in mood_data:
        mood=(i.Mood)
        mrkt_con=(i.Market_condition)
        prep=(i.Preparation)
        thought=(i.Thought)

def trading(request):
        return render(request,"trading.html") 
def instructions(request):
        return render(request,"instruction.html") 
def instru_table(request):
    obj=Intruction_db.objects.all()
    return redirect (option_data_refresh,{'obj':obj})
def instru_data_post(request):
    if request.method=="POST":
        D_target=request.POST.get('Day_target')
        W_target=request.POST.get('weekly_target')
        date_tm=dt_string 
        Trd_plans=request.POST.get('trd_planes')
        data=Intruction_db(trading_plans=Trd_plans,date_time=date_tm,Daily_target=D_target,weekly_target=W_target)
        data.save()
        return redirect(option_data_refresh)
    
def order_data(request):
    obj=Order_db.objects.all()
    return render (request,"order_data.html",{'obj':obj})
def mood_thought_data_post(request):
        if request.method=="POST":
                
                dt_string 
                mood=request.POST.get('Mood')
                Mrkt_con=request.POST.get('Market')
                date_tm=dt_string 
                prep=request.POST.get('prep')
                thought=request.POST.get('prep')
                data=mood_thought_status_db(Mood=mood,date_time=date_tm,Market_condition=Mrkt_con,Preparation=prep,Thought=thought)
                data.save()
                return redirect(option_data_refresh)
def symbol_token_data(request):  
# store the URL in url as  
# parameter for urlopen 
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
# store the response of URL 
        response = urlopen(url) 
# from url in data 
        if response.getcode() == 200:
        #     source = response.read()
            data_json = json.loads(response.read())
        else:
                print('An error occurred while attempting to retrieve data from the API.')   
# print the json response 
        try :
                with open("sample.json", "w") as f:
                        json.dump(data_json, f)
        except:
                print("json is not saved")
        rslt="Symbol data saved to location"

        return redirect (option_data_refresh)
         
def expiry_date_dropdwn(request):
        global Expiry_date 
       
        #ref site== https://stackoverflow.com/questions/56315183/how-to-get-dropdown-list-items-from-pandas-dataframe-using-python-flask

        url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'

        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                        'accept-encoding': 'gzip, deflate, br'} 

        session = requests.Session()
        data=session.get(url_nf,headers=headers).json() ['records']['data']

        option_data=[]

        for i in data:
                for j,k in i.items():
                        if j=="CE" or j=="PE":
                                info=k
                                info["instrumentType"]=j
                                option_data.append(info)
                                df=pd.DataFrame(option_data)
        Expiry_dates=pd.to_datetime(df["expiryDate"])

        Expiry_dates=(Expiry_dates.drop_duplicates())
                
        #print(Expiry_dates.dtype)

        # Sort DataFrame by date column in descending order

        d=Expiry_dates.sort_values(ascending=True)
        print(d)
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("Expiry_dt")
        # st.range("A1").value=Expiry_dates
        # d = {'Services': ["red", "green", "blue"]}
        #df = pd.DataFrame(data=d)
        # Expiry_date=request.POST.get('expiry_date')
        # print("expiry date :",Expiry_date)
        return render (request,'trading.html', {"data" :d})     
def round_nearest(x,num=50):
        global n
        n=(int(math.ceil(float(x)/num)*num))
        return print(n)
def nifty_option_data(request):
        global Expiry_date
        global trading_symbol_CE
        global trading_symbol_PE
        global option_df

        # pandas to json Reffrence site == https://hackershrine.com/uncategorized/render-pandas-dataframe-on-your-django-webapp/ 
        # reference site=https://www.youtube.com/watch?v=CZUy_MCrA-E
        # link to get spot price== https://nsetools.readthedocs.io/en/latest/usage.html#getting-a-stock-quote
        # Urls for fetching Data
        url_oc      = "https://www.nseindia.com/option-chain"
        url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

        url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        url_indices = "https://www.nseindia.com/api/allIndices"
        nifty_spot_url="https://www.nseindia.com/api/marketStatus"

        # Headers
       
        
        headers={"accept-encoding": "gzip, deflate, br",
                "accept-language": "en-US,en;q=0.9",
                "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36"
                }

        session = requests.Session()
        data=session.get(url_nf,headers=headers).json() ['records']['data']
        data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
        data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

        nifty_spot_price=data_nifty.iat[0,4]
        print("Nifty spot price LNo 1o3:",nifty_spot_price)
        #print(data_nifty_spot)
        round_nearest(nifty_spot_price)
        print(n)
        CE_1=(n)-50
        CE_2=n-100
        CE_3=n-150
        CE_4=n-200

        PE_1=n
        PE_2=n+50
        PE_3=n+100
        PE_4=n+150

        print("CE:",CE_1)
        print("CE:",CE_2)
        print("CE:",CE_3)
        print("CE:",CE_4)
        print("$"*35)
        print("PE:",PE_1)
        print("PE:",PE_2)
        print("PE:",PE_3)
        print("PE:",PE_4)
        option_data=[]

        for i in data:
                for j,k in i.items():
                        if j=="CE" or j=="PE":
                                info=k
                                info["instrumentType"]=j
                                option_data.append(info)

        df=pd.DataFrame(option_data) 
        # insert column using insert(position,column_name,
        # first_column) function
        df['expiryDate'] = pd.to_datetime(df['expiryDate'], errors='coerce')

# df['expiryDate'] = pd.to_datetime(df.expiryDate, format='%d-%m-%Y')

        print("DF after date formated mode")
        print(df)
        print(df.dtypes)

        print("df with Exiry date")
        print("Expiry date :",Expiry_date)
        Expiry_date_df=df.loc[df['expiryDate'] == Expiry_date]

        CE_data_expiry_dt=Expiry_date_df.loc[df['instrumentType'] == "CE"]
        print("Choosen Expiry Date and CE data ")
        print(CE_data_expiry_dt)
        OI_sum_CE_expiry = sum(CE_data_expiry_dt['openInterest'])
        print("CE OI Sum Of Choosen Expiry date: ",OI_sum_CE_expiry)
        Vol_sum_CE_expiry = sum(CE_data_expiry_dt['totalTradedVolume'])
        print("Total volume of CE ption Chain :",Vol_sum_CE_expiry)

        PE_data_expiry_dt=Expiry_date_df.loc[df['instrumentType'] == "PE"]
        # 
        Vol_sum_PE_expiry = sum(PE_data_expiry_dt['totalTradedVolume'])
        print("Total volume of CE ption Chain :",Vol_sum_PE_expiry)

        OI_sum_PE_expiry = sum(PE_data_expiry_dt['openInterest'])
        print("CE OI Sum Of Choosen Expiry date: ",OI_sum_PE_expiry)
       

        OI_VOL_data = {"Data":["OI","VOL"],
                       'CE': [OI_sum_CE_expiry,Vol_sum_CE_expiry],
        'PE': [OI_sum_PE_expiry,Vol_sum_PE_expiry],
        "Diff":[OI_sum_CE_expiry -OI_sum_PE_expiry,Vol_sum_CE_expiry -Vol_sum_PE_expiry] }
        OI_VOL_DF=pd.DataFrame(OI_VOL_data)

        print("OI VOL datframe with choosen expiry date")
        print(OI_VOL_DF)

        # pandas to json
        OI_VOL_DF_json = OI_VOL_DF.reset_index().to_json(orient ='records')
        OI_VOL_EXP=[]
        OI_VOL_EXP = json.loads(OI_VOL_DF_json)

        CE_data = df.loc[df.instrumentType=="CE"]

        print("NIfty option CE data ")
        print(CE_data)

        CE_data_totals=CE_data.sum(axis=0)
        print("CE totals")
        print(CE_data_totals)

        CE_OI_totals = df.loc[df.instrumentType=="openInterest"]

        print("CE TOtal OI")
        print (CE_OI_totals)
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("nifty")
        # st.range("A1").value=df
        # now = datetime.now()
        # df2=df.loc[df['instrumentType'] == 'PE', 'token'].item()    
        trading_index="NIFTY" 
# trading symbol NIFTY19JAN2318150CE
        trading_symbol_CE = str(trading_index+formated_dt + str(CE_1)+"CE")
        trading_symbol_PE = str(trading_index+formated_dt + str(PE_1)+"PE")

        print("trading symbol",trading_symbol_CE)
        
        df2 = df.loc[df.instrumentType=="CE"]
        print("printing CE Data")
        print(df2)
        df3=df2.loc[df2.strikePrice==CE_1]
        print(df2)

        df4=df3.loc[df3.expiryDate== Expiry_date]
        print(df4)

        df5 = df.loc[df.instrumentType=="PE"  ]
        df6=df5.loc[df5.strikePrice==PE_1]
        df7=df6.loc[df6.expiryDate== Expiry_date]
        print(df7)
        frames = [df4, df7]
        option_df = pd.concat(frames)
        #calculating deference of CE and PE Open Interests
        try :
                CE_Oi_data=(df4.iloc[0]['openInterest'])
        except:
                print("pls enter valid Expiry date")
                exit("invaid expiry date fix at line No:36 & 37")
        print("CE open interest :",CE_Oi_data)
        PE_Oi_data=(df7.iloc[0]['openInterest'])
        print("CE open interest :",PE_Oi_data)

        OI_difference_CE_PE=CE_Oi_data-PE_Oi_data
        
        oi_d=OI_difference_CE_PE
        print("OI difference between CE and PE :",OI_difference_CE_PE)
        #printing NIFTY nearest to spot price ooption CE symbols data
        print(option_df)
        #print("spot price :",df.iat[1,19])
        # current_time = now.strftime("%H:%M:%S")
        # print(current_time)

        print(indices)
        x=(nse_fiidii())
        # fii_dii_dta=(nse_fiidii("list"))
        df_fii_dii=pd.DataFrame(x)
        print("data frame of DII and FII")

        print(df_fii_dii)
        dii_diff=df_fii_dii.loc[df_fii_dii['category'] == "DII **" , 'netValue'].item()
        print("DII NETdifferemce :",float(dii_diff))
        fii_diff=df_fii_dii.loc[df_fii_dii['category'] == "FII/FPI *" , 'netValue'].item()
        print("Fii_NET difference :",float(fii_diff))

        totl_DII_FII_market_chang=float(dii_diff)+float(fii_diff)
        print("total Fii & dii change in market :",totl_DII_FII_market_chang)
        dii_fii_m=round(totl_DII_FII_market_chang,2)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        dii_fii_json = df_fii_dii.reset_index().to_json(orient ='records')
        dii_fii=[]
        dii_fii = json.loads(dii_fii_json)
        # print(dii_fii)
        # print(nse_fiidii())

       # fii_dii_dta=(nse_fiidii("list"))
      #  print(fii_dii_dta)
        now = datetime.now()
 
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        json_records = option_df.reset_index().to_json(orient ='records')
        arr = []
        arr = json.loads(json_records)
        expiry_date = Expiry_date

        trgt_dta=Intruction_db.objects.all()
        print("target data from db")
        print(trgt_dta)
        
        Order_data=Order_db.objects.all()

        # Convert Django's Queryset into a Pandas DataFrame
        order_df = pd.DataFrame.from_records(Order_data.values())
        print(order_df)
        order_df['Date'] = pd.to_datetime(order_df['Date_time']).dt.date

        print("Order DF")
        print(order_df)
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("exicuted_orders_data")
        # st.range("A1").value=order_df
        td_date = now.strftime("%d/%m/%Y")
        print("Today:", td_date)
        td_date = parser.parse(td_date)
        print(td_date)
        print(type(td_date))
        print("parsed todays date :",td_date)
        td_date = td_date.date()
        print("parsed date:",td_date)
        print(type(td_date))

        print("Calculated Date:",td_date)
        print("data type:",(type(td_date)))
        print("Expiry Date:",Expiry_date)
        datetime64_obj = np.datetime64(td_date)
        print("date type:",type(datetime64_obj))
        td_date = pd.to_datetime(datetime64_obj)

        # td_date="2023-03-17"
        order_df['Date'] = pd.to_datetime(order_df['Date'], errors='coerce')
        # selecting rows based on condition 
        tdys_orderd_data = order_df[order_df['Date'] == td_date]

        # tdys_orderd_data = order_df[(order_df['Date'] == td_date)]
        print("filtered order data from selected date")
        print(tdys_orderd_data)
        tdys_orderd_data['profit_Loss_amnt'] = tdys_orderd_data['profit_Loss_amnt'].astype(float)
        # print (tdys_orderd_data.dtypes)
        tdays_totl_PL = sum(tdys_orderd_data['profit_Loss_amnt'])
        tdays_totl_PL=round(tdays_totl_PL,2)
        print("sum of Todys P/L :",tdays_totl_PL)
        # Function to convert string to datetime

        date_time = parser.parse(Expiry_date)
        print(date_time)
        print(type(date_time))

        cal_date= date_time -timedelta(days = 6)
        print("caclculated date:",cal_date)

        # extracting Date from date time
        cal_date = cal_date.date()
        print("Calculated Date:",cal_date)
        print("data type:",(type(cal_date)))
        print("Expiry Date:",Expiry_date)
        datetime64_obj = np.datetime64(cal_date)
        print("date type:",type(datetime64_obj))
        dt_ns = pd.to_datetime(datetime64_obj)
        
        weekly_order_data = order_df[(order_df['Date'] > dt_ns) & (order_df['Date'] < Expiry_date)]
        print("Order data by week ")
        print(weekly_order_data)
        weekly_order_data['profit_Loss_amnt'] = weekly_order_data['profit_Loss_amnt'].astype(float)
        # print (weekly_order_data.dtypes)
       
        week_totl_PL = sum(weekly_order_data['profit_Loss_amnt'])
        week_totl_PL=round(week_totl_PL,2)
        print("sum of week P/L :",week_totl_PL)
        
        for i in trgt_dta:
                da_trgt=i.Daily_target
                wee_trgt=i.weekly_target
                d_trgt=float(i.Daily_target)-tdays_totl_PL
                week_trgt=float(i.weekly_target)-week_totl_PL
                # print("weekly_target:",i.weekly_target)

        print("weekly target amount :",week_trgt)
        print("Daily pending target amount :",d_trgt)
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("Todays_order_data")
        # st.range("A1").value=tdys_orderd_data

        contextt = {"expiry_OI_VOL":OI_VOL_EXP,"td_PL":tdays_totl_PL,"wk_PL":week_totl_PL,"trgt":trgt_dta,"week_trgt":wee_trgt,"d_trgt":da_trgt,"c_time":current_time, "dii_fii_data":dii_fii,"net_dii_fii":dii_fii_m,"exp_date":expiry_date,'d': arr, 'OI_difference':oi_d,"nifty_spot":nifty_spot_price} 
        return  render(request,'option_data.html',contextt)

def option_data_refresh(request):
        global Expiry_date
        # pandas to json Reffrence site == https://hackershrine.com/uncategorized/render-pandas-dataframe-on-your-django-webapp/ 
        # reference site=https://www.youtube.com/watch?v=CZUy_MCrA-E
        # link to get spot price== https://nsetools.readthedocs.io/en/latest/usage.html#getting-a-stock-quote
        # Urls for fetching Data
        url_oc      = "https://www.nseindia.com/option-chain"
        url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'

        url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
        url_indices = "https://www.nseindia.com/api/allIndices"
        nifty_spot_url="https://www.nseindia.com/api/marketStatus"

        # Headers
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                'accept-encoding': 'gzip, deflate, br'} 

        session = requests.Session()
        
        try:
                data=session.get(url_nf,headers=headers).json() ['records']['data']
                x="True"
        except:
                print("option data record failed")
        while x=="True":
                pass
        else :
                data=session.get(url_nf,headers=headers).json() ['records']['data']
                x="True"
                
        data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
        data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

        nifty_spot_price=data_nifty.iat[0,4]
        print("Nifty spot price LNo 1o3:",nifty_spot_price)
        #print(data_nifty_spot)
        while nifty_spot_price== "nan" :
                data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
                data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

                nifty_spot_price=data_nifty.iat[0,4]
                print("Nifty spot price LNo 1o3:",nifty_spot_price)
        else :
                pass

        round_nearest(nifty_spot_price)
        print(n)
        CE_1=(n)-50
        CE_2=n-100
        CE_3=n-150
        CE_4=n-200

        PE_1=n
        PE_2=n+50
        PE_3=n+100
        PE_4=n+150

        print("CE:",CE_1)
        print("CE:",CE_2)
        print("CE:",CE_3)
        print("CE:",CE_4)
        print("$"*35)
        print("PE:",PE_1)
        print("PE:",PE_2)
        print("PE:",PE_3)
        print("PE:",PE_4)
        option_data=[]

        for i in data:
                for j,k in i.items():
                        if j=="CE" or j=="PE":
                                info=k
                                info["instrumentType"]=j
                                option_data.append(info)

        df=pd.DataFrame(option_data) 
        # insert column using insert(position,column_name,
        # first_column) function
        df['expiryDate'] = pd.to_datetime(df['expiryDate'], errors='coerce')

# df['expiryDate'] = pd.to_datetime(df.expiryDate, format='%d-%m-%Y')

        print("DF after date formated mode")
        print(df)
        print(df.dtypes)

        print("df with Exiry date")
        print("Expiry date :",Expiry_date)
        Expiry_date_df=df.loc[df['expiryDate'] == Expiry_date]

        CE_data_expiry_dt=Expiry_date_df.loc[df['instrumentType'] == "CE"]
        print("Choosen Expiry Date and CE data ")
        print(CE_data_expiry_dt)
        OI_sum_CE_expiry = sum(CE_data_expiry_dt['openInterest'])
        print("CE OI Sum Of Choosen Expiry date: ",OI_sum_CE_expiry)
        Vol_sum_CE_expiry = sum(CE_data_expiry_dt['totalTradedVolume'])
        print("Total volume of CE ption Chain :",Vol_sum_CE_expiry)

        PE_data_expiry_dt=Expiry_date_df.loc[df['instrumentType'] == "PE"]
        # 

        Vol_sum_PE_expiry = sum(PE_data_expiry_dt['totalTradedVolume'])
        print("Total volume of CE ption Chain :",Vol_sum_PE_expiry)

        OI_sum_PE_expiry = sum(PE_data_expiry_dt['openInterest'])
        print("CE OI Sum Of Choosen Expiry date: ",OI_sum_PE_expiry)
       

        OI_VOL_data = {"Data":["OI","VOL"],
                       'CE': [OI_sum_CE_expiry,Vol_sum_CE_expiry],
        'PE': [OI_sum_PE_expiry,Vol_sum_PE_expiry],
        "Diff":[OI_sum_CE_expiry -OI_sum_PE_expiry,Vol_sum_CE_expiry -Vol_sum_PE_expiry] }
        OI_VOL_DF=pd.DataFrame(OI_VOL_data)

        print("OI VOL datframe with choosen expiry date")
        print(OI_VOL_DF)

        # pandas to json
        OI_VOL_DF_json = OI_VOL_DF.reset_index().to_json(orient ='records')
        OI_VOL_EXP=[]
        OI_VOL_EXP = json.loads(OI_VOL_DF_json)

        CE_data = df.loc[df.instrumentType=="CE"]

        print("NIfty option CE data ")
        print(CE_data)

        
        CE_data_totals=CE_data.sum(axis=0)
        print("CE totals")
        print(CE_data_totals)

        CE_OI_totals = df.loc[df.instrumentType=="openInterest"]

        print("CE TOtal OI")
        print (CE_OI_totals)
        
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("nifty")
        # st.range("A1").value=df
        # now = datetime.now()
        # df2=df.loc[df['instrumentType'] == 'PE', 'token'].item()    
        
        trading_index="NIFTY" 
# trading symbol NIFTY19JAN2318150CE
        trading_symbol_CE = str(trading_index+formated_dt + str(CE_1)+"CE")
        trading_symbol_PE = str(trading_index+formated_dt + str(PE_1)+"PE")

        print("trading symbol",trading_symbol_CE)
        
        df2 = df.loc[df.instrumentType=="CE"]
        print("printing CE Data")
        print(df2)
        df3=df2.loc[df2.strikePrice==CE_1]
        print(df2)

        df4=df3.loc[df3.expiryDate== Expiry_date]
        print(df4)

        df5 = df.loc[df.instrumentType=="PE"  ]
        df6=df5.loc[df5.strikePrice==PE_1]
        df7=df6.loc[df6.expiryDate== Expiry_date]
        print(df7)
        frames = [df4, df7]
        option_df = pd.concat(frames)
        #calculating deference of CE and PE Open Interests
        try :
                CE_Oi_data=(df4.iloc[0]['openInterest'])
        except:
                print("pls enter valid Expiry date")
                exit("invaid expiry date fix at line No:36 & 37")
        print("CE open interest :",CE_Oi_data)
        PE_Oi_data=(df7.iloc[0]['openInterest'])
        print("CE open interest :",PE_Oi_data)

        OI_difference_CE_PE=CE_Oi_data-PE_Oi_data
        
        oi_d=OI_difference_CE_PE
        print("OI difference between CE and PE :",OI_difference_CE_PE)
        #printing NIFTY nearest to spot price ooption CE symbols data
        print(option_df)
        #print("spot price :",df.iat[1,19])
        # current_time = now.strftime("%H:%M:%S")
        # print(current_time)

        print(indices)
        x=(nse_fiidii())

        # fii_dii_dta=(nse_fiidii("list"))
        
        df_fii_dii=pd.DataFrame(x)
        print("data frame of DII and FII")

        print(df_fii_dii)
        dii_diff=df_fii_dii.loc[df_fii_dii['category'] == "DII **" , 'netValue'].item()
        print("DII NETdifferemce :",float(dii_diff))
        fii_diff=df_fii_dii.loc[df_fii_dii['category'] == "FII/FPI *" , 'netValue'].item()
        print("Fii_NET difference :",float(fii_diff))

        totl_DII_FII_market_chang=float(dii_diff)+float(fii_diff)
        print("total Fii & dii change in market :",totl_DII_FII_market_chang)
        dii_fii_m=round(totl_DII_FII_market_chang,2)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        dii_fii_json = df_fii_dii.reset_index().to_json(orient ='records')
        dii_fii=[]
        dii_fii = json.loads(dii_fii_json)
        # print(dii_fii)
        # print(nse_fiidii())

       # fii_dii_dta=(nse_
       # fiidii("list"))
      #  print(fii_dii_dta)
        now = datetime.now()
 
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        json_records = option_df.reset_index().to_json(orient ='records')
        arr = []
        arr = json.loads(json_records)
        expiry_date = Expiry_date

        trgt_dta=Intruction_db.objects.all()
        print("target data from db")
        print(trgt_dta)
        
        Order_data=Order_db.objects.all()

        # Convert Django's Queryset into a Pandas DataFrame
        order_df = pd.DataFrame.from_records(Order_data.values())
        print(order_df)
        order_df['Date'] = pd.to_datetime(order_df['Date_time']).dt.date

        print("Order DF")
        print(order_df)
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("exicuted_orders_data")
        # st.range("A1").value=order_df
        td_date = now.strftime("%d/%m/%Y")
        print("Today:", td_date)

        td_date = parser.parse(td_date)
        print("parsed todays date:",td_date)
        print(type(date_time))
        order_df['Date'] = pd.to_datetime(order_df['Date'], errors='coerce')
        # selecting rows based on condition 
        tdys_orderd_data = order_df[order_df['Date'].dt.strftime('%Y-%m-%d') == td_date]
        # tdys_orderd_data = order_df[(order_df['Date'] == td_date)]
        print("filtered order data from selected date")
        print(tdys_orderd_data)
        tdys_orderd_data['profit_Loss_amnt'] = tdys_orderd_data['profit_Loss_amnt'].astype(float)
        print (tdys_orderd_data.dtypes)
        tdays_totl_PL = sum(tdys_orderd_data['profit_Loss_amnt'])
        tdays_totl_PL=round(tdays_totl_PL,2)
        print("sum of Todys P/L :",tdays_totl_PL)
        # Function to convert string to datetime

        date_time = parser.parse(Expiry_date)
        print(date_time)
        print(type(date_time))

        cal_date= date_time -timedelta(days = 6)
        print("caclculated date:",cal_date)
# extracting Date from date time
        cal_date = cal_date.date()
        print("Calculated Date:",cal_date)
        print("data type:",(type(cal_date)))
        print("Expiry Date:",Expiry_date)
        print("Expiry date type:",type(Expiry_date))
        datetime64_obj = np.datetime64(cal_date)
        print("date type:",type(datetime64_obj))
        dt_ns = pd.to_datetime(datetime64_obj)

        weekly_order_data = order_df[(order_df['Date'] > dt_ns) & (order_df['Date'] < Expiry_date)]
        print("Order data by week ")
        print(weekly_order_data)
       
        tdays_totl_PL = sum(weekly_order_data['profit_Loss_amnt'])
        week_totl_PL=round(week_totl_PL,2)
        print("sum of week P/L :",week_totl_PL)
        
        for i in trgt_dta:
                d_trgt=float(i.Daily_target)-tdays_totl_PL
                week_trgt=float(i.weekly_target)-week_totl_PL
                print("weekly_target:",i.weekly_target)
        
        print("weekly target amount :",week_trgt)
        print("Daily pending target amount :",d_trgt)
        #uploading to excel
        # wb=xw.Book("nifty_option_chain_data.xlsx")
        # st=wb.sheets("Todays_order_data")
        # st.range("A1").value=tdys_orderd_data

        contextt = {"expiry_OI_VOL":OI_VOL_EXP,"trgt":trgt_dta,"week_trgt":week_trgt,"d_trgt":d_trgt,"c_time":current_time, "dii_fii_data":dii_fii,"net_dii_fii":dii_fii_m,"exp_date":expiry_date,'d': arr, 'OI_difference':oi_d,"nifty_spot":nifty_spot_price} 
        return  render(request,'option_data.html',contextt)

def square_off(request):

                #Urls for fetching Data
                url_oc      = "https://www.nseindia.com/option-chain"
                url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"
                url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
                url_indices = "https://www.nseindia.com/api/allIndices"
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"

                # Headers
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                        'accept-encoding': 'gzip, deflate, br'} 

                session = requests.Session()
                # data=session.get(url_nf,headers=headers).json() ['records']['data']
                data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
                data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

                nifty_spot_price=data_nifty.iat[0,4]
                print("Niifty spot price :",nifty_spot_price)

                round_nearest(nifty_spot_price)
                print(n)
                PE_1=(n)-50
                print(PE_1)
                PE_2=n-100
                PE_3=n-150
                PE_4=n-200

                CE_1=n
                print(CE_1)
                CE_2=n+50
                CE_3=n+100
                CE_4=n+150


                print("CE:",PE_1)
                print("CE:",PE_2)
                print("CE:",PE_3)
                print("CE:",PE_4)
                print("$"*35)
                print("PE:",CE_1)
                print("PE:",CE_2)
                print("PE:",CE_3)
                print("PE:",CE_4)
                now = datetime.now()

                # df2=df.loc[df['instrumentType'] == 'PE', 'token'].item()
               # Expiry_date="23-Feb-2023"
                dt=Expiry_date
                day=dt[0:2]
                month=dt[3:6]
                month=month.upper()
                year=dt[9:12]
                formated_dt=day+month+year
                print("formated Expiry Date: ",formated_dt)
                trading_index="NIFTY"

                trading_symbol_CE= str(trading_index+formated_dt + str(CE_1)+"CE")

                print("trading symbol",trading_symbol_CE)
                

                print('#'*30)

                symbol=trading_symbol_CE
                token="ANHFDQW2SOZPMXCWKCLRLU7MQQ"
                totp=pyotp.TOTP(token).now()
                apikey="xBhNlutA " 
                username="v89401"
                pwd="0000"

                obj=SmartConnect(api_key=apikey)
                data=obj.generateSession(username,pwd,totp)


                print("Loged in succesfully")
                ###getting symbol token #####
                # token_data = pd.read_json('sample.json')
                                # shift column 'Name' to first position


                df = pd.read_json('D:\\python study\\sample.json')
                                                # shift column 'Name' to first position

                print("sample json")
                print(df)
                wb=xw.Book("nifty_option_chain_data.xlsx")
                st=wb.sheets("sample")
                st.range("A1").value=df
                print(symbol)

                symbol_data=df.loc[df['symbol'] == symbol]
                print(symbol_data)

                symbol_token=df.loc[df['symbol'] == symbol, 'token'].item()
                print("token:",symbol_token)
                qty=df.loc[df['symbol'] == symbol, 'lotsize'].item()
                print("qty:",qty)
                exch_seg=df.loc[df['symbol'] == symbol, 'exch_seg'].item()
                print("exch_seg:",exch_seg)
                try:
                        refreshToken= data['data']['refreshToken']
                except Exception as error:
                        print("Login error:",error)

                if refreshToken:
                        feedToken=obj.getfeedToken()
                        userProfile= obj.getProfile(refreshToken)
                        refreshToken= data['data']['refreshToken']
                         #fetch the feedtoken
                feedToken=obj.getfeedToken()
                obj.position()
                feedToken=obj.getfeedToken()
                userProfile=obj.getProfile(refreshToken)
                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                #print(symbol_data)
                ltp=symbol_data['data']['ltp']
                print("ltp:",ltp)
                exicution_price_1=ltp
                symbol_df=pd.DataFrame(symbol_data)
                print(symbol_df)

                # trade_bk=obj.tradeBook()
                # df1=trade_bk['data']
                # df1=pd.DataFrame[df1]
                # print(df1)
                # print(trade_bk)

                # exicution_price_1=25
                print("Exicuting order")
                try:
                                        orderparams = {
                                                "variety": "NORMAL",
                                                "tradingsymbol": symbol,
                                                "symboltoken": symbol_token,
                                                "transactiontype": "BUY",
                                                "exchange": exch_seg,
                                                "ordertype": "MARKET",
                                                "producttype": "INTRADAY",
                                                "duration": "DAY",
                                                "price": "0",
                                                "squareoff": "0",
                                                "stoploss": "0",
                                                "quantity": qty
                                                }
                                        orderId=obj.placeOrder(orderparams)
                                        print("The order id is: {}".format(orderId))
                                        order_id=format(orderId)
                                        print(order_id)
                                        print_data_1=("The order id is: {}".format(orderId))
                                        return redirect (nifty_option_data)


                except Exception as e:
                                        print("Order placement failed: {}".format(e))

                                        return redirect (nifty_option_data)

def NIFTY_CE_buy(request):
        #Urls for fetching Data
                global Main_orderId
                global symbol
                global exch_seg
                global qty
                url_oc      = "https://www.nseindia.com/option-chain"
                url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"
                url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
                url_indices = "https://www.nseindia.com/api/allIndices"
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"

                # Headers
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                        'accept-encoding': 'gzip, deflate, br'} 

                session = requests.Session()
                # data=session.get(url_nf,headers=headers).json() ['records']['data']
                data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
                data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

                nifty_spot_price=data_nifty.iat[0,4]
                print("Nifty spot price :",nifty_spot_price)

                #Expiry_dates=(Expiry_dates.drop_duplicates())
                # print("expiry date from front end :", Expiry_date)

                print("trading symbol",trading_symbol_CE)
                
                print('#'*30)

                symbol=trading_symbol_CE

                ###getting symbol token #####
                df = pd.read_json('sample.json')
                                # shift column 'Name' to first position
                first_column = df.pop('symbol')
                                
                                # insert column using insert(position,column_name,
                                # first_column) function
                df.insert(0,'symbol', first_column)

                                # print(df)

                result=df.loc[df['symbol'] == symbol]
                        
                print(result)
                # Extract column values by DataFrame.item() method
                symbol_token=df.loc[df['symbol'] == symbol, 'token'].item()
                print("token:",symbol_token)
                qty=df.loc[df['symbol'] == symbol, 'lotsize'].item()
                print("qty:",qty)
                exch_seg=df.loc[df['symbol'] == symbol, 'exch_seg'].item()
                print("exch_seg:",exch_seg)
                      
                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                print(symbol_data)
                ltp=symbol_data['data']['ltp']
                print("ltp:",ltp)
                exicution_price_1=ltp
                symbol_df=pd.DataFrame(symbol_data)
                print(symbol_df)

                print("printing option data")
                print(option_df)
                #getting it to excel
                # wb=xw.Book("nifty_option_chain_data.xlsx")
                # st=wb.sheets("selected_asset_value")
                # st.range("A1").value=option_df
                # print(df)
                ce_oi=option_df.loc[option_df['instrumentType'] == 'CE', 'openInterest'].item()
                print("CE_OI :",ce_oi)
                ce_IV=option_df.loc[option_df['instrumentType'] == 'CE', 'impliedVolatility'].item()
                print("CE_IV :",ce_IV)
                pe_oi=option_df.loc[option_df['instrumentType'] == 'PE', 'openInterest'].item()
                print("PE_OI :",pe_oi)
                pe_IV=option_df.loc[option_df['instrumentType'] == 'PE', 'impliedVolatility'].item()
                print("PE_OI :",pe_IV)

                pe_IV=option_df.loc[option_df['instrumentType'] == 'PE', 'impliedVolatility'].item()
                print("PE_OI :",pe_IV)
                CE_vol=option_df.loc[option_df['instrumentType'] == 'PE', 'impliedVolatility'].item()
                print("PE_OI :",CE_vol)
                PE_vol=option_df.loc[option_df['instrumentType'] == 'PE', 'impliedVolatility'].item()
                print("PE_OI :",PE_vol)

                print("Exicuting order First order ")
                try:
                                        orderparams = {
                                                "variety": "NORMAL",
                                                "tradingsymbol": symbol,
                                                "symboltoken": symbol_token,
                                                "transactiontype": "BUY",
                                                "exchange": exch_seg,
                                                "ordertype": "LIMIT",
                                                "producttype": "INTRADAY",
                                                "duration": "DAY",
                                                "price": exicution_price_1,
                                                "squareoff": "0",
                                                "stoploss": "0",
                                                "quantity": qty
                                                }
                                        Main_orderId=obj.placeOrder(orderparams)
                                        print("The order id is: {}".format(Main_orderId))
                                        Main_orderId=format(Main_orderId)
                                        print("Main Order ID :",Main_orderId)
                                       
                except Exception as e:
                                        print("Order placement failed: {}".format(e))

                order_bk=obj.orderBook()
                df=order_bk["data"]
                df=pd.DataFrame(df)

                #getting it to excel
                # wb=xw.Book("nifty_option_chain_data.xlsx")
                # st=wb.sheets("angel_order_bk")
                # st.range("A1").value=df
                # print(df)
                fst_order_status=df.loc[df['orderid'] == Main_orderId,'status'].item()   
                Exicuted_price=df.loc[df['orderid'] == Main_orderId,'averageprice'].item()
                print("exicuted price :",Exicuted_price)
                print(Main_orderId,",",fst_order_status)
                # data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status
                # ,CE_OI=ce_oi,PE_OI=pe_oi,CE_IV=ce_IV,PE_IV=pe_IV,PE_VOLM=PE_vol,CE_VOLM=CE_vol,Date_time=dt_string,)
                # data.save()
                # Exicuted_price=95.85
                sl_poin=2

                exicution_price_stp_lss=exicution_price_1-sl_poin
                print('exicution_price stop loss :',exicution_price_stp_lss )

                #Exicuting stop loss 
                try:
                                        orderparams = {
                                                "variety": "NORMAL",
                                                "tradingsymbol": symbol,
                                                "symboltoken": symbol_token,
                                                "transactiontype": "SELL",
                                                "exchange": exch_seg,
                                                "ordertype": "LIMIT",
                                                "producttype": "INTRADAY",
                                                "duration": "DAY",
                                                "price": exicution_price_stp_lss,
                                                "squareoff": "0",
                                                "stoploss": "0",
                                                "quantity": qty
                                                }
                                        SL_orderId=obj.placeOrder(orderparams)
                                        print("The order id is: {}".format(SL_orderId))
                                        order_id=format(SL_orderId)
                                        print("order ID :", SL_orderId)
                                        print_data_1=("The order id is: {}".format(SL_orderId))

                except Exception as e:
                                        print("Order placement failed: {}".format(e))

                order_bk=obj.orderBook()
                df=order_bk["data"]
                df=pd.DataFrame(df)

                SL_order_status=df.loc[df['orderid'] == SL_orderId,'status'].item()   
                Exicuted_price_SL=df.loc[df['orderid'] == SL_orderId,'averageprice'].item()
                print("exicuted price :",Exicuted_price_SL)
                print("stop loss order:",order_id,",",SL_order_status)
                

                if (fst_order_status=="rejected") & (SL_order_status =="rejected"):
                        print("starting IF ")
                        while True :
                                print("Exicuting first while")
                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                ltp=symbol_data['data']['ltp']
                        # ltp= 30
                                print("order Exicuted price :",exicution_price_1)
                                print("currrent LTP :",ltp)
                                Stop_loss_point=2
                                prof_loss=ltp-exicution_price_1

                                brokerage=40
                                other_charges=40
                                total_brokerage_fee=brokerage+other_charges
                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                print("Profit or Loss point :",prof_loss)    

                                print("Profit or loss Amount :",prof_loss_Rs)

                                print("starting point of if condition")
          
                                if (prof_loss < 1) &( prof_loss <= -2) :
                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                        ltp=symbol_data['data']['ltp']
                                                        print("LTP :",ltp)
                                                        prof_loss=ltp-exicution_price_1
                                                        print("Prof/Loss:",prof_loss)
                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                        print("prof/Loss :",round(prof_loss_Rs,2))
                                                        prof_loss_Rs=round(prof_loss_Rs,2)

                                                        print("vimal u r not yet profitable")
                                                        print("Stay calm nd focused and energetic")
                                                        if ltp < exicution_price_stp_lss :
                                                                print("Stop loss is been Exicuted  < = 2")
                                                                print("breaking  first while loop of < 1")

                                                                
                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)

                                                                data.save()
                                                                return redirect(nifty_option_data)
                                                                
                                                                # exit("Stoping Exicution by python (ltp is less than SL or<-2)")                      

                                elif (prof_loss >  1) & (prof_loss < 3):
                                        shifting_percenatge=50
                                        print("shifting stop loss")
                                        print("profit point is > 1 and < 3")
                                        # shift stop loss percentaage wise
                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                        print(shifting_point)
                                        SL_modi_price= exicution_price_1 + shifting_point
                                        SL_modi_price = round(SL_modi_price, 2)
                                        print("stop loss Modifiction price :",SL_modi_price)

                                        try:
                                                orderparams =           {
                                                        "variety":"NORMAL",
                                                        "orderid":order_id,
                                                        "ordertype":"LIMIT",
                                                        "producttype":"INTRADAY",
                                                        "duration":"DAY",
                                                        "price":SL_modi_price,
                                                        "quantity":qty,
                                                        "tradingsymbol": symbol,
                                                        "symboltoken":symbol_token,
                                                        "exchange":exch_seg
                                                        }
                                                orderId=obj.placeOrder(orderparams)
                                                print("The order id is: {}".format(orderId))
                                                order_id=format(orderId)
                                                print(order_id)              
                                        except Exception as e:
                                                print("Order placement failed: {}".format(e))
                                        
                                        while True :
                                                print("Exicuting second while")
                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                ltp=symbol_data['data']['ltp']
                                        # ltp= 30
                                                print("order Exicuted price :",exicution_price_1)
                                                print("currrent LTP :",ltp)
                                                Stop_loss_point=2
                                                prof_loss=ltp-exicution_price_1

                                                brokerage=40
                                                other_charges=40
                                                total_brokerage_fee=brokerage+other_charges
                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                print("Profit or Loss point :",prof_loss)    

                                                print("Profit or loss Amount :",prof_loss_Rs)

                                                if (prof_loss < 1) &( prof_loss <= -2) :
                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                        ltp=symbol_data['data']['ltp']
                                                        print("LTP :",ltp)
                                                        prof_loss=ltp-exicution_price_1
                                                        print("Prof/Loss:",prof_loss)
                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                        print("prof/Loss :",round(prof_loss_Rs,2))
                                                        prof_loss_Rs=round(prof_loss_Rs,2)

                                                        print("vimal u r not yet profitable")
                                                        
                                                        print("Stay calm nd focused and energetic")

                                                        if ltp < SL_modi_price :
                                                                print("Stop loss is been Exicuted  < = 2")
                                                                print("breaking  first while loop of < 1")
                                                        
                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                data.save()
                                                                return redirect(nifty_option_data)
                                                                

                                                                exit("Stoping Exicution by python (ltp is less than SL or<-2)")
                                                                
                                                                
                                                elif (prof_loss >  3) & (prof_loss < 6):
                                                                shifting_percenatge=70
                                                                print("shifting stop loss insted second while loop")
                                                                print("profit point is > 3 and < 6")
                                                                # shift stop loss percentaage wise
                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                print("shifting Point :",shifting_point)
                                                                SL_modi_price_1= exicution_price_1 + shifting_point
                                                                SL_modi_price_1 = round(SL_modi_price_1, 2)
                                                                print("stop loss Modification price :",SL_modi_price_1)

                                                                try:
                                                                        orderparams=           {
                                                                                "variety":"NORMAL",
                                                                                "orderid":order_id,
                                                                                "ordertype":"LIMIT",
                                                                                "producttype":"INTRADAY",
                                                                                "duration":"DAY",
                                                                                "price":SL_modi_price_1,
                                                                                "quantity":qty,
                                                                                "tradingsymbol": symbol,
                                                                                "symboltoken":symbol_token,
                                                                                "exchange":exch_seg
                                                                                }
                                                                

                                                                        orderId=obj.placeOrder(orderparams)
                                                                        print("The order id is: {}".format(orderId))
                                                                        order_id=format(orderId)
                                                                        print(order_id)

                                                                except Exception as e:
                                                                        
                                                                        print("Order placement failed: {}".format(e))
                                                                
                                                                while True :
                                                                                print("Exicuting third  while of > 3 ")
                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                ltp=symbol_data['data']['ltp']

                                                                                print("order Modified price :",SL_modi_price_1)
                                                                                print("currrent LTP :",ltp)

                                                                                prof_loss=ltp-exicution_price_1

                                                                                brokerage=40
                                                                                other_charges=40
                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                if ltp <= SL_modi_price_1 :
                                                                                        
                                                                                        print("stop loss is been exicucted")
                                                                                        print("breaking while of < 3 SL")
                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                        data.save()
                                                                                        return redirect(nifty_option_data)
                                                                

                                                                                elif (prof_loss >  6) & (prof_loss < 9):
                                                                                        shifting_percenatge=70
                                                                                        print("shifting stop loss")
                                                                                        print("profit point is > 3 and < 6")
                                                                                        # shift stop loss percentaage wise
                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                        print(shifting_point)
                                                                                        SL_modi_price_2= exicution_price_1 + shifting_point
                                                                                        SL_modi_price = round(SL_modi_price_2, 2)
                                                                                        print("stop loss Modifiaction price :",SL_modi_price_2)

                                                                                        try:
                                                                                                orderparams=           {
                                                                                                        "variety":"NORMAL",
                                                                                                        "orderid":order_id,
                                                                                                        "ordertype":"LIMIT",
                                                                                                        "producttype":"INTRADAY",
                                                                                                        "duration":"DAY",
                                                                                                        "price":SL_modi_price_2,
                                                                                                        "quantity":qty,
                                                                                                        "tradingsymbol": symbol,
                                                                                                        "symboltoken":symbol_token,
                                                                                                        "exchange":exch_seg
                                                                                                        }
                                                                                        

                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                print("The order id is: {}".format(orderId))
                                                                                                order_id=format(orderId)
                                                                                                print(order_id)
                                                                                                

                                                                                        except Exception as e:
                                                                                                print("Order placement failed: {}".format(e))

                                                                                        while True :

                                                                                                print("Exicuting third  while of > 3 ")
                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                print("order Modified price :",SL_modi_price_2)
                                                                                                print("currrent LTP :",ltp)

                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                brokerage=40
                                                                                                other_charges=40
                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                prof_loss_Rs=round(prof_loss_Rs,2)

                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                if ltp <= SL_modi_price_2 :
                                                                                                
                                                                                                        print("stop loss is been exicucted")
                                                                                                        print("breaking while of < 2 SL")
                                                                                                        
                                                                                                        Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                        data.save()
                                                                                                        return redirect(nifty_option_data)
                                                                                                        exit("closing exicution")
                                                                                                        

                                                                                                elif (prof_loss >  6) & (prof_loss < 9):
                                                                                                        shifting_percenatge=80
                                                                                                        print("shifting stop loss")
                                                                                                        print("profit point is > 6 and < 9")
                                                                                                        # shift stop loss percentaage wise
                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                        print(shifting_point)
                                                                                                        SL_modi_price_3= exicution_price_1 + shifting_point
                                                                                                        SL_modi_price_3 = round(SL_modi_price_3, 2)
                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_3)

                                                                                                        try:
                                                                                                                orderparams=           {
                                                                                                                        "variety":"NORMAL",
                                                                                                                        "orderid":order_id,
                                                                                                                        "ordertype":"LIMIT",
                                                                                                                        "producttype":"INTRADAY",
                                                                                                                        "duration":"DAY",
                                                                                                                        "price":SL_modi_price_3,
                                                                                                                        "quantity":qty,
                                                                                                                        "tradingsymbol": symbol,
                                                                                                                        "symboltoken":symbol_token,
                                                                                                                        "exchange":exch_seg
                                                                                                                        }
                                                                                                        

                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                order_id=format(orderId)
                                                                                                                print(order_id)
                                                                                                                
                                                                                                        except Exception as e:
                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                        while True :
                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                print("order Modified price :",SL_modi_price_3)
                                                                                                                print("currrent LTP :",ltp)

                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                brokerage=40
                                                                                                                other_charges=40
                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                if ltp <= SL_modi_price_3 :
                                                                                                                        
                                                                                                                        print("stop loss is been exicucted")
                                                                                                                        print("breaking while of < 6 SL")
                                                                                                                        
                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                        data.save()
                                                                                                                        return redirect(option_data_refresh)
                                                                                                                        exit("closing exicution")
                                                                                                                elif (prof_loss >  9) & (prof_loss < 12):
                                                                                                                        shifting_percenatge=80
                                                                                                                        print("shifting stop loss")
                                                                                                                        print("profit point is > 9 and < 12")
                                                                                                                        # shift stop loss percentaage wise
                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                        print(shifting_point)
                                                                                                                        SL_modi_price_4= exicution_price_1 + shifting_point
                                                                                                                        SL_modi_price_4 = round(SL_modi_price_4, 2)
                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_4)

                                                                                                                        try:
                                                                                                                                orderparams=           {
                                                                                                                                        "variety":"NORMAL",
                                                                                                                                        "orderid":order_id,
                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                        "duration":"DAY",
                                                                                                                                        "price":SL_modi_price_4,
                                                                                                                                        "quantity":qty,
                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                        "exchange":exch_seg
                                                                                                                                        }
                                                                                                                        

                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                order_id=format(orderId)
                                                                                                                                print(order_id)
                                                                                                                        except Exception as e:
                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                        while True :
                                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                print("order Modified price :",SL_modi_price_4)
                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                brokerage=40
                                                                                                                                other_charges=40
                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                if ltp <= SL_modi_price_4 :
                                                                                                                                        
                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                        print("breaking while of < 6 SL")
                                                                                                                                
                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                        data.save()
                                                                                                                                        return redirect(nifty_option_data)

                                                                                                                                elif (prof_loss >  12) & (prof_loss < 15):
                                                                                                                                        shifting_percenatge=80
                                                                                                                                        print("shifting stop loss")
                                                                                                                                        print("profit point is > 12 and <15")
                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                        print(shifting_point)
                                                                                                                                        SL_modi_price_6= exicution_price_1 + shifting_point
                                                                                                                                        SL_modi_price_6 = round(SL_modi_price_6, 2)
                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_6)

                                                                                                                                        try:
                                                                                                                                                orderparams=           {
                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                        "orderid":order_id,
                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                        "duration":"DAY",
                                                                                                                                                        "price":SL_modi_price_6,
                                                                                                                                                        "quantity":qty,
                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                        }
                                                                                                                                        

                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                order_id=format(orderId)
                                                                                                                                                print(order_id)
                                                                                                                                                

                                                                                                                                        except Exception as e:
                                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                                        while True :
                                                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                print("order Modified price :",SL_modi_price_6)
                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                                brokerage=40
                                                                                                                                                other_charges=40
                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                if ltp <= SL_modi_price_6 :
                                                                                                                                                        
                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                        print("breaking while of < 12 SL")
                                                                                                                                                
                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                        data.save()
                                                                                                                                                        exit("closing exicution")


                                                                                                                                                elif (prof_loss >  15) & (prof_loss <20):
                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                        print(shifting_point)
                                                                                                                                                        SL_modi_price_7= exicution_price_1 + shifting_point
                                                                                                                                                        SL_modi_price_7 = round(SL_modi_price_7, 2)
                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_7)

                                                                                                                                                        try:
                                                                                                                                                                orderparams=           {
                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                        "price":SL_modi_price_7,
                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                        }
                                                                                                                                                        

                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                print(order_id)
                                                                                                                                                                

                                                                                                                                                        except Exception as e:
                                                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                                                        while True :
                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                print("order Modified price :",SL_modi_price_7)
                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                                                brokerage=40
                                                                                                                                                                other_charges=40
                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                if ltp <= SL_modi_price_7:
                                                                                                                                                                        
                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                        print("breaking while of < 7 SL")
                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                        data.save()
                                                                                                                                                                        exit("closing exicution")
                                                                                                                                                                elif (prof_loss >  15) & (prof_loss <20):
                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                SL_modi_price_8= exicution_price_1 + shifting_point
                                                                                                                                                                                SL_modi_price_8= round(SL_modi_price_8, 2)
                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_8)

                                                                                                                                                                                try:
                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                "price":SL_modi_price_8,
                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                }
                                                                                                                                                                                

                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                while True :
                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                        print("order Modified price :",SL_modi_price_8)
                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                        if ltp <= SL_modi_price_8:
                                                                                                                                                                                                
                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                print("breaking while of < 7 SL")

                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                data.save()
                                                                                                                                                                                                return redirect(nifty_option_data)
                                                                
                
                                                                                                                                                                                        elif (prof_loss >  20) & (prof_loss <25):
                                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                                SL_modi_price_9= exicution_price_1 + shifting_point
                                                                                                                                                                                                SL_modi_price_9= round(SL_modi_price_9, 2)
                                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_9)

                                                                                                                                                                                                try:
                                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                                "price":SL_modi_price_9,
                                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                                }
                                                                                                                                                                                                

                                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                                while True :
                                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                        print("order Modified price :",SL_modi_price_9)
                                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                        if ltp <= SL_modi_price_9:
                                                                                                                                                                                                                
                                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                                print("breaking while of <  20 ")
                                                                                                                                                                                                                
                                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                data.save()
                                                                                                                                                                                                                return redirect(nifty_option_data)
                                                                
                                                                                                                                                                                                                exit("closing exicution")
                                                                                                                                                                                                        
                                                                                                                                                                                                        elif (prof_loss >  20) & (prof_loss <25):
                                                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                                                SL_modi_price_10= exicution_price_1 + shifting_point
                                                                                                                                                                                                                SL_modi_price_10= round(SL_modi_price_10, 2)
                                                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_10)

                                                                                                                                                                                                                try:
                                                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                                                "price":SL_modi_price_10,
                                                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                                                }
                                                                                                                                                                                                                

                                                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                while True :
                                                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                        print("order Modified price :",SL_modi_price_10)
                                                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                        if ltp <= SL_modi_price_10:
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                                                print("breaking while of <  20 ")
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                data.save()
                                                                                                                                                                                                                                return redirect(nifty_option_data)

                                                                                                                                                                                                                                exit("closing exicution")

                                                                                                                                                                                                                        elif (prof_loss >  25) & (prof_loss <30):
                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                        SL_modi_price_11= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                        SL_modi_price_11= round(SL_modi_price_11, 2)
                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_11)

                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                        "price":SL_modi_price_11,
                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_11)
                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                if ltp <= SL_modi_price_11:
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                        return redirect(nifty_option_data)
                                                                                                                        

                                                                                                                                                                                                                                                elif (prof_loss >  30) & (prof_loss <35):
                                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                                        #shift stop loss percentaage wise

                                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/90 )*prof_loss
                                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                                        SL_modi_price_12= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                                        SL_modi_price_12= round(SL_modi_price_12, 2)
                                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_12)

                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                                        "price":SL_modi_price_12,
                                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_12)
                                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                                if ltp <= SL_modi_price_12: 
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                                        exit("closing exicution")
                                                                                                                                                                                                                                                                elif (prof_loss >  35) & (prof_loss <50):
                                                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                                                        #shift stop loss percentaage wise

                                                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/90 )*prof_loss
                                                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                                                        SL_modi_price_13= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                                                        SL_modi_price_13= round(SL_modi_price_13, 2)
                                                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price)

                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                                                        "price":SL_modi_price_13,
                                                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_13)
                                                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                                                if ltp <= SL_modi_price_13: 
                                                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                                                        return redirect(nifty_option_data)
                                                                
                                                                                                                                                                                                                                                                                        exit("closing exicution")
                                
                                   ###     contents={"Main order ID":Main_orderId,"SL order ID":SL_orderId,"fst_order_status":fst_order_status,"SL_order_status":SL_order_status}
                                        
                                    #    return render(request,'option_exicuted_data.html',contents)

                               # contents={"Main order ID":Main_orderId,"SL order ID":SL_orderId,"fst_order_status":fst_order_status,"SL_order_status":SL_order_status}
                                # return render(request,'option_data.html',contents)




def NIFTY_PE_buy(request):
                #Urls for fetching Data
                url_oc      = "https://www.nseindia.com/option-chain"
                url_bnf     = 'https://www.nseindia.com/api/option-chain-indices?symbol=BANKNIFTY'
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"
                url_nf      = 'https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY'
                url_indices = "https://www.nseindia.com/api/allIndices"
                nifty_spot_url="https://www.nseindia.com/api/marketStatus"

                # Headers
                headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                        'accept-encoding': 'gzip, deflate, br'} 

                session = requests.Session()
                # data=session.get(url_nf,headers=headers).json() ['records']['data']
                data_nifty_spot=session.get(nifty_spot_url,headers=headers).json() 
                data_nifty =pd.DataFrame(data_nifty_spot["marketState"])

                nifty_spot_price=data_nifty.iat[0,4]
                print("Nifty spot price :",nifty_spot_price)

                # print("expiry date from front end :", Expiry_date)


                print("trading symbol :",trading_symbol_PE)
                

                print('#'*30)

                symbol=trading_symbol_PE

                ###getting symbol token #####
                try :

                        df = pd.read_json('sample.json')
                        print(df)
                except:
                        print("kindly Update token data from angel ")
                        exit("Exiting code to update token data")
                print("angel token data")
                                # shift column 'Name' to first position
                first_column = df.pop('symbol')
                print("poping first coumn")
                                
                                # insert column using insert(position,column_name,
                                # first_column) function
                df.insert(0,'symbol', first_column)

                print("Token data from Angel Broking")
                print(df)

                result=df.loc[df['symbol'] == symbol]

                print("symbol is here") 
                print(result)
                        # Extract column values by DataFrame.item() method
                try:
                        symbol_token=df.loc[df['symbol'] == symbol, 'token'].item()
                        print("token:",symbol_token)
                except:
                        exit("PLease update Expiry Date in line 313 nd 314")
                qty=df.loc[df['symbol'] == symbol, 'lotsize'].item()
                print("qty:",qty)
                exch_seg=df.loc[df['symbol'] == symbol, 'exch_seg'].item()
                print("exch_seg:",exch_seg)


                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                print(symbol_data)
                ltp=symbol_data['data']['ltp']
                print("ltp:",ltp)
                exicution_price_1=ltp
                symbol_df=pd.DataFrame(symbol_data)
                print(symbol_df)

                print(option_df)
                #getting it to excel
                # wb=xw.Book("nifty_option_chain_data.xlsx")
                # st=wb.sheets("selected_asset_value")
                # st.range("A1").value=option_df
                # print(df)
                ce_oi=option_df.loc[option_df['instrumentType'] == 'CE', 'openInterest'].item()
                print("CE_OI :",ce_oi)
                ce_IV=option_df.loc[option_df['instrumentType'] == 'CE', 'impliedVolatility'].item()
                print("CE_IV :",ce_IV)
                pe_oi=option_df.loc[option_df['instrumentType'] == 'PE', 'openInterest'].item()
                print("PE_OI :",pe_oi)
                pe_IV=option_df.loc[option_df['instrumentType'] == 'PE', 'impliedVolatility'].item()
                print("PE iv :",pe_IV)

                # print(option_df)
                # wb=xw.Book("nifty_option_chain_data.xlsx")
                # st=wb.sheets("angel_order_bk")
                # st.range("A1").value=option_df
                
                CE_vol=option_df.loc[option_df['instrumentType'] == 'CE', 'totalTradedVolume'].item()
                print("CE vol :",CE_vol)
                PE_vol=option_df.loc[option_df['instrumentType'] == 'PE', 'totalTradedVolume'].item()
                print("PE vol :",PE_vol)

                print("Exicuting order First order ")
                try:
                                        orderparams = {
                                                "variety": "NORMAL",
                                                "tradingsymbol": symbol,
                                                "symboltoken": symbol_token,
                                                "transactiontype": "BUY",
                                                "exchange": exch_seg,
                                                "ordertype": "LIMIT",
                                                "producttype": "INTRADAY",
                                                "duration": "DAY",
                                                "price": exicution_price_1,
                                                "squareoff": "0",
                                                "stoploss": "0",
                                                "quantity": qty
                                                }
                                        Main_orderId=obj.placeOrder(orderparams)
                                        print("The order id is: {}".format(Main_orderId))
                                        Main_orderId=format(Main_orderId)
                                        print("Main Order ID :",Main_orderId)
                                        

                except Exception as e:
                                        print("Order placement failed: {}".format(e))


                # getting order book


                order_bk=obj.orderBook()
                df=order_bk["data"]
                df=pd.DataFrame(df)

                #getting it to excel
                # wb=xw.Book("nifty_option_chain_data.xlsx")
                # st=wb.sheets("angel_order_bk")
                # st.range("A1").value=df
                # print(df)
                fst_order_status=df.loc[df['orderid'] == Main_orderId,'status'].item()   
                Exicuted_price=df.loc[df['orderid'] == Main_orderId,'averageprice'].item()
                print("exicuted price :",Exicuted_price)
                print(Main_orderId,",",fst_order_status)
                # Exicuted_price=95.85
                sl_poin=2

                exicution_price_stp_lss=exicution_price_1-sl_poin
                print('exicution_price stop loss :',exicution_price_stp_lss )

                #Exicuting stop loss 
                try:
                                        orderparams = {
                                                "variety": "NORMAL",
                                                "tradingsymbol": symbol,
                                                "symboltoken": symbol_token,
                                                "transactiontype": "SELL",
                                                "exchange": exch_seg,
                                                "ordertype": "LIMIT",
                                                "producttype": "INTRADAY",
                                                "duration": "DAY",
                                                "price": exicution_price_stp_lss,
                                                "squareoff": "0",
                                                "stoploss": "0",
                                                "quantity": qty
                                                }
                                        SL_orderId=obj.placeOrder(orderparams)
                                        print("The order id is: {}".format(SL_orderId))
                                        order_id=format(SL_orderId)
                                        print("order ID :", SL_orderId)
                                       

                except Exception as e:
                                        print("Order placement failed: {}".format(e))
                
                order_bk=obj.orderBook()
                print(order_bk)
                df=order_bk["data"]
                df=pd.DataFrame(df)

                SL_order_status=df.loc[df['orderid'] == SL_orderId,'status'].item()   
                Exicuted_price_SL=df.loc[df['orderid'] == SL_orderId,'averageprice'].item()
                print("exicuted price :",Exicuted_price_SL)
                print("stop loss order:",order_id,",",SL_order_status)

                if (fst_order_status=="rejected") & (SL_order_status =="rejected"):

                        print("starting IF ")
                        while True :
                                print("Exicuting first while")
                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                ltp=symbol_data['data']['ltp']
                        # ltp= 30
                                print("order Exicuted price :",exicution_price_1)
                                print("currrent LTP :",ltp)
                                Stop_loss_point=2
                                prof_loss=ltp-exicution_price_1

                                brokerage=40
                                other_charges=40
                                total_brokerage_fee=brokerage+other_charges
                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                print("Profit or Loss point :",prof_loss)    

                                print("Profit or loss Amount :",prof_loss_Rs)

                                print("starting point of if condition")
          
                                if (prof_loss < 1) &( prof_loss <= -2) :
                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                        ltp=symbol_data['data']['ltp']
                                                        print("LTP :",ltp)
                                                        prof_loss=ltp-exicution_price_1
                                                        print("Prof/Loss:",prof_loss)
                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                        print("prof/Loss :",round(prof_loss_Rs,2))
                                                        prof_loss_Rs=round(prof_loss_Rs,2)

                                                        print("vimal u r not yet profitable")
                                                        print("Stay calm nd focused and energetic")
                                                        if ltp < exicution_price_stp_lss :
                                                                print("Stop loss is been Exicuted  < = 2")
                                                                print("breaking  first while loop of < 1")

                                                                
                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)

                                                                data.save()
                                                                return redirect(nifty_option_data)
                                                                
                                                                # exit("Stoping Exicution by python (ltp is less than SL or<-2)")                      

                                elif (prof_loss >  1) & (prof_loss < 3):
                                        shifting_percenatge=50
                                        print("shifting stop loss")
                                        print("profit point is > 1 and < 3")
                                        # shift stop loss percentaage wise
                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                        print(shifting_point)
                                        SL_modi_price= exicution_price_1 + shifting_point
                                        SL_modi_price = round(SL_modi_price, 2)
                                        print("stop loss Modifiction price :",SL_modi_price)

                                        try:
                                                orderparams =           {
                                                        "variety":"NORMAL",
                                                        "orderid":order_id,
                                                        "ordertype":"LIMIT",
                                                        "producttype":"INTRADAY",
                                                        "duration":"DAY",
                                                        "price":SL_modi_price,
                                                        "quantity":qty,
                                                        "tradingsymbol": symbol,
                                                        "symboltoken":symbol_token,
                                                        "exchange":exch_seg
                                                        }
                                                orderId=obj.placeOrder(orderparams)
                                                print("The order id is: {}".format(orderId))
                                                order_id=format(orderId)
                                                print(order_id)              
                                        except Exception as e:
                                                print("Order placement failed: {}".format(e))
                                        
                                        while True :
                                                print("Exicuting second while")
                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                ltp=symbol_data['data']['ltp']
                                        # ltp= 30
                                                print("order Exicuted price :",exicution_price_1)
                                                print("currrent LTP :",ltp)
                                                Stop_loss_point=2
                                                prof_loss=ltp-exicution_price_1

                                                brokerage=40
                                                other_charges=40
                                                total_brokerage_fee=brokerage+other_charges
                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                print("Profit or Loss point :",prof_loss)    

                                                print("Profit or loss Amount :",prof_loss_Rs)

                                                if (prof_loss < 1) &( prof_loss <= -2) :
                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                        ltp=symbol_data['data']['ltp']
                                                        print("LTP :",ltp)
                                                        prof_loss=ltp-exicution_price_1
                                                        print("Prof/Loss:",prof_loss)
                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                        print("prof/Loss :",round(prof_loss_Rs,2))
                                                        prof_loss_Rs=round(prof_loss_Rs,2)

                                                        print("vimal u r not yet profitable")
                                                        
                                                        print("Stay calm nd focused and energetic")

                                                        if ltp < SL_modi_price :
                                                                print("Stop loss is been Exicuted  < = 2")
                                                                print("breaking  first while loop of < 1")
                                                        
                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                data.save()
                                                                return redirect(nifty_option_data)
                                                                

                                                                exit("Stoping Exicution by python (ltp is less than SL or<-2)")
                                                                
                                                                
                                                elif (prof_loss >  3) & (prof_loss < 6):
                                                                shifting_percenatge=70
                                                                print("shifting stop loss insted second while loop")
                                                                print("profit point is > 3 and < 6")
                                                                # shift stop loss percentaage wise
                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                print("shifting Point :",shifting_point)
                                                                SL_modi_price_1= exicution_price_1 + shifting_point
                                                                SL_modi_price_1 = round(SL_modi_price_1, 2)
                                                                print("stop loss Modification price :",SL_modi_price_1)

                                                                try:
                                                                        orderparams=           {
                                                                                "variety":"NORMAL",
                                                                                "orderid":order_id,
                                                                                "ordertype":"LIMIT",
                                                                                "producttype":"INTRADAY",
                                                                                "duration":"DAY",
                                                                                "price":SL_modi_price_1,
                                                                                "quantity":qty,
                                                                                "tradingsymbol": symbol,
                                                                                "symboltoken":symbol_token,
                                                                                "exchange":exch_seg
                                                                                }
                                                                

                                                                        orderId=obj.placeOrder(orderparams)
                                                                        print("The order id is: {}".format(orderId))
                                                                        order_id=format(orderId)
                                                                        print(order_id)

                                                                except Exception as e:
                                                                        
                                                                        print("Order placement failed: {}".format(e))
                                                                
                                                                while True :
                                                                                print("Exicuting third  while of > 3 ")
                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                ltp=symbol_data['data']['ltp']

                                                                                print("order Modified price :",SL_modi_price_1)
                                                                                print("currrent LTP :",ltp)

                                                                                prof_loss=ltp-exicution_price_1

                                                                                brokerage=40
                                                                                other_charges=40
                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                if ltp <= SL_modi_price_1 :
                                                                                        
                                                                                        print("stop loss is been exicucted")
                                                                                        print("breaking while of < 3 SL")
                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                        data.save()
                                                                                        return redirect(nifty_option_data)
                                                                

                                                                                elif (prof_loss >  6) & (prof_loss < 9):
                                                                                        shifting_percenatge=70
                                                                                        print("shifting stop loss")
                                                                                        print("profit point is > 3 and < 6")
                                                                                        # shift stop loss percentaage wise
                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                        print(shifting_point)
                                                                                        SL_modi_price_2= exicution_price_1 + shifting_point
                                                                                        SL_modi_price = round(SL_modi_price_2, 2)
                                                                                        print("stop loss Modifiaction price :",SL_modi_price_2)

                                                                                        try:
                                                                                                orderparams=           {
                                                                                                        "variety":"NORMAL",
                                                                                                        "orderid":order_id,
                                                                                                        "ordertype":"LIMIT",
                                                                                                        "producttype":"INTRADAY",
                                                                                                        "duration":"DAY",
                                                                                                        "price":SL_modi_price_2,
                                                                                                        "quantity":qty,
                                                                                                        "tradingsymbol": symbol,
                                                                                                        "symboltoken":symbol_token,
                                                                                                        "exchange":exch_seg
                                                                                                        }
                                                                                        

                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                print("The order id is: {}".format(orderId))
                                                                                                order_id=format(orderId)
                                                                                                print(order_id)
                                                                                                

                                                                                        except Exception as e:
                                                                                                print("Order placement failed: {}".format(e))

                                                                                        while True :

                                                                                                print("Exicuting third  while of > 3 ")
                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                print("order Modified price :",SL_modi_price_2)
                                                                                                print("currrent LTP :",ltp)

                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                brokerage=40
                                                                                                other_charges=40
                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                prof_loss_Rs=round(prof_loss_Rs,2)

                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                if ltp <= SL_modi_price_2 :
                                                                                                
                                                                                                        print("stop loss is been exicucted")
                                                                                                        print("breaking while of < 2 SL")
                                                                                                        
                                                                                                        Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                        data.save()
                                                                                                        return redirect(nifty_option_data)
                                                                                                        exit("closing exicution")
                                                                                                        

                                                                                                elif (prof_loss >  6) & (prof_loss < 9):
                                                                                                        shifting_percenatge=80
                                                                                                        print("shifting stop loss")
                                                                                                        print("profit point is > 6 and < 9")
                                                                                                        # shift stop loss percentaage wise
                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                        print(shifting_point)
                                                                                                        SL_modi_price_3= exicution_price_1 + shifting_point
                                                                                                        SL_modi_price_3 = round(SL_modi_price_3, 2)
                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_3)

                                                                                                        try:
                                                                                                                orderparams=           {
                                                                                                                        "variety":"NORMAL",
                                                                                                                        "orderid":order_id,
                                                                                                                        "ordertype":"LIMIT",
                                                                                                                        "producttype":"INTRADAY",
                                                                                                                        "duration":"DAY",
                                                                                                                        "price":SL_modi_price_3,
                                                                                                                        "quantity":qty,
                                                                                                                        "tradingsymbol": symbol,
                                                                                                                        "symboltoken":symbol_token,
                                                                                                                        "exchange":exch_seg
                                                                                                                        }
                                                                                                        

                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                order_id=format(orderId)
                                                                                                                print(order_id)
                                                                                                                
                                                                                                        except Exception as e:
                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                        while True :
                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                print("order Modified price :",SL_modi_price_3)
                                                                                                                print("currrent LTP :",ltp)

                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                brokerage=40
                                                                                                                other_charges=40
                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                if ltp <= SL_modi_price_3 :
                                                                                                                        
                                                                                                                        print("stop loss is been exicucted")
                                                                                                                        print("breaking while of < 6 SL")
                                                                                                                        
                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                        data.save()
                                                                                                                        return redirect(option_data_refresh)
                                                                                                                        exit("closing exicution")
                                                                                                                elif (prof_loss >  9) & (prof_loss < 12):
                                                                                                                        shifting_percenatge=80
                                                                                                                        print("shifting stop loss")
                                                                                                                        print("profit point is > 9 and < 12")
                                                                                                                        # shift stop loss percentaage wise
                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                        print(shifting_point)
                                                                                                                        SL_modi_price_4= exicution_price_1 + shifting_point
                                                                                                                        SL_modi_price_4 = round(SL_modi_price_4, 2)
                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_4)

                                                                                                                        try:
                                                                                                                                orderparams=           {
                                                                                                                                        "variety":"NORMAL",
                                                                                                                                        "orderid":order_id,
                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                        "duration":"DAY",
                                                                                                                                        "price":SL_modi_price_4,
                                                                                                                                        "quantity":qty,
                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                        "exchange":exch_seg
                                                                                                                                        }
                                                                                                                        

                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                order_id=format(orderId)
                                                                                                                                print(order_id)
                                                                                                                        except Exception as e:
                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                        while True :
                                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                print("order Modified price :",SL_modi_price_4)
                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                brokerage=40
                                                                                                                                other_charges=40
                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                if ltp <= SL_modi_price_4 :
                                                                                                                                        
                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                        print("breaking while of < 6 SL")
                                                                                                                                
                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                        data.save()
                                                                                                                                        return redirect(nifty_option_data)

                                                                                                                                elif (prof_loss >  12) & (prof_loss < 15):
                                                                                                                                        shifting_percenatge=80
                                                                                                                                        print("shifting stop loss")
                                                                                                                                        print("profit point is > 12 and <15")
                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                        print(shifting_point)
                                                                                                                                        SL_modi_price_6= exicution_price_1 + shifting_point
                                                                                                                                        SL_modi_price_6 = round(SL_modi_price_6, 2)
                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_6)

                                                                                                                                        try:
                                                                                                                                                orderparams=           {
                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                        "orderid":order_id,
                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                        "duration":"DAY",
                                                                                                                                                        "price":SL_modi_price_6,
                                                                                                                                                        "quantity":qty,
                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                        }
                                                                                                                                        

                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                order_id=format(orderId)
                                                                                                                                                print(order_id)
                                                                                                                                                

                                                                                                                                        except Exception as e:
                                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                                        while True :
                                                                                                                                                print("Exicuting third  while of > 6 ")
                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                print("order Modified price :",SL_modi_price_6)
                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                                brokerage=40
                                                                                                                                                other_charges=40
                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                if ltp <= SL_modi_price_6 :
                                                                                                                                                        
                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                        print("breaking while of < 12 SL")
                                                                                                                                                
                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                        data.save()
                                                                                                                                                        exit("closing exicution")


                                                                                                                                                elif (prof_loss >  15) & (prof_loss <20):
                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                        print(shifting_point)
                                                                                                                                                        SL_modi_price_7= exicution_price_1 + shifting_point
                                                                                                                                                        SL_modi_price_7 = round(SL_modi_price_7, 2)
                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_7)

                                                                                                                                                        try:
                                                                                                                                                                orderparams=           {
                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                        "price":SL_modi_price_7,
                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                        }
                                                                                                                                                        

                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                print(order_id)
                                                                                                                                                                

                                                                                                                                                        except Exception as e:
                                                                                                                                                                print("Order placement failed: {}".format(e))

                                                                                                                                                        while True :
                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                print("order Modified price :",SL_modi_price_7)
                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                prof_loss=ltp-exicution_price_1

                                                                                                                                                                brokerage=40
                                                                                                                                                                other_charges=40
                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                if ltp <= SL_modi_price_7:
                                                                                                                                                                        
                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                        print("breaking while of < 7 SL")
                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                        data.save()
                                                                                                                                                                        exit("closing exicution")
                                                                                                                                                                elif (prof_loss >  15) & (prof_loss <20):
                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                SL_modi_price_8= exicution_price_1 + shifting_point
                                                                                                                                                                                SL_modi_price_8= round(SL_modi_price_8, 2)
                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_8)

                                                                                                                                                                                try:
                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                "price":SL_modi_price_8,
                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                }
                                                                                                                                                                                

                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                while True :
                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                        print("order Modified price :",SL_modi_price_8)
                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                        if ltp <= SL_modi_price_8:
                                                                                                                                                                                                
                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                print("breaking while of < 7 SL")

                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                data.save()
                                                                                                                                                                                                return redirect(nifty_option_data)
                                                                
                
                                                                                                                                                                                        elif (prof_loss >  20) & (prof_loss <25):
                                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                                SL_modi_price_9= exicution_price_1 + shifting_point
                                                                                                                                                                                                SL_modi_price_9= round(SL_modi_price_9, 2)
                                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_9)

                                                                                                                                                                                                try:
                                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                                "price":SL_modi_price_9,
                                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                                }
                                                                                                                                                                                                

                                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                                while True :
                                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                        print("order Modified price :",SL_modi_price_9)
                                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                        if ltp <= SL_modi_price_9:
                                                                                                                                                                                                                
                                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                                print("breaking while of <  20 ")
                                                                                                                                                                                                                
                                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                data.save()
                                                                                                                                                                                                                return redirect(nifty_option_data)
                                                                
                                                                                                                                                                                                                exit("closing exicution")
                                                                                                                                                                                                        
                                                                                                                                                                                                        elif (prof_loss >  20) & (prof_loss <25):
                                                                                                                                                                                                                shifting_percenatge=90
                                                                                                                                                                                                                print("shifting stop loss")
                                                                                                                                                                                                                print("profit point is > 15 ")
                                                                                                                                                                                                                # shift stop loss percentaage wise
                                                                                                                                                                                                                shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                                print(shifting_point)
                                                                                                                                                                                                                SL_modi_price_10= exicution_price_1 + shifting_point
                                                                                                                                                                                                                SL_modi_price_10= round(SL_modi_price_10, 2)
                                                                                                                                                                                                                print("stop loss Modifiaction price :",SL_modi_price_10)

                                                                                                                                                                                                                try:
                                                                                                                                                                                                                        orderparams=           {
                                                                                                                                                                                                                                "variety":"NORMAL",
                                                                                                                                                                                                                                "orderid":order_id,
                                                                                                                                                                                                                                "ordertype":"LIMIT",
                                                                                                                                                                                                                                "producttype":"INTRADAY",
                                                                                                                                                                                                                                "duration":"DAY",
                                                                                                                                                                                                                                "price":SL_modi_price_10,
                                                                                                                                                                                                                                "quantity":qty,
                                                                                                                                                                                                                                "tradingsymbol": symbol,
                                                                                                                                                                                                                                "symboltoken":symbol_token,
                                                                                                                                                                                                                                "exchange":exch_seg
                                                                                                                                                                                                                                }
                                                                                                                                                                                                                

                                                                                                                                                                                                                        orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                        print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                        order_id=format(orderId)
                                                                                                                                                                                                                        print(order_id)
                                                                                                                                                                                                                except Exception as e:
                                                                                                                                                                                                                        print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                while True :
                                                                                                                                                                                                                        print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                        symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                        ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                        print("order Modified price :",SL_modi_price_10)
                                                                                                                                                                                                                        print("currrent LTP :",ltp)

                                                                                                                                                                                                                        prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                        brokerage=40
                                                                                                                                                                                                                        other_charges=40
                                                                                                                                                                                                                        total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                        prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                        print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                        print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                        if ltp <= SL_modi_price_10:
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                print("stop loss is been exicucted")
                                                                                                                                                                                                                                print("breaking while of <  20 ")
                                                                                                                                                                                                                                
                                                                                                                                                                                                                                data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                        Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                data.save()
                                                                                                                                                                                                                                return redirect(nifty_option_data)

                                                                                                                                                                                                                                exit("closing exicution")

                                                                                                                                                                                                                        elif (prof_loss >  25) & (prof_loss <30):
                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                        # shift stop loss percentaage wise
                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/100)*prof_loss
                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                        SL_modi_price_11= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                        SL_modi_price_11= round(SL_modi_price_11, 2)
                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_11)

                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                        "price":SL_modi_price_11,
                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_11)
                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                if ltp <= SL_modi_price_11:
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                        return redirect(nifty_option_data)
                                                                                                                        

                                                                                                                                                                                                                                                elif (prof_loss >  30) & (prof_loss <35):
                                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                                        #shift stop loss percentaage wise

                                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/90 )*prof_loss
                                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                                        SL_modi_price_12= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                                        SL_modi_price_12= round(SL_modi_price_12, 2)
                                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price_12)

                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                                        "price":SL_modi_price_12,
                                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_12)
                                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                                if ltp <= SL_modi_price_12: 
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                                        exit("closing exicution")
                                                                                                                                                                                                                                                                elif (prof_loss >  35) & (prof_loss <50):
                                                                                                                                                                                                                                                                        shifting_percenatge=90
                                                                                                                                                                                                                                                                        print("shifting stop loss")
                                                                                                                                                                                                                                                                        print("profit point is > 15 ")
                                                                                                                                                                                                                                                                        #shift stop loss percentaage wise

                                                                                                                                                                                                                                                                        shifting_point=(shifting_percenatge/90 )*prof_loss
                                                                                                                                                                                                                                                                        print(shifting_point)
                                                                                                                                                                                                                                                                        SL_modi_price_13= exicution_price_1 + shifting_point
                                                                                                                                                                                                                                                                        SL_modi_price_13= round(SL_modi_price_13, 2)
                                                                                                                                                                                                                                                                        print("stop loss Modifiaction price :",SL_modi_price)

                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                orderparams=           {
                                                                                                                                                                                                                                                                                        "variety":"NORMAL",
                                                                                                                                                                                                                                                                                        "orderid":order_id,
                                                                                                                                                                                                                                                                                        "ordertype":"LIMIT",
                                                                                                                                                                                                                                                                                        "producttype":"INTRADAY",
                                                                                                                                                                                                                                                                                        "duration":"DAY",
                                                                                                                                                                                                                                                                                        "price":SL_modi_price_13,
                                                                                                                                                                                                                                                                                        "quantity":qty,
                                                                                                                                                                                                                                                                                        "tradingsymbol": symbol,
                                                                                                                                                                                                                                                                                        "symboltoken":symbol_token,
                                                                                                                                                                                                                                                                                        "exchange":exch_seg
                                                                                                                                                                                                                                                                                        }
                                                                                                                                                                                                                                                                        

                                                                                                                                                                                                                                                                                orderId=obj.placeOrder(orderparams)
                                                                                                                                                                                                                                                                                print("The order id is: {}".format(orderId))
                                                                                                                                                                                                                                                                                order_id=format(orderId)
                                                                                                                                                                                                                                                                                print(order_id)
                                                                                                                                                                                                                                                                        except Exception as e:
                                                                                                                                                                                                                                                                                print("Order placement failed: {}".format(e))
                                                                                                                                                                                                                                                                        while True :
                                                                                                                                                                                                                                                                                print("Exicuting third  while of > 7 ")
                                                                                                                                                                                                                                                                                symbol_data=obj.ltpData(exch_seg,symbol,symbol_token)
                                                                                                                                                                                                                                                                                ltp=symbol_data['data']['ltp']

                                                                                                                                                                                                                                                                                print("order Modified price :",SL_modi_price_13)
                                                                                                                                                                                                                                                                                print("currrent LTP :",ltp)

                                                                                                                                                                                                                                                                                prof_loss=ltp-exicution_price_1
                                                                                                                                                                                                                                                                                brokerage=40
                                                                                                                                                                                                                                                                                other_charges=40
                                                                                                                                                                                                                                                                                total_brokerage_fee=brokerage+other_charges
                                                                                                                                                                                                                                                                                prof_loss_Rs=(prof_loss*50 )-total_brokerage_fee
                                                                                                                                                                                                                                                                                print("Profit or Loss point :",prof_loss)    

                                                                                                                                                                                                                                                                                print("Profit or loss Amount :",prof_loss_Rs)
                                                                                                                                                                                                                                                                                if ltp <= SL_modi_price_13: 
                                                                                                                                                                                                                                                                                        print("stop loss is been exicucted")
                                                                                                                                                                                                                                                                                        print("breaking while of <  20 ")
                                                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                        data=Order_db(Exicuted_orderId=Main_orderId,symbol=symbol,Exicuted_p=exicution_price_1,qty=qty,order_status=fst_order_status,profit_Loss_amnt=prof_loss_Rs
                                                                                                                                                                                                                                                                                        ,CE_IV=ce_IV,CE_OI=ce_oi,PE_OI=pe_oi,PE_IV=pe_IV,CE_VOLM=CE_vol,PE_VOLM=PE_vol,Date_time=dt_string,
                                                                                                                                                                                                                                                                                                Mood=mood,Market_condition=mrkt_con,Preparation=prep,Thought=thought)
                                                                                                                                                                                                                                                                                        data.save()
                                                                                                                                                                                                                                                                                        return redirect(nifty_option_data)
                                                                
                                                                                                                                                                                                                                                                                        exit("closing exicution")
                                
                                   ###     contents={"Main order ID":Main_orderId,"SL order ID":SL_orderId,"fst_order_status":fst_order_status,"SL_order_status":SL_order_status}
                                        
                                    #    return render(request,'option_exicuted_data.html',contents)

                               # contents={"Main order ID":Main_orderId,"SL order ID":SL_orderId,"fst_order_status":fst_order_status,"SL_order_status":SL_order_status}
                                # return render(request,'option_data.html',contents)

