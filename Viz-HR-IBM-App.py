# https://docs.spyder-ide.org/current/installation.html#install-standalone
#!python -m venv viz-env # Take some minutes
#!viz-env\Scripts\activate.bat
#  Take some minutes
#!conda install spyder numpy scipy pandas matplotlib sympy cython streamlit altair vega_datasets
# !conda install -c conda-forge streamlit altair vega_datasets
#!pip install streamlit

# github process
# https://www.geeksforgeeks.org/devops/how-to-deploy-python-project-on-github/
# git init
# git config --global user.name "alexzzlin"
# git config --global user.email "alexzzlin@github.com"

# To view this Streamlit app on a browser, run it with the following command
# in the Powershell Prompt or Console Terminal
# streamlit run D:\UCB-MSDS\Viz_Course\Project\Viz-HR-IBM-App.py
import altair as alt
import streamlit as st
import numpy as np
from vega_datasets import data
# Import our data processing library (note: you may have to install this!)
import pandas as pd

# Loading the cars dataset
df = data.cars()

# Let's use this to upload a sample dataset and show the start of the dataset
# Note that you need to download the dataset and make sure it's in the same
# directory as your notebook
# data= pd.read_csv("employee_data.csv")
# hr_data= pd.read_csv("EmployeeRevisionDataset.csv")
hr_data = pd.read_csv("D:/UCB-MSDS/Viz_Course/Project/HR-Employee-Attrition.csv")
#hr_data.head()

# List of quantitative data items
item_list = [
    col for col in df.columns if df[col].dtype in ['float64', 'int64']]

# List of Origins
origin_list = list(df['Origin'].unique())

# Store the SPLOM
# List of quantitative data items
list_factors = ["Age", 'DailyRate', "DistanceFromHome",
                "EnvironmentSatisfaction", "RelationshipSatisfaction",
                "JobSatisfaction", "PerformanceRating", "YearsAtCompany",
                "YearsInCurrentRole", "YearsSinceLastPromotion"]

list_focus_factors = ["Age", 'DailyRate', "DistanceFromHome",
                      "EnvironmentSatisfaction", "RelationshipSatisfaction",
                      "JobSatisfaction", 
                      "YearsInCurrentRole", "YearsSinceLastPromotion"]


hr_data_quan = hr_data[list_factors]
corr = hr_data_quan.corr().stack().reset_index()
corr.columns = ['var1', 'var2', 'correlation']
# Sort by 'var1' then 'var2'
corr = corr.sort_values(by=['var1', 'var2'])
# print(corr.shape[0])

# Create a boolean mask for the upper triangle (keeping the diagonal, k=1)
mask = np.triu(np.ones(len(list_factors))).astype(bool)

# mask.flatten().shape
# Apply the mask to filter out the upper triangle data
corr_lower_triangle = corr[mask.flatten()]
# corr_lower_triangle.shape
corr_lower_triangle["correlation"] = corr_lower_triangle["correlation"].round(3)
#corr_lower_triangle

# Create the heatmap
correlations_chart = alt.Chart(corr_lower_triangle).mark_rect().encode(
    x=alt.X('var1:O', title=None),
    y=alt.Y('var2:O', title=None),
    color='correlation:Q',
    tooltip=['var1', 'var2', 'correlation']
).properties(
    title='Lower Triangular Correlation Matrix',
    width=300, height=300
).configure_axis(labelFontSize=14)
#).mark_text().encode(
#    text=alt.Text('correlation:Q', format='.2f'),  # Format to 2 decimal places
#    color=alt.value('black') # Set text color
#)

# correlations_chart.display()

ht_twyrs = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X("TotalWorkingYears", bin=True, title='binned x values'),
    y=alt.Y('count()', title='counts in x'),
    color='Attrition',
    tooltip='JobRole'
).interactive().properties(width=300, height=300)

ht_yrs_cr = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X("YearsInCurrentRole", bin=True, title='binned x values'),
    y=alt.Y('count()', title='counts in x'),
    color='Attrition',
    tooltip='JobRole'
).interactive().properties(width=300, height=300)

# ht_twyrs | ht_yrs_cr

hr_data_active = hr_data[hr_data["Attrition"] != "Yes"]
hr_data_attrited = hr_data[(hr_data["Attrition"] == "Yes")]

ht_active_age = alt.Chart(hr_data_active).mark_bar().encode(
    x=alt.X("Age", bin=True, title='binned x values'),
    y=alt.Y('count()', title='counts in x')
)

ht_attrited_age = alt.Chart(hr_data_attrited).mark_bar().encode(
    x=alt.X("Age", bin=True, title='binned x values'),
    y=alt.Y('count()', title='counts in x')
)

ht_age_dists = ht_active_age|ht_attrited_age
#ht_age_dists.display()

ht_age_dists = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X("Age:Q", bin=True, title='Binned-Age Values'),
    y=alt.Y('count()', title='Vounts in Binned-Age'),
    color="Attrition"
)

#ht_age_dists

# Create the countplot
job_role_status_count_chart = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X('count(Attrition):Q', stack='zero'),  # Categorical variable on the x-axis
    y=alt.Y('JobRole:N'),   # Count of records on the y-axis
    color='Attrition:N' # Color the bars by category
).properties(
    title='Workforce Attrition Distribution by Job Role'
)

