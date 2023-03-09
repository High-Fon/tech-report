# 1. Importing packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 2. Importing datasets

# Imported from Kaggle using their API command, is read from the unzipped data file
df = pd.read_csv('sleep_efficiency.csv', index_col='ID')

url = 'https://raw.githubusercontent.com/reisanar/datasets/master/SleepStudy.csv'
df2 = pd.read_csv(url)

# 3. Data analysis

### 3.1. Preliminary Dataframe Analysis
print(df.shape)
print(df.dtypes)
df.info()
df.head()
df.describe()

print(df2.shape)
print(df2.dtypes)
df2.info()
df2.head()
df2.describe()

### 3.1.1 Deleting Columns in second dataframe
df2.drop(columns=['ClassYear', 'DASScore', 'LarkOwl', 'NumEarlyClass', 'EarlyClass', 'GPA', 'ClassesMissed', 'CognitionZscore', 'PoorSleepQuality', 'DepressionScore'])

### 3.2. Adjusting Columns
# Rename columns
df.rename(columns = {'Wakeup time':'wakeup_time', 'Sleep duration':'sleep_duration',"Sleep efficiency":"sleep_efficiency",
                     "REM sleep percentage":"REM_sleep_percentage","Deep sleep percentage":"deep_sleep_percentage",
                     "Light sleep percentage":"light_sleep_percentage","Caffeine consumption":"caffeine_consumption",
                     "Alcohol consumption":"alcohol_consumption","Smoking status":"smoking_status","Exercise frequency":"exercise_frequency", 
                     'Age': 'age', 'Gender': 'gender', 'Bedtime': 'bedtime', 'Awakenings': 'awakenings'}, inplace = True)

df2.rename(columns = {'AnxietyScore': 'anxiety_score', 'StressScore': 'stress_score', 'DepressionStatus': 'depression_status',
                    'AnxietyStatus': 'anxiety_status', 'AlcoholUse': 'alcohol_use', 'WeekdayBed': 'weekday_bed', 
                    'WeekdayRise': 'weekday_rise', 'Weekday sleep': 'weekday_sleep', 'WeekendBed': 'weekend_bed', 
                    'WeekendRise': 'weekend_rise', 'WeekendSleep': 'weekend_sleep', 'AverageSleep': 'average_sleep', 
                    'AllNighter': 'all_nighter'}, inplace=True)
# Result
df.head()

# Create new columns with actual sleep time. From that new columns can be created with time of REM, deep, and light sleep.
# Sleep time = duration * efficiency
df['actual_sleep_time']=df['sleep_duration']*df['sleep_efficiency']

# REM/deep/light sleep time = Sleep time * (REM/deep/light percentage / 100)
df['REM_sleep_time']=(df['actual_sleep_time']*df['REM_sleep_percentage']/100).round(2)
df['deep_sleep_time']=(df['actual_sleep_time']*df['deep_sleep_percentage']/100).round(2)
df['light_sleep_time']=(df['actual_sleep_time']*df['light_sleep_percentage']/100).round(2)

### 3.3. Data visualisation


# General data exploration charts


## 1
gender_ratio = px.pie(df, values=df.index, names='gender')
gender_ratio.update_layout(title='Ratio of male and female', legend_title='Gender')


## 2
age_dist = px.histogram(df, x='age', hover_data=['age'], labels={'age': 'Age'}, title='Age distribution of the population')
age_dist.update_yaxes(title={'text':'Count'})

## 3
age_slp_dur = go.Figure()
age_slp_dur.add_trace(go.Scatter(x=df.age, y=df.actual_sleep_time, mode='markers', marker={'color':df.sleep_efficiency, 'colorbar':{'title': 'Sleep efficiency'}}),)

age_slp_dur.update_layout(title={'text':'Actual sleep time by age'},
                          xaxis={'rangeslider':{'visible':True, 'borderwidth': 1, 'bordercolor':'#3101c1'}})
age_slp_dur.update_xaxes({'title':'Age'})
age_slp_dur.update_yaxes({'title':'Actual sleep time (h)'})

