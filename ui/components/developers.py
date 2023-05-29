import streamlit
from PIL import Image

def developersDashboard():
    cols = streamlit.columns(5)

    with cols[0]:
        streamlit.subheader("Suyash Chavan")
        streamlit.write("2019BTECS00041")
        image = Image.open('./assets/images/suyash.jpg')
        streamlit.image(image)

    with cols[1]:
        streamlit.subheader("Om Khairnar")
        streamlit.write("2019BTECS00078")
        image = Image.open('./assets/images/om.jpg')
        streamlit.image(image)

    with cols[2]:
        streamlit.subheader("Prof. M. K. Chavan")
        streamlit.write("Project Guide")
        image = Image.open('./assets/images/mkc.enc')
        streamlit.image(image)

    with cols[3]:
        streamlit.subheader("Yash Pandhare")
        streamlit.write("2019BTECS00085")
        image = Image.open('./assets/images/yash.jpg')
        streamlit.image(image)

    with cols[4]:
        streamlit.subheader("Pratik Raut")
        streamlit.write("2019BTECS00050")
        image = Image.open('./assets/images/pratik.jpeg')
        streamlit.image(image)