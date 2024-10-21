import streamlit as st
import base64


st.set_page_config(layout="wide")
def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
image_path = "/home/raneem/code/KhalylDammas/neo-hazardous-classification/neo/app/galaxy.jpg"
base64_image = get_base64_image(image_path)

#css code
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .header {{
        font-size: 50px;
        font-weight: bold;
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF; 
        text-align: left;
        margin-bottom: 1px; 
    }}
    .sub-header {{
        font-size: 20px;
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF; 
        text-align: left;
        margin-bottom: 150px; 
    }}
    .custom-header {{
        font-size: 24px;
        font-weight: 500;
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF; 
        margin-left: 40px; 
        line-height: 1.5; 
    }}
    .button-container {{
        margin-left: 40px; 
        background-color: #7B1FA2;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

#input page
def input_page():
    st.markdown('<div class="header">NEO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Near Earth Objects</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.header("Input Hazardous Object Details")
    
    absolute_magnitude = st.number_input("Enter Absolute Magnitude:", min_value=0.0, format="%.2f")
    estimated_diameter_max = st.number_input("Enter Estimated Maximum Diameter (meters):", min_value=0.0, format="%.2f")
    relative_velocity = st.number_input("Enter Relative Velocity (km/h):", min_value=0.0, format="%.2f")
    miss_distance = st.number_input("Enter Miss Distance (kilometers):", min_value=0.0, format="%.2f")

    if st.button("Predict"):
        # Display the entered values
        st.write(f"Absolute Magnitude: {absolute_magnitude}")
        st.write(f"Estimated Maximum Diameter: {estimated_diameter_max} meters")
        st.write(f"Relative Velocity: {relative_velocity} km/h")
        st.write(f"Miss Distance: {miss_distance} kilometers")

    if st.button("Back to Home"):
        st.session_state.page = "Home"  
    st.markdown('</div>', unsafe_allow_html=True)

#main page
def main_page():
    st.markdown('<div class="header">NEO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Near Earth Objects</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="custom-header">
            Our advanced algorithms assess the threat<br>
            level of hazardous objects,<br>
            determining whether they pose a danger to Earth.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
    st.markdown('<div class="button-container">', unsafe_allow_html=True) #???????????????????
    if st.button("Assess Risk!"):
        st.session_state.page = "Input Data"  
    st.markdown('</div>', unsafe_allow_html=True)


st.sidebar.title("Navigation")
if 'page' not in st.session_state:
    st.session_state.page = "Home" 


if st.session_state.page == "Home":
    main_page()
else:
    input_page()










