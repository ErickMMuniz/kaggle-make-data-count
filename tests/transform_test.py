def test_first_pdf_transform():
    from transform.pdf import extract_text_from_pdf

    pdf_file_path = "tests/fixtures/transform_test_pdf_to_text.pdf"
    text_file_path = "tests/fixtures/transform_test_pdf_to_text.txt"

    assert extract_text_from_pdf(pdf_file_path) == open(text_file_path, "r").read()
