import os
import fitz  # PyMuPDF
from tkinter import Tk, filedialog
import google.generativeai as genai

# Set the environment variable for Google Cloud credentials
genai.configure(api_key="AIzaSyCFlTt82_LZYl4eDupTm3FaBb_fJRH_35g")

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-exp-0801",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])


def select_pdf():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF", filetypes=[("PDF Files", "*.pdf")]
    )
    return file_path


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text


def main():
    pdf_file = select_pdf()
    if pdf_file:
        text = extract_text_from_pdf(pdf_file)
        print(text)
        
        prompt = f"""
        based on these reports of this patient recommend a doctor and provide output in a good format. only provide whats requested nothing else:
        {text}

        Follow these rules to recommend a doctor:
        1. Age-Based Recommendations:
        • If Age < 15: Recommend a Pediatrician or complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        • If Age is between 15 and 60: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        • If Age > 60: Recommend Geriatric Medicine or complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        2. Gender-Based Modifications:
        • If Gender is Male: Follow age-based recommendations.
        • If Gender is Female: Add complete obstetrician-gynecologist to the age-based recommendations.
        3. Hemoglobin Level-Based Modifications:
        • If Gender is Male:
        - If Hemoglobin < 13 or > 17: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist (excluding complete obstetrician-gynecologist).
        • If Gender is Female:
        - If Hemoglobin < 10 or > 15: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + complete obstetrician-gynecologist.
        4. Total Leukocyte Count (TLC) Modifications:
        • If TLC > 11000 or < 4000:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + complete obstetrician-gynecologist + Oncologist.
        5. Neutrophil Count Modifications:
        • If Neutrophil > 100:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist + complete obstetrician-gynecologist + Special Cancer Marker Test.
        • If Neutrophil < 40:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist + complete obstetrician-gynecologist.
        6. Lymphocyte Count Modifications:
        • If Lymphocytes > 40:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist + complete obstetrician-gynecologist + Special Cancer Marker Test.
        • If Lymphocytes < 20:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist + complete obstetrician-gynecologist.
        7. Basophil Count Modifications:
        • If Basophil > 1:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist.
        • If Basophil < 0: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        8. Monocyte Count Modifications:
        • If Monocytes > 10:
        - If Gender is Male: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist.
        - If Gender is Female: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Oncologist + Endocrinologist + complete obstetrician-gynecologist + Special Cancer Marker Test.
        • If Monocytes < 2: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist.
        9. MCV, MCH, MCHC, and MPV Modifications:
        • For Female:
        - MCV > 101 or < 83
        - MCH > 32 or < 27
        - MCHC > 34.5 or < 31.5
        - MPV > 9 or < 6
        Recommend complete obstetrician-gynecologist + complete General Physician, Internal Medicine, Nutritionist, Hematologist + Outer Test Suggestion + Iron Level + Urine Marker + LFT, KFT, TSH, T3, T4, Vit B12.
        • For Male:
        - MCV > 101 or < 83
        - MCH > 32 or < 27
        - MCHC > 34.5 or < 31.5
        - MPV > 9 or < 6
        Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Diabetologist + Endocrinologist + Cardiologist.
        10. RBC Count Modifications:
        • For Male:
        - If RBC > 4.8 or < 3.8: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + Endocrinologist.
        • For Female:
        - If RBC > 4.8 or < 3.8: Recommend complete General Physician, Internal Medicine, Nutritionist, Hematologist + complete obstetrician-gynecologist.
        11. RDW-CV Modifications:
        • If RDW-CV > 14:
        - For Female: Recommend Endocrinologist + complete obstetrician-gynecologist + complete General Physician, Internal Medicine, Nutritionist, Hematologist + Pathologist for further tests (Bone Marrow Biopsy) + Nephrologist.
        - For Male: Recommend Endocrinologist + complete General Physician, Internal Medicine, Nutritionist, Hematologist + Pathologist for further tests (Bone Marrow Biopsy) + Nephrologist.

        Output Format:
        here is an example output format:
        Recommended Doctor(s):

        Complete General Physician
        Internal Medicine Specialist
        Nutritionist
        Hematologist
        Cardiologist

        Explanation:

        This patient is a 23-year-old male. Based on the provided blood report, several values are outside the typical range:

        MCH (Mean Corpuscular Hemoglobin): High (36.40 pg)
        MCHC (Mean Corpuscular Hemoglobin Concentration): High (39.06 g/dL)
        RDW-CV (Red Cell Distribution Width): High (16.0 %)
        MPV (Mean Platelet Volume): High (9.8 fL)

        These values, particularly the elevated MCH, MCHC, and RDW-CV, can indicate conditions such as macrocytic anemia. The high MPV suggests larger platelets, which can be associated with various health issues.

        Therefore, the recommendations include specialists who can address these potential concerns:

        Complete General Physician: Provides overall assessment and coordination of care.
        Internal Medicine Specialist: Diagnoses and manages complex medical conditions.
        Nutritionist: Addresses potential dietary factors contributing to the blood abnormalities.
        Hematologist: Specializes in blood disorders and will investigate the cause of the abnormal blood counts.
        Cardiologist:  Recommended due to potential link between high RDW-CV and cardiovascular risk.

        This combination of specialists will ensure a thorough evaluation and appropriate management plan for the patient.
        """

        response = chat_session.send_message(prompt)
        print(response.text.strip())
    else:
        print("No PDF selected.")


if __name__ == "__main__":
    main()
