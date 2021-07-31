#%%
import pandas as pd
from sklearn.linear_model import LinearRegression
#%%
data = pd.read_excel("data/data.xlsx")

# %%
data.describe(include='all')
# %%
candidate_name = 'ABCDE00212'
machine = data[data['candidate']==candidate_name]
# %%
events = machine['event'].unique()
# %%
events[0]
events.size
# %%
fail_date_overall = 1000000000
fail_event = None
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
            # If severity_2 data is considered, threshold = (max of severity_3_data + 50%)
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

# %%
print(f"Machine fails at {fail_date_overall} due to failure at {fail_event}")

# %%
