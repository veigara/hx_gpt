import logging
from rapidocr_onnxruntime import RapidOCR


logger = logging.getLogger("chat_app")


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    try:
        from rapidocr_paddle import RapidOCR
    except ImportError:
        from rapidocr_onnxruntime import RapidOCR


def get_ocr(use_cuda: bool = True) -> "RapidOCR":
    try:
        from rapidocr_paddle import RapidOCR

        ocr = RapidOCR(
            det_use_cuda=use_cuda, cls_use_cuda=use_cuda, rec_use_cuda=use_cuda
        )
    except ImportError:
        from rapidocr_onnxruntime import RapidOCR

        ocr = RapidOCR()
    return ocr


if __name__ == "__main__":
    # ocr = get_ocr()
    # image_path = "E:/idea_workspace/pythonProject/hx_gpt/img/1.png"
    # result, elapse_list = ocr(image_path)
    # print(result)
    # print(elapse_list)
    import paddle

    print(paddle.utils.run_check())