## 4
plots_box = go.Figure()

plots_box.add_trace(go.Box(y=df.sleep_duration, name='Sleep duration (dataset 1)'))
plots_box.add_trace(go.Box(y=df2.average_sleep, name='Average sleep (dataset 2)'))

plots_box.update_layout(title={'text': 'Comparing the sleep duration in the two datasets'}, showlegend=False)
plots_box.update_yaxes(title='Sleep duration (h)')


# Impact of substances charts


## Smoking


### 1
smoke_box = px.box(df, x='smoking_status', y='sleep_efficiency', 
             labels={'smoking_status': 'Smokes', 'sleep_efficiency': 'Sleep efficiency'}, 
             title='Impact of smoking on sleep efficiency', notched=True)
smoke_box.update_layout(showlegend=False, boxgap=0.8)


### 2
perc_box = go.Figure()

perc_box.add_trace(go.Box(x=df.smoking_status, y=df.deep_sleep_percentage, name='Deep sleep'))
perc_box.add_trace(go.Box(x=df.smoking_status, y=df.light_sleep_percentage, name='Light sleep'))
perc_box.add_trace(go.Box(x=df.smoking_status, y=df.REM_sleep_percentage, name='REM sleep'))

perc_dropdown = [  {'label': 'All', 'method': 'update','args': [{'visible': [True, True, True]}, {'title': 'All'}]},
                      {'label': 'Deep sleep', 'method': 'update','args': [{'visible': [True, False, False]}, {'title': 'Deep sleep'}]},  
                      {'label': 'Light sleep', 'method': 'update','args': [{'visible': [False, True, False]}, {'title': 'Light sleep'}]},  
                      {'label': 'REM sleep', 'method': "update",'args': [{"visible": [False, False, True]}, {'title': 'REM sleep'}]}]


perc_box.update_layout(boxmode='group', title={'text': 'Impact of smoking on the ratio of deep, light, and REM sleep.'}, legend={'title':'Types of sleep'},
                       updatemenus=[{'type': "dropdown",'x': 1.2, 'y': 0.5,'showactive': True,'active': 0,'buttons': perc_dropdown}])
perc_box.update_xaxes(patch={'title':'Smokes'})
perc_box.update_yaxes(patch={'title':'Percentage of time asleep'})



## Alcohol 


### 1
alcohol_box = px.box(df, x='alcohol_consumption', y='sleep_efficiency',
             labels={'alcohol_consumption': 'Alcohol consumption (oz)', 'sleep_efficiency': 'Sleep efficiency'},
             title='Impact of alcohol on sleep efficiency', notched=True)
alcohol_box.update_layout(showlegend=False)


### 2
alc_box = go.Figure()

alc_box.add_trace(go.Box(x=df.alcohol_consumption, y=df.deep_sleep_percentage, name='Deep sleep'))
alc_box.add_trace(go.Box(x=df.alcohol_consumption, y=df.light_sleep_percentage, name='Light sleep'))
alc_box.add_trace(go.Box(x=df.alcohol_consumption, y=df.REM_sleep_percentage, name='REM sleep'))

alc_dropdown = [{'label': 'All', 'method': 'update', 'args': [{'visible': [True, True, True]}, {'title': 'All'}]},
                {'label': 'Deep sleep', 'method': 'update', 'args': [{'visible': [True, False, False]}, {'title': 'Deep sleep'}]},
                {'label': 'Light sleep', 'method': 'update', 'args': [{'visible': [False, True, False]}, {'title': 'Deep sleep'}]},
                {'label': 'REM sleep', 'method': 'update', 'args': [{'visible': [True, False, False]}, {'title': 'REM sleep'}]}]

alc_box.update_layout(boxmode='group', title={'text': 'Impact of alcohol on the percentage of deep, light and REM sleep.'},
                        legend={'title': 'Types of sleep'},
                        updatemenus=[{'type': 'dropdown', 'x': 1.2, 'y': 0.5, 'showactive': True, 'active': 0, 'buttons': alc_dropdown}])
