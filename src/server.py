import tempfile
import unoserver.converter
import unoserver.server
from flask import Flask, request, send_file, redirect
import os

app = Flask(__name__)

server = unoserver.server.UnoServer()
converter = None


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
    res = tempfile.NamedTemporaryFile(suffix='.pdf')
    converter.convert(inpath=tmp.name, outpath=res.name, convert_to='pdf')
    filename = got.filename[:-5] + '.pdf'
    return send_file(res.name, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    server.start()
    converter = unoserver.converter.UnoConverter(server.interface, server.port)
    app.run()
