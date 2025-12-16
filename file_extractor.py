# file_extractor.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image, ImageEnhance
import pandas as pd
import docx
import io
import logging
import warnings

# Suppress PIL decompression warnings
warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)

# Configure Tesseract path (Windows)
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except (FileNotFoundError, ImportError):
    pass  # Use default path for Linux/Mac

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR)

def enhance_image(image):
    """Preprocess image for better OCR results"""
    try:
        # Convert to grayscale
        image = image.convert('L')
        
        # Increase resolution
        image = image.resize((image.width*2, image.height*2), 
                          resample=Image.Resampling.BICUBIC)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Thresholding
        image = image.point(lambda x: 0 if x < 200 else 255)
        
        return image
    except Exception as e:
        logger.error(f"Image enhancement failed: {str(e)}")
        return image

def extract_text_from_image(file):
    """Extract text from images with advanced preprocessing"""
    try:
        # Read and enhance image
        image = Image.open(io.BytesIO(file.read()))
        enhanced_image = enhance_image(image)
        
        # OCR with optimized parameters
        text = pytesseract.image_to_string(
            enhanced_image,
            config='--psm 11 --oem 3 -c preserve_interword_spaces=1'
        )
        return text.strip()
    except Exception as e:
        logger.error(f"OCR failed: {str(e)}")
        return ""

def extract_text_from_pdf(file):
    """Extract text from PDF files"""
    try:
        text = []
        doc = fitz.open(stream=file.read(), filetype="pdf")
        for page in doc:
            text.append(page.get_text().strip())
        return "\n".join(text)
    except Exception as e:
        logger.error(f"PDF extraction error: {str(e)}")
        return ""

# Keep other extraction functions (docx, excel, etc) same as previous version

def get_text_from_file(file):
    """Main file processing function"""
    try:
        file.seek(0)
        content = file.read()
        file_like = io.BytesIO(content)
        
        if file.name.lower().endswith('.pdf'):
            return extract_text_from_pdf(file_like)
        elif file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            return extract_text_from_image(file_like)
        # Add other file type handling here
        else:
            return "Unsupported file type"
    except Exception as e:
        logger.error(f"File processing failed: {str(e)}")
        return ""