import streamlit as st
import requests
import base64
import os

st.set_page_config(layout="wide")

def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

image_path = os.path.expanduser("neo/app/galaxy.jpg")
base64_image = get_base64_image(image_path)

# CSS code for custom styling
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

# Input page
def input_page():
    st.markdown('<div class="header">NEO</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Near Earth Objects</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    st.header("Input Hazardous Object Details")

    absolute_magnitude = st.number_input("Enter Absolute Magnitude:", min_value=0.0, format="%.2f")
    estimated_diameter_min = st.number_input("Enter Estimated Minimum Diameter (Kilometers):", min_value=0.0, format="%.2f")
    relative_velocity = st.number_input("Enter Relative Velocity (Km/h):", min_value=0.0, format="%.2f")
    miss_distance = st.number_input("Enter Miss Distance (Kilometers):", min_value=0.0, format="%.2f")

    if st.button("Predict"):
        # Prepare the payload to send to FastAPI
        payload = {
            "absolute_magnitude": absolute_magnitude,
            "estimated_diameter_min": estimated_diameter_min,
            "relative_velocity": relative_velocity,
            "miss_distance": miss_distance
        }

        # Send the request to the FastAPI server
        try:
            response = requests.get("http://127.0.0.1:8000/prediction", params=payload)
            response_data = response.json()
            pred = None

            # Display the prediction result
            if response.status_code == 200:
                if response_data['prediction']:
                    pred='Hazardous'
                    st.error(f"Prediction: {pred}")
                else:
                    pred='Non-Hazardous'
                    st.success(f"Prediction: {pred}")
            else:
                st.error("Error: Could not fetch prediction. Please check the inputs or try again later.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    if st.button("Back to Home"):
        st.session_state.page = "Home"
    st.markdown('</div>', unsafe_allow_html=True)

# Main page
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

    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("Assess Risk!"):
        st.session_state.page = "Input Data"
    st.markdown('</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
if 'page' not in st.session_state:
    st.session_state.page = "Home"

if st.session_state.page == "Home":
    main_page()
else:
    input_page()
