import streamlit as st


def on_file_upload():
    if st.session_state.picture_uploader is not None:
        st.session_state.picture = st.session_state.picture_uploader

def on_file_delete():
    st.session_state.picture = None
    
def upload_image():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        upload_container = st.container()
        with upload_container:
            st.markdown("<h1 style='text-align: center;'>Picture Uploader</h1>", unsafe_allow_html=True)
            if st.session_state.picture is None:
                st.session_state.picture = st.file_uploader("Upload a picture", type=["png", "jpg", "jpeg"], key="picture_uploader", on_change=on_file_upload, label_visibility="hidden", accept_multiple_files=False)
            else:
                st.image(st.session_state.picture, width=512, use_container_width=False)
                btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                with btn_col2:
                    if st.button("Delete Picture", type="primary", key="delete_button", on_click=on_file_delete):
                        pass
    

def main():
    st.set_page_config(page_title="Test", layout="wide")
    
    # Sidebar
    menu = st.sidebar.selectbox(
    "Menu Navigasi",
    ["Upload dan Filter","Clustering (K-Means)", "Pembobotan Kriteria (AHP)", 
     "Perankingan (SAW)", "Hasil Rekomendasi"]
    )
    
    # Var setup
    if 'picture' not in st.session_state:
        st.session_state.picture = None

    uploadContainer = st.container()
    with uploadContainer:
        if menu == "Upload dan Filter":
            upload_image()

                    
            
        
            
    
            
            

if __name__ == "__main__":
    main()
    