import tokenize


class CouldNotHandleEncoding(Exception):
    def __init__(self, path, cause):
        super().__init__(message=path)
        self.path = path
        self.cause = cause


def read_py_file(filepath):
    # see https://docs.python.org/3/library/tokenize.html#tokenize.detect_encoding
    # first just see if the file is properly encoded
    try:
        with open(filepath, "rb") as pyfile:
            tokenize.detect_encoding(pyfile.readline)
    except SyntaxError as err:
        # this warning is issued:
        #   (1) in badly authored files (contains non-utf8 in a comment line)
        #   (2) a coding is specified, but wrong and
        #   (3) no coding is specified, and the default
        #       'utf-8' fails to decode.
        #   (4) the encoding specified by a pep263 declaration did not match
        #       with the encoding detected by inspecting the BOM
        raise CouldNotHandleEncoding(filepath, err) from err

    try:
        with tokenize.open(filepath) as pyfile:
            return pyfile.read()
        # this warning is issued:
        #   (1) if utf-8 is specified, but latin1 is used with something like \x0e9 appearing
        #       (see http://stackoverflow.com/a/5552623)
    except UnicodeDecodeError as err:
        raise CouldNotHandleEncoding(filepath, err) from err
