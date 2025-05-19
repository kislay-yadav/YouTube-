from flask import Flask, render_template, request, send_file, jsonify
import os
import uuid
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
COOKIE_FILE = "cookies.txt"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        unique_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestvideo+bestaudio/best',
            'quiet': True,
            'merge_output_format': 'mp4',
            'cookiefile': COOKIE_FILE,  # ⬅️ use uploaded cookies.txt
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = ydl.prepare_filename(info).replace('.webm', '.mp4')
            title = info.get('title', 'video')

        return jsonify({'filename': os.path.basename(downloaded_path), 'title': title})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get/<filename>')
def get_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
