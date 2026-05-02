import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

# पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="Interactive Physics Lab", layout="wide")

# CSS से स्टाइलिंग (Dark/Light mode support)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔬 Virtual Refraction Lab 2.0")
st.write("विभिन्न माध्यमों में प्रकाश के व्यवहार को समझने के लिए नीचे दिए गए विकल्पों का उपयोग करें।")

# साइडबार - इंटरएक्टिव कंट्रोल्स
st.sidebar.header("🛠️ Lab Settings")

# मटेरियल प्रीसेट्स (Presets)
materials = {
    "Air (हवा)": 1.0,
    "Water (पानी)": 1.33,
    "Glass (कांच)": 1.5,
    "Glycerin": 1.47,
    "Diamond (हीरा)": 2.42
}

st.sidebar.subheader("Medium 1 (Upper)")
m1_choice = st.sidebar.selectbox("Select Material 1", list(materials.keys()), index=0)
n1 = st.sidebar.number_input("Custom n1", value=materials[m1_choice])

st.sidebar.subheader("Medium 2 (Lower)")
m2_choice = st.sidebar.selectbox("Select Material 2", list(materials.keys()), index=2)
n2 = st.sidebar.number_input("Custom n2", value=materials[m2_choice])

st.sidebar.markdown("---")
angle_i_deg = st.sidebar.slider("Incident Angle (i°)", 0.0, 89.0, 45.0)
speed = st.sidebar.select_slider("Animation Speed", options=["Slow", "Normal", "Fast"], value="Normal")

# कैलकुलेशन
angle_i_rad = np.radians(angle_i_deg)
sin_r = (n1 * np.sin(angle_i_rad)) / n2

# मुख्य लेआउट
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Real-time Data")
    
    # कूल मेट्रिक्स
    st.metric("Relative Refractive Index (n21)", round(n2/n1, 2))
    
    if n1 > n2:
        c_angle = np.degrees(np.arcsin(n2/n1))
        st.warning(f"Critical Angle: {c_angle:.2f}°")
        if angle_i_deg > c_angle:
            st.error("Status: Total Internal Reflection")
        else:
            st.info("Status: Refraction")
    else:
        st.info("Status: Refraction (Rare to Dense)")

    # लॉजिक को स्पष्ट करने के लिए टेक्स्ट
    if sin_r <= 1.0:
        angle_r_deg = np.degrees(np.arcsin(sin_r))
        deviation = abs(angle_i_deg - angle_r_deg)
        st.write(f"किरण अभिलंब से {deviation:.1f}° विचलित हुई है।")

with col2:
    plot_spot = st.empty()
    
    # एनीमेशन टाइमिंग
    sleep_time = {"Slow": 0.1, "Normal": 0.05, "Fast": 0.01}[speed]

    for f in np.linspace(0.1, 1.0, 20):
        fig, ax = plt.subplots(figsize=(7, 7))
        
        # बैकग्राउंड कलरिंग (माध्यमों को अलग दिखाने के लिए)
        ax.fill_between([-2, 2], 0, 2, color='#e3f2fd', alpha=0.3, label=m1_choice)
        ax.fill_between([-2, 2], -2, 0, color='#fff3e0', alpha=0.3, label=m2_choice)
        
        ax.axhline(0, color='black', lw=2)
        ax.axvline(0, color='gray', linestyle='--')
        
        # Incident Ray
        ax.annotate('', xy=(0, 0), xytext=(-np.tan(angle_i_rad)*f, f),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=2))
        
        if sin_r <= 1.0:
            angle_r_rad = np.arcsin(sin_r)
            # Refracted Ray
            ax.annotate('', xy=(np.tan(angle_r_rad)*f, -f), xytext=(0, 0),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))
            ax.text(0.2, -0.5, f"r = {np.degrees(angle_r_rad):.1f}°", color='red')
        else:
            # TIR Ray
            ax.annotate('', xy=(np.tan(angle_i_rad)*f, f), xytext=(0, 0),
                        arrowprops=dict(arrowstyle='->', color='green', lw=2))
            st.toast("Total Internal Reflection Detected!", icon="⚠️")

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(f"Simulation: {m1_choice} ➔ {m2_choice}")
        ax.set_aspect('equal')
        
        plot_spot.pyplot(fig)
        plt.close(fig)
        time.sleep(sleep_time)