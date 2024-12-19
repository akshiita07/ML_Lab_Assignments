from flask import Flask, request, render_template
from google_images_download import google_images_download
import os

app = Flask(__name__)

# Function to download images
def download_images(keyword, limit):
    response = google_images_download.googleimagesdownload()
    arguments = {"keywords": keyword, "limit": limit, "print_urls": True, "output_directory": "downloads", "image_directory": keyword}
    paths = response.download(arguments)
    return paths

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # Get form data
    keyword = request.form['keyword']
    limit = int(request.form['limit'])
    
    # Call the download function
    download_images(keyword, limit)
    
    return f"Downloaded {limit} images for keyword: {keyword}. Check the 'downloads' folder."

if __name__ == '__main__':
    # Create downloads folder if it doesn't exist
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)
