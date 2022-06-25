import tempfile
from arguments import ConversionArguments
from converter_manager import ConvertingMethod
from pathlib import Path
import argument_processer
from flask import Flask, request, send_file, redirect, abort, make_response, after_this_request
import zipfile
import os

app = Flask(__name__)


@app.route("/<path:path>")
def get_static_resource(path):
    return app.send_static_file(path)


@app.route("/")
def main():
    return redirect('/index.html')

import pdb

@app.route("/convert", methods=["POST"])
def convert():
    td = tempfile.TemporaryDirectory()
    tmp_dir = td.name
    got = request.files.getlist('file')
    if len(got) == 1 and got[0].filename == "" or len(got) == 0:
        abort(make_response("No files were sent to the server", 400))
    for i in range(len(got)):
        if not got[i].filename.endswith(".docx"):
            abort(make_response("File with the wrong extension was sent to the server: %s" % got[i].filename, 400))
    for i in range(len(got)):
        got[i].save(tmp_dir + "/" + got[i].filename)
    args = ConversionArguments(list(map(Path, [tmp_dir + "/" + q.filename for q in got])), None, ConvertingMethod.UNOSERVER)
    argument_processer.process_arguments(args)
    result = None
    if len(got) == 1:
        if os.path.exists(tmp_dir + "/" + got[0].filename[:-5] + '.pdf'):
            base = tmp_dir + "/" + got[0].filename[:-5]
            return send_file(base + '.pdf', as_attachment=True, download_name=got[0].filename[:-5] + '.pdf')
        else:
            abort(make_response("The file you sent was corrupt", 400))
    for i in range(len(got)):
        if not os.path.exists(tmp_dir + '/' + got[0].filename[:-5] + '.pdf'):
            abort(make_response("Corrupted file was sent to the server: %s" % got[i], 400))
    archive = tmp_dir + "/documents.zip"
    with zipfile.ZipFile(archive, 'w') as arch:
        for i in range(len(got)):
            arch.write(tmp_dir + '/' + got[i].filename[:-5] + '.pdf', got[i].filename[:-5] + '.pdf')
    return send_file(archive, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
