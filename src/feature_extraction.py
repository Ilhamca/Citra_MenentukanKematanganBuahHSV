import cv2
import numpy as np
from io import BytesIO
from PIL import Image


def load_image_from_upload(uploaded_file):
    """
    Load image from Streamlit file uploader.
    
    Parameters:
    - uploaded_file: Streamlit UploadedFile object
    
    Returns:
    - image: NumPy array in BGR format
    """
    # Read the uploaded file
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return image


def extract_hsv_features(image):
    """
    Extract HSV color space features from image.
    
    Parameters:
    - image: Input image in BGR format (OpenCV default)
    
    Returns:
    - hsv_features: Dictionary containing mean and std of H, S, V channels
    """
    # Convert to HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate mean and standard deviation for each channel
    h_mean = np.mean(hsv_image[:, :, 0])
    s_mean = np.mean(hsv_image[:, :, 1])
    v_mean = np.mean(hsv_image[:, :, 2])
    
    h_std = np.std(hsv_image[:, :, 0])
    s_std = np.std(hsv_image[:, :, 1])
    v_std = np.std(hsv_image[:, :, 2])
    
    hsv_features = {
        'hue_mean': h_mean,
        'saturation_mean': s_mean,
        'value_mean': v_mean,
        'hue_std': h_std,
        'saturation_std': s_std,
        'value_std': v_std
    }
    
    return hsv_features


def determine_ripeness(hsv_features, fruit_type='generic'):
    """
    Determine fruit ripeness level based on HSV features using rule-based thresholds.
    
    Parameters:
    - hsv_features: Dictionary containing HSV statistics
    - fruit_type: Type of fruit (default: 'generic', can be 'banana', 'mango', 'tomato', etc.)
    
    Returns:
    - ripeness_info: Dictionary containing ripeness level, percentage, and description
    """
    hue = hsv_features['hue_mean']
    saturation = hsv_features['saturation_mean']
    value = hsv_features['value_mean']
    
    # Generic fruit ripeness rules based on HSV
    # Green (unripe): Hue ~60-80, High saturation
    # Yellow-Orange (ripe): Hue ~15-45, Medium-High saturation
    # Brown-Red (overripe): Hue ~0-15 or high, Low saturation or very high
    
    if fruit_type == 'banana':
        # Banana specific thresholds
        if hue > 70 and saturation > 100:  # Green
            level = "Mentah"
            percentage = 20
            description = "Buah masih sangat mentah (hijau)"
        elif 50 < hue <= 70 and saturation > 80:  # Green-yellow
            level = "Belum Matang"
            percentage = 40
            description = "Buah belum matang (hijau kekuningan)"
        elif 25 < hue <= 50 and saturation > 60:  # Yellow
            level = "Matang"
            percentage = 80
            description = "Buah matang sempurna (kuning)"
        elif hue <= 25 and saturation > 40:  # Yellow-brown
            level = "Sangat Matang"
            percentage = 95
            description = "Buah sangat matang (kuning kecoklatan)"
        else:  # Brown spots
            level = "Terlalu Matang"
            percentage = 100
            description = "Buah terlalu matang (bintik coklat)"
            
    elif fruit_type == 'mango':
        # Mango specific thresholds
        if hue > 60 and saturation > 80:  # Green
            level = "Mentah"
            percentage = 25
            description = "Mangga masih mentah (hijau)"
        elif 40 < hue <= 60 and saturation > 70:  # Green-yellow
            level = "Belum Matang"
            percentage = 50
            description = "Mangga belum matang"
        elif 20 < hue <= 40 and saturation > 60:  # Yellow-orange
            level = "Matang"
            percentage = 85
            description = "Mangga matang (kuning kemerahan)"
        else:  # Very orange/red
            level = "Sangat Matang"
            percentage = 100
            description = "Mangga sangat matang"
            
    elif fruit_type == 'tomato':
        # Tomato specific thresholds
        if hue > 50 and saturation > 80:  # Green
            level = "Mentah"
            percentage = 20
            description = "Tomat mentah (hijau)"
        elif 30 < hue <= 50:  # Yellow-orange
            level = "Belum Matang"
            percentage = 50
            description = "Tomat belum matang (kekuningan)"
        elif 10 < hue <= 30 and saturation > 100:  # Orange-red
            level = "Matang"
            percentage = 85
            description = "Tomat matang (merah)"
        elif hue <= 10 and saturation > 80:  # Deep red
            level = "Sangat Matang"
            percentage = 95
            description = "Tomat sangat matang (merah tua)"
        else:
            level = "Terlalu Matang"
            percentage = 100
            description = "Tomat terlalu matang"
            
    else:  # Generic fruit
        if hue > 60 and saturation > 90:  # Green
            level = "Mentah"
            percentage = 25
            description = "Buah masih mentah (hijau)"
        elif 40 < hue <= 60 and saturation > 70:
            level = "Belum Matang"
            percentage = 50
            description = "Buah belum matang"
        elif 20 < hue <= 40 and saturation > 60:
            level = "Matang"
            percentage = 80
            description = "Buah matang"
        elif hue <= 20 and saturation > 50:
            level = "Sangat Matang"
            percentage = 95
            description = "Buah sangat matang"
        else:
            level = "Terlalu Matang"
            percentage = 100
            description = "Buah terlalu matang"
    
    ripeness_info = {
        'level': level,
        'percentage': percentage,
        'description': description,
        'hue': round(hue, 2),
        'saturation': round(saturation, 2),
        'value': round(value, 2)
    }
    
    return ripeness_info


def analyze_fruit_ripeness(uploaded_file, fruit_type='generic'):
    """
    Complete pipeline to analyze fruit ripeness from uploaded image.
    
    Parameters:
    - uploaded_file: Streamlit UploadedFile object
    - fruit_type: Type of fruit to analyze
    
    Returns:
    - results: Dictionary containing image, features, and ripeness information
    """
    # Load image
    image = load_image_from_upload(uploaded_file)
    
    # Extract HSV features
    hsv_features = extract_hsv_features(image)
    
    # Determine ripeness
    ripeness_info = determine_ripeness(hsv_features, fruit_type)
    
    # Convert image to RGB for display
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = {
        'image': image_rgb,
        'hsv_features': hsv_features,
        'ripeness': ripeness_info
    }
    
    return results


def create_hsv_visualization(image):
    """
    Create visualization of HSV channels.
    
    Parameters:
    - image: Input image in BGR format
    
    Returns:
    - hsv_channels: Dictionary with H, S, V channel images
    """
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    h_channel = hsv_image[:, :, 0]
    s_channel = hsv_image[:, :, 1]
    v_channel = hsv_image[:, :, 2]
    
    # Convert to RGB for display
    h_display = cv2.applyColorMap(h_channel, cv2.COLORMAP_HSV)
    s_display = cv2.cvtColor(s_channel, cv2.COLOR_GRAY2RGB)
    v_display = cv2.cvtColor(v_channel, cv2.COLOR_GRAY2RGB)
    
    hsv_channels = {
        'hue': cv2.cvtColor(h_display, cv2.COLOR_BGR2RGB),
        'saturation': s_display,
        'value': v_display
    }
    
    return hsv_channels
