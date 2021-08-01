#%%
import pandas as pd
from sklearn.linear_model import LinearRegression
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


data = pd.read_excel("data/data.xlsx")
data.drop(inplace=True, index=data['date'].str.isnumeric().dropna().index)

# data.describe(include='all')


app = FastAPI()
print("server_start")

app.mount("/public", StaticFiles(directory="public"), name="static")

@app.get("/get_machine_life/")
async def get_details(id):

    machine = data[data['candidate']==id]

    # if id is not found return error
    if (machine["date"].count()<=0):
        return {"error":"invalid_id"}

    events = machine['event'].unique()
        
    fail_date_overall = 1000000000
    fail_event = None
    rul = None
    for i in range(events.size):
        # print(events[i])
        data_event_i = machine[machine['event'] == events[i]]
        data_event_i_svr1 = data_event_i[data_event_i['svrty_level'] == 1]

        # If severity_1 data is found, threshold = (max of severity_1_data + 5%) 
        if(data_event_i_svr1.size > 0):
            threshold = data_event_i_svr1['units'].max()*1.05
            # print(threshold)
        else:
            # If severity_2 data is considered, threshold = (max of severity_2_data + 25%)
            data_event_i_svr2 = data_event_i[data_event_i['svrty_level'] == 2]
            if(data_event_i_svr2.size > 0):
                threshold = data_event_i_svr2['units'].max()*1.25
                # print(threshold)
            else:
                # If severity_3 data is considered, threshold = (max of severity_3_data + 50%)
                data_event_i_svr3 = data_event_i[data_event_i['svrty_level'] == 3]
                threshold = data_event_i_svr3['units'].max()*1.50
                # print(threshold)

        model = LinearRegression()
        model.fit(data_event_i['units'].values.reshape(-1,1), data_event_i['date'].values)
        fail_date = model.predict([[threshold]])[0]
        # print(fail_date)

        if fail_date<fail_date_overall:
            fail_date_overall=fail_date
            fail_event = events[i]
            rul = fail_date - data_event_i['date'].max()
    
    print(f"Machine fails at {fail_date_overall} due to failure at {fail_event}")
    return {"machine_id": id, "fail_event": fail_event, "RUL":rul} 


