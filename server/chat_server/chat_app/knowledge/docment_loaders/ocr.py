from rapidocr_onnxruntime import RapidOCR


def get_ocr() -> "RapidOCR":
    """使用cpu"""
    from rapidocr_onnxruntime import RapidOCR

    ocr = RapidOCR()

    return ocr
