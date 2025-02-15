# app/ocr.py
import re
import torch
import pandas as pd
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
from utils.logger import setup_logger

class DonutOCR:
    def __init__(self, model_name="naver-clova-ix/donut-base-finetuned-cord-v2"):
        self.logger = setup_logger(self.__class__.__name__)
        self.logger.info("Inisialisasi DonutOCR...")
        try:
            self.processor = DonutProcessor.from_pretrained(model_name)
            self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            self.logger.info("Model berhasil diload pada %s", self.device)
        except Exception as e:
            self.logger.error("Gagal inisialisasi model: %s", str(e))
            raise e

    def process_image(self, image_file) -> dict:
        """
        Memproses file image dan mengembalikan hasil OCR dalam bentuk JSON.
        :param image_file: objek file (misal, stream file dari upload)
        :return: dict hasil ekstraksi OCR.
        """
        try:
            # Buka image menggunakan PIL
            image = Image.open(image_file).convert("RGB")
            self.logger.info("Gambar berhasil dibuka.")

            # Preprocessing gambar
            pixel_values = self.processor(image, return_tensors="pt").pixel_values

            # Siapkan decoder input ids dengan prompt task
            task_prompt = "<s_cord-v2>"
            decoder_input_ids = self.processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids

            # Generate output OCR
            self.logger.info("Sedang memproses OCR...")
            outputs = self.model.generate(
                pixel_values.to(self.device),
                decoder_input_ids=decoder_input_ids.to(self.device),
                max_length=self.model.decoder.config.max_position_embeddings,
                early_stopping=True,
                pad_token_id=self.processor.tokenizer.pad_token_id,
                eos_token_id=self.processor.tokenizer.eos_token_id,
                use_cache=True,
                num_beams=1,
                bad_words_ids=[[self.processor.tokenizer.unk_token_id]],
                return_dict_in_generate=True,
                output_scores=True,
            )

            # Decode hasil sequence
            sequence = self.processor.batch_decode(outputs.sequences)[0]
            sequence = sequence.replace(self.processor.tokenizer.eos_token, "").replace(self.processor.tokenizer.pad_token, "")
            sequence = re.sub(r"<.*?>", "", sequence, count=1).strip()
            self.logger.info("Proses OCR selesai.")

            # Konversi sequence ke JSON
            result = self.processor.token2json(sequence)
            
            return result
        except Exception as e:
            self.logger.error("Error saat memproses image: %s", str(e))
            return {"error": str(e)}
        
    def flatten_json(self, json_data, parent_key='', sep='_'):
        """
        Meratakan JSON bersarang menjadi format yang cocok untuk DataFrame.
        """
        flattened_dict = {}
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, (dict, list)):
                    flattened_dict.update(self.flatten_json(v, new_key, sep=sep))
                else:
                    flattened_dict[new_key] = v
        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                flattened_dict.update(self.flatten_json(item, f"{parent_key}{sep}{i}", sep=sep))
        return flattened_dict

    def process_image_to_dataframe(self, image_file):
        """
        Memproses gambar menjadi DataFrame untuk ditampilkan dalam tabel.
        """
        result_json = self.process_image(image_file)
        if "error" in result_json:
            return pd.DataFrame([{"Key": "Error", "Value": result_json["error"]}])  # Jika error, tampilkan sebagai tabel
        else:   
            flattened_data = self.flatten_json(result_json)
            df = pd.DataFrame(flattened_data.items(), columns=["Key", "Value"])
            
        return df.set_index("Key")