from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:\\python_workspace\\MyCloudServer\\shareFile'

# 파일 업로드를 위한 경로
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'File {filename} uploaded successfully'

# 파일 다운로드를 위한 경로
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 파일 미리보기 기능 (이미지 파일에 대해서만)
@app.route('/preview/<filename>')
def preview_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return '<img src="{}">'.format(f'/download/{filename}')
    return 'File not supported for preview'

# 홈페이지
@app.route('/')
def index():
    return '''
    <!doctype html>
    <html>
    <head><title>My Cloud Server</title></head>
    <body>
    <h1>Welcome to My Cloud Server</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
