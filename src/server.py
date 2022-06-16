import tempfile
from arguments import ConversionArguments
from converter_manager import ConvertingMethod
from pathlib import Path
import argument_processer
from flask import Flask, request, send_file, redirect
import zipfile
import os

app = Flask(__name__)


@app.route("/<path:path>")
def get_static_resource(path):
    return app.send_static_file(path)


@app.route("/")
def main():
    return redirect('/index.html')


@app.route("/convert", methods=["POST"])
def convert():
    got = request.files.getlist('file')
    temps = []
    for i in range(len(got)):
        temps.append(tempfile.NamedTemporaryFile(suffix='.docx'))
        got[i].save(temps[-1])
    args = ConversionArguments(list(map(Path, [q.name for q in temps])), None, ConvertingMethod.UNOSERVER)
    argument_processer.process_arguments(args)
    if len(temps) == 1:
        return send_file(temps[0].name[:-5] + '.pdf', as_attachment=True, download_name=got[0].filename[:-5] + '.pdf')
    archive = tempfile.NamedTemporaryFile(suffix=".zip")
    with zipfile.ZipFile(archive.name, 'w') as arch:
        for i in range(len(got)):
            arch.write(temps[i].name[:-5] + '.pdf', os.path.basename(got[i].filename[:-5] + '.pdf'))
    return send_file(archive.name, as_attachment=True, download_name='documents.zip')
    #TODO: remove pdf files after sending them


if __name__ == "__main__":
    app.run()