alc_box.update_xaxes(patch={'title':'Amount of alcohol (oz)'})
alc_box.update_yaxes(patch={'title':'Percentage of time asleep'})



## Caffeine


### 1
caff_eff = px.box(df, x='caffeine_consumption', y='sleep_efficiency',
             labels={'caffeine_consumption': 'Caffeine consumption (mg)', 'sleep_efficiency': 'Sleep efficiency'},
             title='Impact of caffeine on sleep efficiency')


### 2
caff_perc = go.Figure() 
caff_perc.update_layout(boxmode='group', xaxis={'rangeslider':{'visible':True, 'borderwidth': 1, 'bordercolor':'#3101c1'}},title={'text':'Impact of caffeine consumption on the percentage of deep, light, and REM sleep'})
caff_perc.update_xaxes(title={'text':'Caffeine consumption (mg)'})
caff_perc.update_yaxes(title={'text':'Amount (h)'})


# 4. Streamlit Initialization


# App configuration
st.set_page_config(page_title='Studies on sleep efficiency')


#Title and introduction
st.title('Studies on sleep efficiency')
st.markdown('This tech report delves into the exploration of a sleep efficiency study. It contains information on 452 participants with a number of columns of information on each. The aim of this report is to delve into the impacts of substances on the overall quality of sleep. Each row contains the age and gender of the subject. For sleep statistics it contains the time the subject goes to bed, and when the subject wakes up. Furthermore, it displays the duration of sleep and the efficiency, which is the percentage of the duration actually spent asleep. Quality of sleep is recorded in the percentages of REM, deep, and light sleep and the number of awakenings. Lastly, factors on sleep quality are recorded in milligrams of caffeine, and ounces of alcohol consumed prior to going to bed. Also, whether the subject smokes and the amount of times the subject goes to the gym each week is recorded. To create more useful data the sleep efficiencies and percentages of REM, deep, and light sleep have been converted into hours and added into to new columns for each. This dataset was obtained through the Kaggle API and stored into a dataframe for analysis. The second dataset was collected through Github. While looking at the Github dataset it was decided to delete a number of columns that were deemed irrelevant to the subject of this report. This dataset centred on a group of university students. Mostly columns about happiness, depression, stress and anxiety because these were not deemed useful in comparison to the Kaggle dataset.')
st.dataframe(df)
st.caption('The Kaggle dataset of 452 subjects.')

#General data exploration section
st.header('General data exploration')
st.markdown('Before diving into the impacts of substances on sleep quality, the dataset is explored. This is done generally on the population. Firstly, the ratio between male and female participants is graphed. Secondly, the age distribution of the population is shown. Lastly, the sleep efficiency by age is plotted.')
gen1, gen2, gen3, gen4 = st.tabs(['Gender ratio', 'Age distribution', 'Time asleep by age', 'Comparison of datasets'])
with gen1:
    st.markdown('Below is a pie chart showing the ratio of male to female participants. The population is representative with roughly half of the population being male and female.')
    st.plotly_chart(gender_ratio, True)
with gen2:
    st.markdown('Below is a histogram that plots the age distribution of the population. This shows a good spread of participants of all ages.')
    st.plotly_chart(age_dist, True)
with gen3:
    st.markdown('Below is a chart showing the actual time spent asleep per participant with its colour representing the sleep efficiency. From the graph it is visible that participants that spent less time asleep generally also had a lower sleep efficiency. Meaning that these participants had a less restfull night of sleep.')
    st.code("""age_slp_dur = go.Figure()
age_slp_dur.add_trace(go.Scatter(x=df.age, y=df.actual_sleep_time, mode='markers', marker={'color':df.sleep_efficiency, 'colorbar':{'title': 'Sleep efficiency'}}),)

age_slp_dur.update_layout(title={'text':'Actual sleep time by age'},
                          xaxis={'rangeslider':{'visible':True, 'borderwidth': 1, 'bordercolor':'#3101c1'}})
age_slp_dur.update_xaxes({'title':'Age'})
age_slp_dur.update_yaxes({'title':'Actual sleep time (h)'})""")
    st.plotly_chart(age_slp_dur, True)
