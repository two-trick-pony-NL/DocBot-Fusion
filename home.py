import streamlit as st
#from components.logo import logo_component
from components.sidebar import sidebar_component
st.set_page_config(
    page_title=" DocBot Fusion", 
    layout="wide",
    page_icon='💬',
    initial_sidebar_state='expanded',
    menu_items={
        'Report a bug': "https://github.com/two-trick-pony-NL/DocBot-Fusion/issues",
        'About': "https://petervandoorn.com"
    })



sidebar_component()


from PIL import Image

image = Image.open('images/logo.png')
example = Image.open('images/example.png')


#st.image(image)

st.markdown(
    """
    # If ChatGPT really knew you, what would it say? 😏
    Well you're about to find out. With Docbot Fusion you fuse ChatGPT with **your** files so that it knows what's going on in your life.""")

# Place buttons in the columns
st.markdown('<a href="/chat" target="_self">Start Chat 💬 </a>', unsafe_allow_html=True)
st.markdown('<a href="/files" target="_self">Upload files 🗂️ </a>', unsafe_allow_html=True)

st.markdown("""
    ## How does that work? Simple:
    - 📤 just upload some files like your calendar 📆 and preferences of your family 👨‍👩‍👧
    
    - 💬 Start chatting
    - 🤓 Get personalsid responses
    
"""
)

st.markdown(
    """
     ## Upload your first file

    """
)
#Adding file upload
uploaded_file = st.file_uploader("", type=['pdf', 'txt'])
# Save uploaded files to disk
if uploaded_file is not None:
    # Use the original filename
    file_name = str(uploaded_file.name)
    file_path = os.path.join(data_folder, file_name)

    # Save the file to disk
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getvalue())

    st.success(f"File '{file_name}' uploaded successfully!")

st.markdown(
    """
     ## Example chat

    """
)

st.image(example)




st.markdown(
    """
    ### Open source
    If you're curious how this tool works, then you can. The code is [here](https://github.com/two-trick-pony-NL/DocBot-Fusion)
"""
)



