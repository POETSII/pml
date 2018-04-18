import jinja2
import os

def load_text(file):
    with open(file, "r") as fid:
        return fid.read()


def get_path(file, parent_file):
    """
    Return the absolute path of 'file', assuming a workdir where 'parent_file'
    is located.
    """
    parent_dir = os.path.split(parent_file)[0]
    return os.path.join(parent_dir, file)


def generate_xml(template, graph, content=dict()):
    """Generate xml string from xml template and graph object.

    'template' can either be a filename or a template string."""

    is_file = os.path.isfile(template)

    template_str = load_text(template) if is_file else template
    template_dir = os.path.split(template)[0] if is_file else '.'

    # Create jinja template content

    content = join_dicts({"graph": graph}, content)

    # Define custom jinja function 'include'

    def include_file(file, **kwargs):
        """Include file in jinja template."""

        # Determine absolute path of included file
        full_file = get_path(file, template) if is_file else file

        # Create 'inner_content', a copy of 'content' merged with the named
        # arguments of 'include'.
        inner_content = join_dicts(content, kwargs)

        # Generate result (recursively) using generate_xml
        return generate_xml(full_file, graph, inner_content)

    # Prepare jinja environment

    loader = jinja2.PackageLoader(__name__, '')
    env = jinja2.Environment(loader=loader)
    env.globals['include'] = include_file

    # Return rendered template
    return env.get_template(template).render(**content)


def join_dicts(*dicts):
    """Return a sum of dictionaries."""

    result = dicts[0]

    for d in dicts[1:]:
        result = dict(result, **d)

    return result