#job_role_status_count_chart.display()

# Create the countplot
job_role_emp_status_pct_chart = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X('count(Attrition):Q', stack='normalize', title=None),  # Categorical variable on the x-axis
    y=alt.Y('JobRole:N'),   # Count of records on the y-axis
    color='Attrition:N' # Color the bars by category
).properties(
    title='Workforce Active vs. Attrition Distribution by Job Role',
    width=300, height=200
).configure_axis(labelFontSize=13)

# job_role_emp_status_pct_chart.display()

# Create the column of YYYY 
df['YYYY'] = df['Year'].apply(lambda x: x.year)
min_year = df['YYYY'].min()
max_year = df['YYYY'].max()

min_dist = hr_data['DistanceFromHome'].min()
max_dist = hr_data['DistanceFromHome'].max()
charts_type = ["Stacked Bar Chart", "Histogram"]
# List of Job Roles
job_role_list = list(hr_data['JobRole'].unique())
# List of Departments
dept_list = list(hr_data['Department'].unique())
# List of Education
edu_list = list(hr_data['Education'].unique())
# List of JobInvolvement
job_inv_list = list(hr_data['JobInvolvement'].unique())

st.set_page_config(layout="wide")

# Sidebar
st.sidebar.title("Dashboard of IBM HR")
#st.sidebar.markdown('###')
#st.sidebar.markdown("### *Factors*")

#start_dist, end_dist = st.slider(
#    "Commuting Distance",
#    min_value=min_dist, max_value=max_dist,
#    value=(min_dist, max_dist))

#start_year, end_year = st.sidebar.slider(
#    "Period",
#    min_value=min_year, max_value=max_year,
#    value=(min_year, max_year))

#st.sidebar.markdown('###')
#origins = st.sidebar.multiselect('Origins', origin_list,
#                                 default=origin_list)

# st.sidebar.markdown('###')
#item1 = st.sidebar.selectbox('Item 1', item_list, index=0)
#item2 = st.sidebar.selectbox('Item 2', item_list, index=3)

#job_role = st.sidebar.multiselect('Job Role', job_role_list, default=job_role_list)
dept = st.sidebar.multiselect('Department', dept_list, default=dept_list)
# edu = st.sidebar.multiselect('Education', edu_list, default=edu_list)
#job_inv = st.sidebar.multiselect('Job Involvement', job_inv_list, default=job_inv_list)

#st.markdown('###')
# chartType = st.sidebar.selectbox('Chart Type', charts_type, index=0)
itemQF = st.sidebar.selectbox('Quantative Factor', list_focus_factors, index=0)
# itemY = st.sidebar.selectbox('Factor 2', list_factors, index=1)

# df_rng = df[(df['YYYY'] >= 1900) & (df['YYYY'] <= 2025)]

#source = df_rng[df_rng['Origin'].isin(origins)]
hr_source = hr_data[hr_data['Department'].isin(dept)]

# Content
# base = alt.Chart(source).properties(height=300)

#bar = base.mark_bar().encode(
#    x=alt.X('count(Origin):Q', title='Number of Records'),
#    y=alt.Y('Origin:N', title='Origin'),
#    color=alt.Color('Origin:N', legend=None)
#)

ht_factor_q = alt.Chart(hr_source).mark_bar().encode(
    x=alt.X(itemQF+":Q", bin=True, title='binned x values'),
    y=alt.Y('count()', title='counts in '+itemQF),
    color=alt.Color('Attrition',  legend=None),
    tooltip='JobRole'
).interactive().properties(width=300, height=300)

#point = base.mark_circle(size=50).encode(
#    x=alt.X(item1 + ':Q', title=item1),
#    y=alt.Y(item2 + ':Q', title=item2),
#    color=alt.Color('Origin:N', title='',
#                    legend=alt.Legend(orient='bottom-left'))
#)

#line1 = base.mark_line(size=5).encode(
#    x=alt.X('yearmonth(Year):T', title='Date'),
#    y=alt.Y('mean(' + item1 + '):Q', title=item1),
#    color=alt.Color('Origin:N', title='',
#                    legend=alt.Legend(orient='bottom-left'))
#)

#line2 = base.mark_line(size=5).encode(
#    x=alt.X('yearmonth(Year):T', title='Date'),
#    y=alt.Y('mean(' + item2 + '):Q', title=item2),
#    color=alt.Color('Origin:N', title='',
#                    legend=alt.Legend(orient='bottom-left'))
#)

# Layout (Content)
left_column, right_column = st.columns([2, 1])

right_column.markdown('**_' + itemQF + '_ Scale**')
right_column.altair_chart(ht_factor_q, use_container_width=True)

#left_column.markdown(
#    '**Number of Records (' + str(start_year) + '-' + str(end_year) + ')**')
#left_column.altair_chart(ht_age_dists, use_container_width=True)
left_column.markdown('**Workforce Attrition Distribution by Job Role**')
left_column.altair_chart(job_role_status_count_chart, use_container_width=True)

#left_right_column = st.columns(2)

left_column.markdown('**Correlation Matrix**')
left_column.altair_chart(correlations_chart, use_container_width=True)