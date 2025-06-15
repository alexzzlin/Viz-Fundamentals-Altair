# https://docs.spyder-ide.org/current/installation.html#install-standalone
# https://altair-viz.github.io/user_guide/customization.html
#!python -m venv viz-env # Take some minutes
#!viz-env\Scripts\activate.bat
#  Take some minutes
#!conda install spyder numpy scipy pandas matplotlib sympy cython streamlit altair vega_datasets
#!conda install -c conda-forge streamlit altair vega_datasets
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
import pandas as pd  # Import data processing library

# Download the dataset at the same github directory as this python script
hr_data = pd.read_csv("HR-Employee-Attrition.csv")
# hr_data = pd.read_csv("D:/UCB-MSDS/Viz_Course/Project/HR-Employee-Attrition.csv")
#hr_data.head()

# List of quantitative data items
list_q_factors = ["Age", 'DailyRate', "DistanceFromHome", "YearsAtCompany",
                  "YearsInCurrentRole", "YearsSinceLastPromotion"]

list_n_factors = ["EnvironmentSatisfaction", "RelationshipSatisfaction",
                  "JobSatisfaction", "PerformanceRating"]

list_factors = list_q_factors + list_n_factors

list_focus_factors = ["Age", 'DailyRate', "DistanceFromHome",
                      "EnvironmentSatisfaction", "RelationshipSatisfaction",
                      "JobSatisfaction", "YearsAtCompany"
                      "YearsInCurrentRole", "YearsSinceLastPromotion"]

# Construct & Compute Correlation matrix for quantitative factors
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
# corr_lower_triangle
# corr_lower_triangle["correlation"] = corr_lower_triangle["correlation"].round(3)

# Create the heatmap
correlations_chart = alt.Chart(corr_lower_triangle).mark_rect().encode(
    x=alt.X('var1:O', title=None),
    y=alt.Y('var2:O', title=None),
    color=alt.Color('correlation:Q').scale(reverse=True), # scheme="lightgreyred"
    tooltip=['var1', 'var2', 'correlation']
).properties(
    #title='Lower Triangular Correlation Matrix',
    width=300, height=300
).configure_axis(labelFontSize=13)
#).mark_text().encode(
#    text=alt.Text('correlation:Q', format='.2f'),  # Format to 2 decimal places
#    color=alt.value('black') # Set text color
#)

# correlations_chart.display()

hr_data_active = hr_data[hr_data["Attrition"] != "Yes"]
hr_data_attrited = hr_data[(hr_data["Attrition"] == "Yes")]

#ht_age_dists = alt.Chart(hr_data).mark_bar().encode(
#    x=alt.X("Age:Q", bin=True, title='Binned-Age Values'),
#    y=alt.Y('count():Q', title='Employee Count'),
#    color="Attrition"
#)

#ht_age_dists

# Create the countplot
job_role_status_count_chart = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X("count(Attrition):Q", stack="zero",
            title='Employee Count'),  # Categorical variable on the x-axis
    y=alt.Y("JobRole:N"),   # Count of records on the y-axis
    color="Attrition:N" # Color the bars by category
).properties(
    #title="Workforce Attrition Distribution by Job Role",
    width=300, height=300
)

#job_role_status_count_chart.display()

# Create the countplot
job_role_emp_status_pct_chart = alt.Chart(hr_data).mark_bar().encode(
    x=alt.X('count(Attrition):Q', stack='normalize', title=None),  # Categorical variable on the x-axis
    y=alt.Y('JobRole:N'),   # Count of records on the y-axis
    color='Attrition:N' # Color the bars by category
).properties(
    title='Workforce Active vs. Attrition Distribution by Job Role',
    width=300, height=400
).configure_axis(labelFontSize=13)

# job_role_emp_status_pct_chart.display()

min_dist = hr_data['DistanceFromHome'].min()
max_dist = hr_data['DistanceFromHome'].max()
charts_type = ["Stacked Bar Chart", "Histogram"]
# List of Job Roles
job_role_list = list(hr_data['JobRole'].unique())
# List of Departments
dept_list = ["Overall"] + list(hr_data['Department'].unique())
# List of Education
edu_list = list(hr_data['Education'].unique())
# List of JobInvolvement
job_inv_list = list(hr_data['JobInvolvement'].unique())

st.set_page_config(layout="wide")

#
# Sidebar
#
st.sidebar.title("Dashboard - IBM HR")
#st.sidebar.markdown('###')
#st.sidebar.markdown("### *Factors*")

#start_dist, end_dist = st.slider(
#    "Commuting Distance",
#    min_value=min_dist, max_value=max_dist,
#    value=(min_dist, max_dist))

#job_role = st.sidebar.multiselect('Job Role', job_role_list, default=job_role_list)
dept = st.sidebar.selectbox('Department', dept_list, index=0)
# edu = st.sidebar.multiselect('Education', edu_list, default=edu_list)
#job_inv = st.sidebar.multiselect('Job Involvement', job_inv_list, default=job_inv_list)

#st.markdown('###')
# chartType = st.sidebar.selectbox('Chart Type', charts_type, index=0)
itemQF = st.sidebar.selectbox('Quantative Factor', list_q_factors, index=0)
itemNF = st.sidebar.selectbox('Nominal Factor', list_n_factors, index=0)
# itemY = st.sidebar.selectbox('Factor 2', list_factors, index=1)

if dept=="Overall":
    hr_source = hr_data[hr_data['Department'].isin(dept_list)]
else:
    hr_source = hr_data[hr_data["Department"]==dept]

# Content
base = alt.Chart(hr_source).properties(height=300)

#bar = base.mark_bar().encode(
#    x=alt.X('count(Origin):Q', title='Number of Records'),
#    y=alt.Y('Origin:N', title='Origin'),
#    color=alt.Color('Origin:N', legend=None)
#)

ht_factor_q = base.mark_bar().encode(
    x=alt.X(itemQF+":Q", bin=True, title='Binned Values'),
    y=alt.Y('count()', title='Employee Counts'),
    color=alt.Color('Attrition',  legend=None),
    tooltip='JobRole'
).interactive().properties(width=300, height=300)

ht_factor_n = base.mark_bar(size=20).encode(
    x=alt.X(itemNF, title=None, axis=alt.Axis(tickMinStep=1)),
    y=alt.Y('count()', title='Employee Counts'),
    color=alt.Color('Attrition', legend=None),
    #                legend=alt.Legend(orient='bottom')),
    tooltip='JobRole'
).interactive().properties(width=300, height=300)

# Layout (Content)
left_column, right_column = st.columns([2, 1])

#left_column.markdown(
#    '**Number of Records (' + str(start_year) + '-' + str(end_year) + ')**')
#left_column.altair_chart(ht_age_dists, use_container_width=True)
left_column.markdown('**Workforce Attrition Distribution by Job Role**')
left_column.altair_chart(job_role_status_count_chart, use_container_width=True)

right_column.markdown('**Quan: _' + itemQF + '_**')
right_column.altair_chart(ht_factor_q, use_container_width=True)


#left_right_column = st.columns(2)

left_column.markdown('**Correlation Matrix (Lower Triangular)**')
left_column.altair_chart(correlations_chart, use_container_width=True)

right_column.markdown('**Nominal: _' + itemNF + '_**')
right_column.altair_chart(ht_factor_n, use_container_width=True)
