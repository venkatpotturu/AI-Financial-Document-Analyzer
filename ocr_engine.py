# ocr_engine.py
import pytesseract
from PIL import Image, ImageEnhance, ImageOps
import fitz  # PyMuPDF
import io
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Windows users: Set this path to your Tesseract installation
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    """Optimize image for OCR reading"""
    try:
        # Convert to grayscale
        image = image.convert('L')
        
        # Enhance image quality
        image = ImageEnhance.Contrast(image).enhance(2.0)
        image = ImageEnhance.Sharpness(image).enhance(2.0)
        image = image.resize((image.width*2, image.height*2), Image.Resampling.LANCZOS)
        
        return image
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        return image

def extract_text_from_image(file):
    """Extract text from image files"""
    try:
        img = Image.open(io.BytesIO(file.read()))
        img = preprocess_image(img)
        text = pytesseract.image_to_string(img, config='--psm 6')
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
        return ""

def extract_text_from_pdf(file):
    """Extract text from PDF files"""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = [page.get_text().strip() for page in doc]
        return "\n\n".join(text)
    except Exception as e:
        logger.error(f"PDF error: {str(e)}")
        return ""

def get_text_from_file(file):
    """Main function to handle all file types"""
    try:
        file.seek(0)
        ext = file.name.lower().split('.')[-1]
        
        if ext == 'pdf':
            return extract_text_from_pdf(file)
        elif ext in ['png', 'jpg', 'jpeg']:
            return extract_text_from_image(file)
        else:
            return "Unsupported file type"
    except Exception as e:
        logger.error(f"File error: {str(e)}")
        return ""