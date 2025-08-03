import re

import jinja2

from core.config import settings


def _get_template_env() -> jinja2.environment.Environment:
    """
    Get template environment.

    Returns:
        jinja2.environment.Environment: jinja2 environment object.
    """
    if not getattr(_get_template_env, 'template_env', None):
        template_loader = jinja2.FileSystemLoader(searchpath=settings.templates_dir)
        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )
        _get_template_env.template_env = env

    return _get_template_env.template_env


def render_template(template_name: str, data: dict | None = None) -> str:
    """
    Render telegram message use jinja2.

    Args:
        template_name (str): jinja2 template name.
        data (dict | None): jinja2 template context.
    """
    if data is None:
        data: dict = {}
    template = _get_template_env().get_template(template_name)
    rendered = template.render(**data).replace('\n', ' ')
    rendered = rendered.replace('<br>', '\n')
    rendered = re.sub(' +', ' ', rendered).replace(' .', '.').replace(' ,', ',')
    rendered = '\n'.join(line.strip() for line in rendered.split('\n'))
    rendered = rendered.replace('{FOURPACES}', '    ')
    return rendered
