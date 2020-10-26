import pandas as pd
import numpy as np
import streamlit as st 
import json
import base64

# TODO: Figure out a way to scale logo
# from PIL import Image
# im = Image.open('Fox Logo.jpg')
# print(im.width,im.height)
# image = im.resize(size=(int(im.width/7),int(im.height/7)))

# Create an exportable Rubric List
@st.cache(allow_output_mutation=True)
def get_data():
    return []

def read_traits():
    s = open(r'files/trait_points.txt', 'r').read()
    trait_points = json.loads(s)
    print(trait_points.keys())

    rubric_dict_grad = trait_points['rubric_dict_grad']
    rubric_dict_ugrad = trait_points['rubric_dict_ugrad']
    rubric_dict_grad_range = trait_points['rubric_dict_grad_range']
    rubric_dict_ugrad_range = trait_points['rubric_dict_ugrad_range']

    return rubric_dict_grad, rubric_dict_ugrad, rubric_dict_grad_range, rubric_dict_ugrad_range

def get_trait():
    
    # Graduate
    grad_level = left_column.selectbox("Enter Grad Level", options = ['Graduate','Under Graduate'])

    # Trait
    selected_trait = first_column.selectbox('Select a Trait', list_of_traits)

    # Max points out of 10
    max_points = last_column.selectbox('Select Maximum Point Value', np.arange(100,1,-1))

    # Range option
    range_opt = right_column.selectbox("Range", options = ['Yes','No'])

    return selected_trait, max_points, grad_level, range_opt

def export_data(to_be_exported, grad_level, range_opt):
    export = []
    for data in to_be_exported:
        trait = data['Trait']
        point = data['Max Points']
        
        temp = df.loc[df['Trait']==trait,:]

        if grad_level == 'Graduate' and range_opt == 'Yes':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_grad_range.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

        if grad_level == 'Under Graduate' and range_opt == 'Yes':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_ugrad_range.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

        if grad_level == 'Graduate' and range_opt == 'No':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_grad.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

        if grad_level == 'Under Graduate' and range_opt == 'No':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_ugrad.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

    rubrics = pd.concat(export)

    # st.table(rubrics)
    csv = rubrics.to_csv(index=False, header=True)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}" download="Rubrics.csv">Download csv file</a>'
    st.markdown(href, unsafe_allow_html = True)

def footer():
    st.markdown("Built by")
    left, right = st.beta_columns(2)

    left.markdown("""
                Matthew Kunkle  
                Fox School of Business  
                PhD Fall 20
            """)

    right.markdown("""
                Sarvesh Shah  
                Fox School of Business  
                MSBA Fall 19
            """)


# st.image(im, use_column_width=True)
st.write("""
# Rubrics Builder for CMA
""")

# FAQ Code
# expander = st.beta_expander("Click on + for FAQ")
# expander.write("""
# A simple to use Rubrics Builder. Select a trait of your choice and add it to the list.
# """)

# Read the existing Traits, can be further changed
df = pd.read_csv(r"files/traits.csv",sep=",", encoding='cp1252')
list_of_traits = df['Trait'].unique()

# Control Panel 
# Setting up two columns
left_column, first_column, last_column, right_column = st.beta_columns(4)

selected_trait, max_points, grad_level, range_opt = get_trait()
rubrics = df.loc[df['Trait']==selected_trait]

rubric_dict_grad, rubric_dict_ugrad, rubric_dict_grad_range, rubric_dict_ugrad_range = read_traits()

# Add new columns
with np.errstate(invalid='ignore'):
    if grad_level == 'Graduate' and range_opt == 'Yes':
        for column, multiplier in rubric_dict_grad_range.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)

    if grad_level == 'Graduate' and range_opt == 'No':
        for column, multiplier in rubric_dict_grad.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)    

    if grad_level == 'Under Graduate' and range_opt == 'Yes':
        for column, multiplier in rubric_dict_ugrad_range.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)

    if grad_level == 'Under Graduate' and range_opt == 'No':
        for column, multiplier in rubric_dict_ugrad.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)

# Show the DataFrame
st.markdown("""## Trait Description""")

st.dataframe(rubrics.iloc[:,1:5].T)
st.dataframe(rubrics.iloc[:,5:].T)

first_column, second_column, third_column = st.beta_columns(3)

with first_column:
    add = st.button("Add this to list")
    if add:
        get_data().append({"Trait":selected_trait,
        "Max Points": max_points})
        st.text('Added to the list')
    
    st.table(pd.DataFrame(get_data()))

with second_column:
    clear = st.button("Clear List")
    if clear:
        from streamlit import caching
        caching.clear_cache()

with third_column:
    export = st.button("Export Rubrics")

if export:
    export_data(get_data(), grad_level, range_opt)

footer()
