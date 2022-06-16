import tempfile
from arguments import ConversionArguments
from converter_manager import ConvertingMethod
from pathlib import Path
import argument_processer
from flask import Flask, request, send_file, redirect

app = Flask(__name__)


@app.route("/<path:path>")
def get_static_resource(path):
    return app.send_static_file(path)


@app.route("/")
def main():
    return redirect('/index.html')


@app.route("/convert", methods=["POST"])
def convert():
    got = request.files['file']
    tmp = tempfile.NamedTemporaryFile(suffix='.docx')
    got.save(tmp)
    args = ConversionArguments([Path(tmp.name)], None, ConvertingMethod.UNOSERVER)
    print(tmp.name, args.input_paths, args.output_folder)
    argument_processer.process_arguments(args)
    filename = tmp.name[:-5] + '.pdf'
    return send_file(filename, as_attachment=True, download_name=got.filename[:-5] + '.pdf')


if __name__ == "__main__":
    app.run()
