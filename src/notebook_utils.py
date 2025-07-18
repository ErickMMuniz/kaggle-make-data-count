import os


DATA : str = os.path.abspath(os.path.join(os.getcwd(), os.pardir, "data"))
TRAIN : str = os.path.abspath(os.path.join(DATA, "train"))
TEST : str = os.path.abspath(os.path.join(DATA, "test"))

PDF_TRAIN = os.path.abspath(os.path.join(TRAIN, "PDF"))
XML_TRAIN = os.path.abspath(os.path.join(TRAIN, "XML"))

PDF_TEST = os.path.abspath(os.path.join(TEST, "PDF"))
XML_TEST = os.path.abspath(os.path.join(TEST, "XML"))
