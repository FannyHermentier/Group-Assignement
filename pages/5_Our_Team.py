import streamlit as st
from PIL import Image

def load_image(image_path):
    image = Image.open(image_path)
    # Crop the image to make it square
    width, height = image.size
    new_size = min(width, height)
    left = max((width - new_size) // 2, 0)
    top = max((height - new_size) // 2, 0)
    right = min((width + new_size) // 2, width)
    bottom = min((height + new_size) // 2, height)
    image = image.crop((left, top, right, bottom))
    return image

def create_team_member_section(name, image_path, linkedin_url):
    with st.container():
        # Display image
        image = load_image(image_path)
        st.image(image, width=250, use_column_width=False, output_format='PNG')
        # Display name and LinkedIn link
        st.markdown(f"<h3 style='text-align: center'>{name}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center'><a href='{linkedin_url}'>LinkedIn</a></p>", unsafe_allow_html=True)

# Page configuration
st.set_page_config(page_title="Our Team", layout="wide")

# Title for the team page
st.title('Meet Our Team')

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stImage > img {
        border-radius: 50%;  /* Circular images */
        border: 4px solid #ddd;  /* Border around images */
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);  /* Shadow effect */
    }
    h3 {
        color: #4CAF50;  /* Text color for names */
    }
    a {
        color: #F63366;  /* Text color for LinkedIn links */
        font-weight: bold;
    }
    /* New style for sidebar background */
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.markdown(
    """
    ### About Us
    <div style="background-color: #d9ead3; padding: 10px; border-radius: 10px;">
    We are five students from IE University who developed this app as part of our coursework in the Masters in Big Data & Business Analytics program. This project was created for our Machine Learning class, showcasing our skills and dedication to applying advanced technologies in practical scenarios.
    </div>
    """,
    unsafe_allow_html=True
)

# Team members info - images, names, LinkedIn URLs
team_members = [
    {"name": "Fanny", "image": "Fanny.jpg", "linkedin": "https://www.linkedin.com/in/fanny-hermentier/"},
    {"name": "Jonathan", "image": "Jonathan.jpeg", "linkedin": "https://www.linkedin.com/in/jonathanschmidtr/"},
    {"name": "Pamela", "image": "Pamela.jpeg", "linkedin": "https://www.linkedin.com/in/pamelafawaz/"},
    {"name": "Ignacio", "image": "Ignacio.jpeg", "linkedin": "https://www.linkedin.com/in/ignacio-gdpa/"},
    {"name": "Marcos", "image": "Marcos.jpeg", "linkedin": "https://www.linkedin.com/in/marcosray/"}
]

# Display team members
# First row
cols = st.columns(3)
for i in range(3):
    with cols[i]:
        member = team_members[i]
        create_team_member_section(member["name"], member["image"], member["linkedin"])

# Second row (centered)
if len(team_members) > 3:
    cols = st.columns([1, 1, 1])
    for j in range(3, len(team_members)):
        with cols[j - 3]:
            member = team_members[j]
            create_team_member_section(member["name"], member["image"], member["linkedin"])

# Footer
st.markdown("---")
st.markdown(
    "© 2023 Medical Advice App by IE University students."
)