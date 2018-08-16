import subprocess

def prettify_xml(xml):
    """Prettify XML using xmllint.

    Fails safely by returning the unformatted XML input if xmllint is not
    installed.
    """

    try:
        cmd = ['xmllint', '--format', '-']
        pipe = subprocess.PIPE
        proc = subprocess.Popen(cmd, stdout=pipe, stdin=pipe,stderr=pipe)
        output, err = proc.communicate(input=xml)
    except OSError:
        return xml

    if proc.returncode is not 0:
        print err
        raise Exception("xmllint returned non-zero exit code")

    return output
