from subprocess import PIPE, Popen


def pdftotext(filename: str) -> str:
    """Convert a PDF file to a text equivalent.

    Args:
      filename: A string path, the filename to convert.
    Returns:
      A string, the text contents of the filename.
    """
    executable = ['pdftotext', '-layout', filename, '-']
    pipe = Popen(executable, stdout=PIPE, stderr=PIPE)
    stdout, stderr = pipe.communicate()
    if stderr:
        raise ValueError(stderr.decode('utf-8'))
    else:
        return stdout.decode()
