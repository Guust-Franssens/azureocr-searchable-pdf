import os
from argparse import ArgumentParser
from pathlib import Path

import pymupdf
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def main(input_file: str, output_file: str) -> None:
    """
    Reads in the input file, sends it to Azure OCR for processing and saves in the output_file location
    """
    pdf = pymupdf.open(input_file)
    bytes = open(input_file, "rb").read()

    poller = di_client.begin_analyze_document(model_id="prebuilt-read", document=bytes)
    result = poller.result()

    fontname = "helv"
    font = pymupdf.Font(fontname)
    for pdf_page, ocr_page in zip(pdf, result.pages):
        # Calculate scaling factors
        scale_x = pdf_page.rect.width / ocr_page.width
        scale_y = pdf_page.rect.height / ocr_page.height

        for word in ocr_page.words:
            # ocr results are in relative coordinates, convert to absolute
            points = [pymupdf.Point(point.x * scale_x, point.y * scale_y) for point in word.polygon]
            # Create a rectangle from the transformed points
            bbox_mupdf = pymupdf.Rect(points[0], points[2])

            # Font selection and text length calculation
            tl = font.text_length(word.content, fontsize=1)
            fontsize = bbox_mupdf.width / tl

            # use descender insertion point, or use standard (check with your own pdf what works best)
            insertion_point = bbox_mupdf.bl + (0, font.descender * fontsize)
            # insertion_point = bbox_mupdf.bl

            pdf_page.insert_text(
                point=insertion_point,
                text=word.content,
                fontsize=fontsize,
                fontname=fontname,
                render_mode=3,  # Visible text for debugging, set to 3 for invisible
            )

    pdf.save(output_file)


if __name__ == "__main__":
    load_dotenv()
    parser = ArgumentParser()
    parser.add_argument("input_file", type=str, help="Input PDF file name")
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=False,
        default="",
        help="Output PDF file name. Default: input_file + .ocr.pdf",
    )
    args = parser.parse_args()
    input_file = Path(args.input_file)
    output_file = args.output_file or input_file.parent / f"{input_file.stem}.ocr.pdf"
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_URL"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    di_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    main(str(input_file), str(output_file))
