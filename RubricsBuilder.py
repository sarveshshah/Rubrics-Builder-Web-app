import pandas as pd
import numpy as np
import streamlit as st 

# Create an exportable Rubric List
@st.cache(allow_output_mutation=True)
def get_data():
    return []

def get_trait():
    # Trait
    selected_trait = left_column.selectbox(
        'Select a Trait',
        list_of_traits)

    # Max points out of 10
    max_points = right_column.selectbox('Select Maximum Point Value',
    np.arange(10,1,-1)
    )

    return selected_trait, max_points

def export_data(to_be_exported):
    export = []
    for data in to_be_exported:
        trait = data['Trait']
        point = data['Max Points']
        
        temp = df.loc[df['Trait']==trait,:]
        with np.errstate(invalid='ignore'):
            for column, multiplier in rubric_dict.items():
                temp.loc[:,column] = round(max_points*multiplier,2)                
        export.append(temp)
    rubrics = pd.concat(export)

    st.table(rubrics)
    rubrics.to_excel('Rubrics.xlsx',sheet_name='Rubrics',index=False, header=True)

st.write("""
# Rubrics Builder for CMA
""")

# FAQ Code
# expander = st.beta_expander("Click on + for FAQ")
# expander.write("""
# A simple to use Rubrics Builder. Select a trait of your choice and add it to the list.
# """)

# Read the existing Traits, can be further changed
df = pd.read_excel("Rubric Builder 2.5.xlsx", sheet_name="RAW Data")
list_of_traits = df['Trait'].unique()

# Control Panel 
# Setting up two columns
left_column, right_column = st.beta_columns(2)

selected_trait, max_points = get_trait()
rubrics = df.loc[df['Trait']==selected_trait]

# Rubric List dict, to be replaced with a json/config file
rubric_dict = {
    "Exemplary": 1,
    "Proficient": 0.93,
    "Developing": 0.86,
    "Limited": 0.79
}

# Add new columns
with np.errstate(invalid='ignore'):
    for column, multiplier in rubric_dict.items():
        rubrics.loc[:,column] = round(max_points*multiplier,2)

# Show the DataFrame
"""### Trait Description"""

st.dataframe(rubrics.iloc[:,1:5].T)
st.dataframe(rubrics.iloc[:,5:].T)

first_column, second_column, third_column = st.beta_columns(3)

with first_column:
    add = st.button("Add this to list")
    if add:
        get_data().append({"Trait":selected_trait,
        "Max Points": max_points})
        st.text('Added to the list')
    
    show = st.checkbox("Show List")
    if show:
        st.table(pd.DataFrame(get_data()))

with second_column:
    clear = st.button("Clear List")
    if clear:
        from streamlit import caching
        caching.clear_cache()

with third_column:
    export = st.button("Export Rubrics")

if export:
    export_data(get_data())
