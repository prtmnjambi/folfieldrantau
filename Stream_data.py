import pickle
import streamlit as st
import pygame  # Untuk memutar file MP3
import threading  # Untuk menjalankan suara tanpa mengganggu Streamlit

# Load the model
try:
    with open('Pred_rtu.sav', 'rb') as file:
        LokasiKM = pickle.load(file)
except Exception as e:
    st.error(f"Error loading the model: {e}")
    LokasiKM = None  # Assign None if there's an error loading the model

# Fungsi untuk memainkan MP3 di thread terpisah menggunakan pygame
def play_alarm():
    def play_sound():
        pygame.mixer.init()
        pygame.mixer.music.load("buzzer.mp3")  # Ganti dengan file MP3 kamu
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue  # Tunggu sampai suara selesai diputar
    threading.Thread(target=play_sound, daemon=True).start()

# Web Title with style
st.markdown(
    "<h1 style='text-align: center; color: #FF5733;'>PERTAMINA FIELD RANTAUGG</h1>",
    unsafe_allow_html=True,
)

# Input Section Header
st.markdown(
    "<h3 style='text-align: center; color: #33A1FF;'>Input Delta Pressure di Titik 1-9 (PSI)</h3>",
    unsafe_allow_html=True,
)

# Create a 3x3 grid for inputs
cols = st.columns(3)

Titik_1_PSI = cols[0].text_input('Titik 1 (PSI)', value="")
Titik_2_PSI = cols[1].text_input('Titik 2 (PSI)', value="")
Titik_3_PSI = cols[2].text_input('Titik 3 (PSI)', value="")
Titik_4_PSI = cols[0].text_input('Titik 4 (PSI)', value="")
Titik_5_PSI = cols[1].text_input('Titik 5 (PSI)', value="")
Titik_6_PSI = cols[2].text_input('Titik 6 (PSI)', value="")
Titik_7_PSI = cols[0].text_input('Titik 7 (PSI)', value="")
Titik_8_PSI = cols[1].text_input('Titik 8 (PSI)', value="")
Titik_9_PSI = cols[2].text_input('Titik 9 (PSI)', value="")

# Add CSS for custom button styling
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #33A1FF;
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

suspect_loct = ''

# Prediction Button with centered alignment
if LokasiKM is not None:
    if st.button("Prediksi Lokasi"):
        try:
            # Ensure all inputs are valid numbers
            inputs = [
                float(Titik_1_PSI), float(Titik_2_PSI), float(Titik_3_PSI),
                float(Titik_4_PSI), float(Titik_5_PSI), float(Titik_6_PSI),
                float(Titik_7_PSI), float(Titik_8_PSI), float(Titik_9_PSI)
            ]

            # Predict the location
            prediksi_lokasi = LokasiKM.predict([inputs])
            hasil_prediksi = prediksi_lokasi[0]

            # Build result text
            lines = []
            for i, val in enumerate(hasil_prediksi, start=1):
                if val > 0 and val < 63:
                    # Bunyi alarm
                    play_alarm()
                    lines.append(f"<span style='color: red;'>Titik {i}: KM {val:.2f}</span>")
                else:
                    lines.append(f"<span style='color: green;'>Titik {i}: Tidak Terdapat Kebocoran</span>")

            # Combine results
            suspect_loct = "<h4>Suspect Lokasi:</h4><br>" + "<br>".join(lines)

            # Display result with styles
            st.markdown(suspect_loct, unsafe_allow_html=True)

        except ValueError:
            st.error("Pastikan semua input adalah angka valid.")
        except Exception as e:
            st.error(f"Error predicting location: {e}")
