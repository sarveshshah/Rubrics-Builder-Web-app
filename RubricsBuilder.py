import pandas as pd
import numpy as np
import streamlit as st 
import json
import base64

from PIL import Image
im = Image.open('files/Fox Logo.jpg')
print(im.width,im.height)

def header():
    left_column_head, center_column_head, right_column_head = st.beta_columns(3)

    with left_column_head:
        st.image(im, use_column_width=True)

    with center_column_head:
        st.write()

    with right_column_head:
        st.write()
        
    st.markdown("""
        # Rubrics Builder 
        by [Curriculum Management & Assessment](https://www.fox.temple.edu/analytics-and-accreditation/curriculum-management-assessment/),
        Fox School of Business, Temple University
    """)

    # FAQ Code  
    expander = st.beta_expander("How to use")
    expander.write("""

    In order to fully experience this app, navigate to hamburger menu in top right -> Settings -> Check 'Show app in wide mode'

    ### **Selection Guide**  
        1. Select the graduate/undergradute level  
        2. Select a trait of your choice      
        3. Select Maximum Points  
        4. Select if you want rubric point ranges (default = Yes)   

    ### **Other Controls**  
        1. The trait descriptions and points will be visible in the tables below  
        2. If you're satisfied with the selection, add it to the list by clicking the option below  
        3. You can always clear the list if you want to start from scratch  
        4. Once you're happy with the selection, click the Export button  
        5. Click the link to download your rubrics  

    **Make sure to clear the list before using it, to clear out any previous selection**

    Feel free to share any feedback at ``sarvesh.shah@temple.edu``

""")


# Create an exportable Rubric List
@st.cache(allow_output_mutation=True)
def get_data():
    return []

def read_traits():
    s = open(r'files/trait_points.txt', 'r').read()
    trait_points = json.loads(s)

    rubric_dict_grad = trait_points['rubric_dict_grad']
    rubric_dict_ugrad = trait_points['rubric_dict_ugrad']
    rubric_dict_grad_range = trait_points['rubric_dict_grad_range']
    rubric_dict_ugrad_range = trait_points['rubric_dict_ugrad_range']

    return rubric_dict_grad, rubric_dict_ugrad, rubric_dict_grad_range, rubric_dict_ugrad_range

def get_trait():
    
    # Graduate
    grad_level = left_column.selectbox("Enter Grad Level", options = ['Graduate','Undergraduate'])

    # Trait
    selected_trait = first_column.selectbox('Select a Trait', list_of_traits)

    # Max points out of 10
    max_points = last_column.selectbox('Select Maximum Points', np.arange(100,1,-1))

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

        if grad_level == 'Undergraduate' and range_opt == 'Yes':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_ugrad_range.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

        if grad_level == 'Graduate' and range_opt == 'No':
            with np.errstate(invalid='ignore'):
                for column, multiplier in rubric_dict_grad.items():
                    temp.loc[:,column] = round(point*multiplier,2)                
            export.append(temp)

        if grad_level == 'Undergraduate' and range_opt == 'No':
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
    st.markdown("### Built by")
    left, right = st.beta_columns(2)

    left.markdown("""
                > [Matthew Kunkle, PhD](https://www.fox.temple.edu/about-fox/directory/matthew-kunkle/)  
                > Fox School of Business  
                > Senior Associate Director  
                > Analytics and Accreditation
            """)

    right.markdown("""
                > [Sarvesh Shah, MSBA](https://www.sarvesh-shah.com/)  
                > Fox School of Business  
                > Data Scientist  
                > SEPTA
            """)

    st.markdown("""
        **Note**:  
        This app is purely for demonstration purposes only.  
        The traits, rubrics available in the app are intellectual property of Fox School of Business, Temple University.  
        Feel free to contribute to this project on GitHub.
    
    """)


header()

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

    if grad_level == 'Undergraduate' and range_opt == 'Yes':
        for column, multiplier in rubric_dict_ugrad_range.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)

    if grad_level == 'Undergraduate' and range_opt == 'No':
        for column, multiplier in rubric_dict_ugrad.items():
            rubrics.loc[:,column] = round(max_points*multiplier,2)

# Show the DataFrame
st.markdown("""## Trait Description""")

st.table((rubrics.set_index('Trait')).iloc[:,0:5])
st.dataframe(rubrics.iloc[:,5:].T)

first_column, second_column, third_column = st.beta_columns(3)

with first_column:
    add = st.button("Add this to list")
    if add:
        get_data().append({"Trait":selected_trait,
        "Max Points": max_points})
        st.text('Added to the list')
    try:
        st.table(pd.DataFrame(get_data()).set_index('Trait'))
    except:
        pass

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
