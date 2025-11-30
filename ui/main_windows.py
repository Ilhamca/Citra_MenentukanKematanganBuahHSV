import streamlit as st
import src.preprocessing as preprocessing
import src.feature_extraction as feature_extraction

def on_file_upload():
    if st.session_state.picture_uploader is not None:
        st.session_state.picture = st.session_state.picture_uploader
        # Reset analysis when new image is uploaded
        st.session_state.analyzed = False
        st.session_state.analysis_results = None

def on_file_delete():
    st.session_state.picture = None
    st.session_state.analyzed = False
    st.session_state.analysis_results = None
    
def upload_image():
    upload_container = st.container(width="stretch")
    with upload_container:
        st.write("<h1 style='text-align: center;'>Menentukan Kematangan Buah</h1>", unsafe_allow_html=True)
        st.file_uploader("Upload a picture", type=["png", "jpg", "jpeg"], key="picture_uploader", on_change=on_file_upload, label_visibility="hidden", accept_multiple_files=False)
    
def edit_gambar():
    st.subheader("Pengaturan Analisis")
    
    # Fruit type selection
    st.selectbox(
        "Jenis Buah",
        options=['generic', 'banana', 'mango', 'tomato'],
        format_func=lambda x: {
            'generic': 'Generic (Umum)',
            'banana': 'Pisang',
            'mango': 'Mangga',
            'tomato': 'Tomat'
        }[x],
        key="fruit_type",
        help="Pilih jenis buah untuk analisis yang lebih akurat"
    )
    
    st.divider()
    
    # Display analysis results if available
    if st.session_state.get('analyzed', False):
        results = st.session_state.analysis_results
        ripeness = results['ripeness']
        
        st.subheader("Hasil Analisis")
        
        # Display ripeness level with color coding
        if ripeness['percentage'] < 40:
            color = "🟢"
        elif ripeness['percentage'] < 70:
            color = "🟡"
        else:
            color = "🔴"
        
        st.markdown(f"### {color} {ripeness['level']}")
        st.progress(ripeness['percentage'] / 100)
        st.caption(f"Tingkat Kematangan: {ripeness['percentage']}%")
        
        st.write(ripeness['description'])
        
        # Display HSV values
        with st.expander("Detail Nilai HSV"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Hue (H)", f"{ripeness['hue']:.1f}")
            with col2:
                st.metric("Saturation (S)", f"{ripeness['saturation']:.1f}")
            with col3:
                st.metric("Value (V)", f"{ripeness['value']:.1f}")
                    
def analyze_image():
    """Analyze fruit ripeness and store results in session state."""
    if st.session_state.picture is not None:
        # Get fruit type selection
        fruit_type = st.session_state.get('fruit_type', 'generic')
        
        # Analyze fruit ripeness
        results = feature_extraction.analyze_fruit_ripeness(
            st.session_state.picture, 
            fruit_type=fruit_type
        )
        
        # Store results in session state
        st.session_state.analysis_results = results
        st.session_state.analyzed = True

def preprocess_image(image):
    hue = st.session_state.hue_slider
    saturation = st.session_state.saturation_slider
    brightness = st.session_state.brightness_slider
    
    adjusted_image = preprocessing.adjust_hsv(image, hue, saturation, brightness)
    st.session_state.preview_image = adjusted_image

def main():
    st.set_page_config(page_title="Test", layout="wide")
    
    # Var setup
    if 'picture' not in st.session_state:
        st.session_state.picture = None
    if 'preview_image' not in st.session_state:
        st.session_state.preview_image = None
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'fruit_type' not in st.session_state:
        st.session_state.fruit_type = 'generic'

    uploadContainer = st.container()
    with uploadContainer:
        upload_image()
        if st.session_state.picture is not None:
            image_col1, image_col2 = st.columns([3, 2], gap="medium")
            with image_col1:
                # Show preview if available, otherwise show original
                display_image = st.session_state.preview_image if st.session_state.preview_image is not None else st.session_state.picture
                st.image(display_image, caption="Image Preview", use_container_width=True)
                
                if st.button("Analisa Buah", type="secondary", key="analyze_button"):
                    analyze_image()
                    
            with image_col2:
                edit_gambar()
  

if __name__ == "__main__":
    main()
    