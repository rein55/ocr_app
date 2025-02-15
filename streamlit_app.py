# streamlit_app.py
import streamlit as st
from app.ocr import DonutOCR
from utils.logger import setup_logger

def main():
    st.title("Donut OCR Application")
    st.write("Upload file gambar untuk ekstraksi OCR.")

    logger = setup_logger("Streamlit")
    # Inisialisasi OCR processor
    try:
        ocr_processor = DonutOCR()
    except Exception as e:
        st.error("Error saat inisialisasi model OCR.")
        logger.error("Gagal inisialisasi DonutOCR: %s", str(e))
        return

    uploaded_file = st.file_uploader("Pilih file gambar", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Gambar yang diupload", width=250)
        if st.button("Process"):
            logger.info("Memproses gambar yang diupload...")
            df_result = ocr_processor.process_image_to_dataframe(uploaded_file)

            # Tampilkan hasil dalam bentuk tabel di Streamlit
            st.write("Hasil OCR dalam bentuk tabel:")
            st.dataframe(df_result)


if __name__ == "__main__":
    main()
