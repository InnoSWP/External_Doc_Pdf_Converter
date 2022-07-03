import tempfile
from arguments import ConversionArguments
from converter_manager import ConvertingMethod
from pathlib import Path
import argument_processer
from flask import Flask, request, send_file, redirect, abort, make_response
import zipfile
import os

app = Flask(__name__)


@app.route("/<path:path>")
def get_static_resource(path):
    return app.send_static_file(path)


@app.route("/")
def main():
    return redirect("/docxToPdf.html")


@app.route("/convert", methods=["POST"])
def convert():
    td = tempfile.TemporaryDirectory()
    tmp_dir = td.name + "/"
    original_names = []
    converted_names = []
    got = request.files.getlist('file')
    if len(got) == 1 and got[0].filename == "" or len(got) == 0:
        abort(make_response("No files were sent to the server", 400))
    for i in range(len(got)):
        if not got[i].filename.endswith(".docx"):
            abort(make_response("File with the wrong extension was sent to the server: %s" % got[i].filename, 400))
        original_names.append(got[i].filename)
        converted_names.append(got[i].filename[:-5] + ".pdf")
    for i in range(len(got)):
        got[i].save(tmp_dir + original_names[i])
    args = ConversionArguments(list(map(Path, [tmp_dir + q for q in original_names])), None, ConvertingMethod.UNOSERVER)
    argument_processer.process_arguments(args)
    if len(got) == 1:
        f = tmp_dir + converted_names[i]
        if os.path.exists(f):
            return send_file(f, as_attachment=True, download_name=converted_names[0])
        else:
            abort(make_response("The file you sent was corrupt", 400))
    for i in range(len(got)):
        f = tmp_dir + converted_names[i]
        if not os.path.exists(f):
            abort(make_response("Corrupted file was sent to the server: " + f, 400))
    archive = tmp_dir + "documents.zip"
    with zipfile.ZipFile(archive, 'w') as arch:
        for i in range(len(got)):
            arch.write(tmp_dir + converted_names[i], converted_names[i])
    return send_file(archive, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
