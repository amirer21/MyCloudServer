from flask import Flask, request, send_from_directory, render_template, redirect, url_for, Response
from werkzeug.utils import secure_filename
import os
import zipfile
from flask import redirect, url_for


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:\\python_workspace\\MyCloudServer\\shareFile'
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 제한 크기: 16MB

# 파일 업로드를 위한 경로 (여러 파일 처리)
@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('file')  # 여러 파일 받기
    if not files:
        return 'No files to upload'
    uploaded_files = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(filename)
    # 파일 업로드 완료 후 메인 페이지로 리디렉션
    return redirect(url_for('index'))


# 파일 다운로드를 위한 경로
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 갤러리 페이지
@app.route('/gallery')
def gallery():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('gallery.html', files=files)

# 여러 파일 다운로드
@app.route('/download-selected', methods=['POST'])
def download_selected_files():
    selected_files = request.form.getlist('files')
    if not selected_files:
        return 'No files selected for download'
    zip_filename = "selected_files.zip"
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zf:
        for filename in selected_files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            zf.write(file_path, filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], zip_filename, as_attachment=True)

# 홈페이지 (업로드 폼 수정)
@app.route('/')
def index():
    return '''
    <!-- Bootstrap CDN 추가 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- 홈페이지에 Bootstrap 클래스 적용 -->
    <!doctype html>
    <html>
    <head>
    <title>My Cloud Server</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <div class="container">
    <h1 class="mt-5 mb-3">Welcome to My Cloud Server</h1>
    <form action="/upload" method="post" enctype="multipart/form-data" class="mb-3">
        <input type="file" name="file" multiple class="form-control">
        <button type="submit" class="btn btn-primary mt-3">Upload</button>
    </form>
    <a href="/gallery" class="btn btn-info">View Gallery</a>
    </div>
    </body>
    </html>

    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

