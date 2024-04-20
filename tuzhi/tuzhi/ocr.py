from pathlib import Path

from flask import Blueprint, redirect, render_template, url_for, current_app
from werkzeug.utils import secure_filename

from tuzhi.forms import FileForm

bp = Blueprint("ocr", __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()

    if form.validate_on_submit():
        print('Uploading file...')
        f = form.pdf.data
        filename = secure_filename(f.filename)
        print(f'Saving file {filename}')
        f.save(Path(current_app.instance_path) / filename)
        return redirect(url_for('ocr.uploaded'))

    return render_template('index.html', form=form)


@bp.route('/uploaded', methods=['GET', 'POST'])
def uploaded():
    return 'Upload success'