with gen4:
    st.markdown('Below the two datasets have been compared to check the validity of data. Given the sizes of the datasets it can be assumed both populations experience a similar length of nightrest. This is confirmed by the boxplot. The Github dataset population sleeps on average a little longer than the Kaggle dataset but the values are closed that it can be concluded that the data is validl.')
    st.plotly_chart(plots_box, True)


#Impact of substances section
st.header('Impact of substances on overall sleep quality')
st.markdown('After performing general data exploration it is possible to look deeper into the dataset to find correlation between the use of substances and sleep quality. It is already well known that certain substances can have adverse effects on the overall quality of sleep. This will be researched with the analysis of the dataset done in this chapter. Firstly, the effects of smoking on sleep qualityis shown. Secondly, the affects of alcohol are explored. Lastly, the relation between caffeine intake and sleep quality is shown.')


#Smoking section
st.subheader('Effects of smoking')
st.markdown('Firstly, the impact of smoking on the quality of sleep is explored. From the charts it is visible that smoking affects both sleep efficiency and the percentages of deep, light, and REM sleep. Smoking on average reduces sleep efficiency by 0,06. The interquartile range is extended from 0,73 - 0,91 to 0,55 - 0,88. This means that people who smoke experience a significant reduction in the restfulness of their sleep. This is further emphasized by the REM, deep, light sleep graph. In the sleep cycle, the most important parts of the cycle are deep and REM sleep. Deep sleep is attributed to bodily recovery and growth. It is believed to also bolster immune response and other key bodily processes. REM also provides similar benefits to essential cognitive functions like memory, learning and creativity. In subjects who smoke, it is seen that the amount of sleep spent in the deep sleep stage is decreased and light sleep increases. This means that the subject experiences significantly reduced restorative sleep. To summarize, smoking has a very negative effect on the quality of sleep. People who smoke spend less time per night asleep and of that time asleep less time is spent in restorative sleep cycles. This leads people to feel less refreshed after a full night\'s rest and can lead to cognitive issues after extended periods of use.')
smoke1, smoke2 = st.tabs(['Sleep efficiency', 'Percentage deep, light, and REM sleep'])
with smoke1:
    st.plotly_chart(smoke_box, True)
with smoke2:
    st.code("""perc_box = go.Figure()

perc_box.add_trace(go.Box(x=df.smoking_status, y=df.deep_sleep_percentage, name='Deep sleep'))
perc_box.add_trace(go.Box(x=df.smoking_status, y=df.light_sleep_percentage, name='Light sleep'))
perc_box.add_trace(go.Box(x=df.smoking_status, y=df.REM_sleep_percentage, name='REM sleep'))

perc_dropdown = [  {'label': 'All', 'method': 'update','args': [{'visible': [True, True, True]}, {'title': 'All'}]},
                      {'label': 'Deep sleep', 'method': 'update','args': [{'visible': [True, False, False]}, {'title': 'Deep sleep'}]},  
                      {'label': 'Light sleep', 'method': 'update','args': [{'visible': [False, True, False]}, {'title': 'Light sleep'}]},  
                      {'label': 'REM sleep', 'method': "update",'args': [{"visible": [False, False, True]}, {'title': 'REM sleep'}]}]


perc_box.update_layout(boxmode='group', title={'text': 'Impact of smoking on the ratio of deep, light, and REM sleep.'}, legend={'title':'Types of sleep'},
                       updatemenus=[{'type': "dropdown",'x': 1.2, 'y': 0.5,'showactive': True,'active': 0,'buttons': perc_dropdown}])
perc_box.update_xaxes(patch={'title':'Smokes'})
perc_box.update_yaxes(patch={'title':'Percentage of time asleep'})""")
    st.plotly_chart(perc_box, True)


