import re
from typing import Any

import jinja2

from config import TEMPLATES_DIR


def _get_template_env() -> jinja2.Environment:
    """Get template environment."""
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATES_DIR)
    env = jinja2.Environment(
        loader=template_loader,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )
    return env


def render_template(template_name: str, data: dict[str, Any]) -> str:
    """Render telegram message use jinja2."""
    template = _get_template_env().get_template(template_name)
    rendered = template.render(**data).replace('\n', ' ')
    rendered = rendered.replace('<br>', '\n')
    rendered = re.sub(' +', ' ', rendered).replace(' .', '.').replace(' ,', ',')
    rendered = '\n'.join(line.strip() for line in rendered.split('\n'))
    rendered = rendered.replace('{FOURPACES}', '    ')
    return rendered
