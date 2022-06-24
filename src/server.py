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
    return redirect('/index.html')


@app.route("/convert", methods=["POST"])
def convert():
    got = request.files.getlist('file')
    if len(got) == 1 and got[0].filename == "":
        abort(make_response("No files were sent to the server", 400))
    temps = []
    for i in range(len(got)):
        print(got[i].filename)
        if not got[i].filename.endswith(".docx"):
            abort(make_response("File with the wrong extension was sent to the server: %s" % got[i].filename, 400))
        temps.append(tempfile.NamedTemporaryFile(suffix='.docx'))
        got[i].save(temps[-1])
    args = ConversionArguments(list(map(Path, [q.name for q in temps])), None, ConvertingMethod.UNOSERVER)
    argument_processer.process_arguments(args)
    if len(temps) == 1:
        if os.path.exists(temps[0].name[:-5] + '.pdf'):
            temp_base = temps[0].name[:-5]
            original_base = got[0].filename[:-5]
            return send_file(temp_base + '.pdf', as_attachment=True, download_name=original_base + '.pdf')
        else:
            abort(make_response("The file you sent was corrupt", 400))
    archive = tempfile.NamedTemporaryFile(suffix=".zip")
    with zipfile.ZipFile(archive.name, 'w') as arch:
        for i in range(len(got)):
            if os.path.exists(temps[i].name[:-5] + '.pdf'):
                arch.write(temps[i].name[:-5] + '.pdf', os.path.basename(got[i].filename[:-5] + '.pdf'))
            else:
                abort(make_response("Corrupted file was sent to the server: %s" % got[i], 400))
    return send_file(archive.name, as_attachment=True, download_name='documents.zip')
    # TODO: remove pdf files after sending them
    # returning the error string should be enough to recover, the temporary files will be deleted.


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