#Alcohol Section
st.subheader('Effects of alcohol')
st.markdown('Another substance known to cause severe issues with sleep quality is alcohol. This has also been analyzed below. Similarly to smoking, alcohol affects sleep_efficiency and the sleep cycle. The alcohol consumption of participants has been measured in terms of ounces and goes up to five ounces consumed prior to sleeping. Participants who consumed one ounces where not impacted strongly with only a small decrease in sleep efficiency and even an increase in deep sleep. However, when participants consumed more than one ounce of alcohol prior to sleeping it resulted in a strong effect on the quality of the night rest. Those participants experienced a significant reduction of sleep efficiency of up to 20 percent. Their sleep cycles were similarly affected with a stark decrease of time spent in deep sleep. This led to an increase of time spent in light sleep, with time in REM sleep remaining mostly unaffected by the alcohol. Thus, it can be concluded that alcohol strongly impacts the restorative rest an individual receives and can thus lead to cognitive and physical issues when exposed to this substance for prolonged time. This is alongside the other risks that the consumption of alcohol poses to the body.')
alc1, alc2 = st.tabs(['Sleep efficiency', 'Percentage deep, light, and REM sleep'])
with alc1:
    st.plotly_chart(alcohol_box, True)
with alc2:
    st.plotly_chart(alc_box, True)

#Caffeine section
st.subheader('Effects of caffeine')
st.markdown('Caffeine is a natural substance known for stimulating the brain and nervous system. This theoretically means that when a person consumes caffeine it could  have a negative impact on their sleep. Through the visualisations it is visible that caffeine does not seem to have a strong effect on the sleep quality. On the contrary to what was expected, caffeine seems to slightly increase sleep efficiency and the interquartile range seems to constrict. It also seems to increase time spent in deep sleep while maintaining time spent in REM sleep. This can be further researched on a larger subset of people to get a more accurate picture of the situation. However, it can be concluded that caffeine does not have adverse effects on the sleep quality.')

col1, col2 = st.columns([3, 1])
plot = col1.radio('Select graph', ('Sleep efficiency', 'Percentages REM/deep/light'), index=0)

if plot == 'Sleep efficiency':
    offREMsleep = col2.checkbox('REM sleep', True, 1, disabled=True)
    offdeepsleep = col2.checkbox('Deep sleep', True, 2, disabled=True)
    offlightsleep = col2.checkbox('Light sleep', True, 3, disabled=True)

    st.plotly_chart(caff_eff, True)

if plot == 'Percentages REM/deep/light':
    REMsleep = col2.checkbox('REM sleep', True, 4)
    deepsleep = col2.checkbox('Deep sleep', True, 5)
    lightsleep = col2.checkbox('Light sleep', True, 6)

    if deepsleep:
        caff_perc.add_trace(go.Box(x=df.caffeine_consumption, y=df.deep_sleep_time, name='Deep sleep'))

    if lightsleep:
        caff_perc.add_trace(go.Box(x=df.caffeine_consumption, y=df.light_sleep_time, name='Light sleep'))
    
    if REMsleep:
        caff_perc.add_trace(go.Box(x=df.caffeine_consumption, y=df.REM_sleep_time, name='REM sleep'))
    
    st.plotly_chart(caff_perc, True)

# Conclusion

st.header('Conclusion')
st.markdown('The goal of this report was to confirm and outline the effects that certain substances have on the quality of sleep. Through data analysis and visualization it was confirmed that smoking and alcohol can have severe impacts on the quality of sleep a person can get at night. It was seen that alcohol and smoking reduces the efficiency with one sleeps at night. Alongside this, it was seen that this also impacts the amount of time spent in deep sleep. As this part of the cycle is essential to bodily recovery and growth this can have repercussions on the body and mind after extended exposure to one or both of these substances. Alcohol tends to have a stronger effect than smoking when the person consumes more than two ounces prior to sleeping. Caffeine has been found to not adversely impact sleep quality. On the contrary, it seems to offer minor benefits to sleep efficiency and deep sleep time. As this study was performed on only 452 subjects, this should be scaled up to more accurately investigate the effects of smoking and alcohol on both the short and long term. However, even without further research it can be said that reducing alcohol and stopping smoking will have a beneficial effect on the quality of sleep one experiences. This will also prevent health issues that both of these substances pose a risk to.')