from pathlib import Path

from jinja2 import (
    Environment,
    PackageLoader,
    select_autoescape,
)

bootstrap_ctx = {
    'version': '5.3.2',
}

template_data = {
    'icon.html': {
        'baseUrl': '/static/favicons',
        'sizes': [180, 152, 120, 76],
    },
    "styles.html": bootstrap_ctx,
    "scripts.html": bootstrap_ctx
}


def render(out_dir: str = 'tuzhi/templates/generated'):
    # Creates a template environment with a loader that looks up templates in the templates folder
    # inside `static_templ` Python package or next to `static_templ` python module.
    env = Environment(
        loader=PackageLoader('static_templ'),
        autoescape=select_autoescape(),
    )

    dest_dir = Path(out_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    for name, ctx in template_data.items():
        template = env.get_template(name)
        htmlStr = template.render(ctx)
        with (dest_dir / name).open(mode='w', encoding='utf-8') as f:
            f.write(htmlStr)


if __name__ == '__main__':
    render()
