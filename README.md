# Medical Text NER & Keyword Matcher

A powerful web application for medical text analysis using Named Entity Recognition (NER) and keyword matching. Built with Flask and spaCy, this tool can extract medical entities from text, URLs, and PDF documents.

## 🚀 Features

- **Multiple Input Methods**: Manual text input, URL extraction, and PDF upload
- **Advanced NLP Processing**: Named Entity Recognition using spaCy
- **Custom Medical Patterns**: Keyword matching with custom medical patterns
- **Web Interface**: Modern, responsive web interface
- **Real-time Analysis**: Fast text processing and entity extraction
- **Multiple Entity Sources**: Combines NER and pattern matching results

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **NLP**: spaCy
- **Text Extraction**: BeautifulSoup, PyMuPDF
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Render

## 📋 Prerequisites

- Python 3.8+
- spaCy trained model
- All dependencies listed in `requirements.txt`

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-nlp-app.git
   cd medical-nlp-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your spaCy model**
   - Place your trained spaCy model in the project directory
   - Update the model path in the web interface

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5000`

## 📁 Project Structure

```
medical-nlp-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── templates/
│   └── index.html        # Web interface template
├── uploads/              # Temporary file storage
└── README.md            # Project documentation
```

## 🎯 Usage

### 1. Load Model
- Enter your spaCy model directory path
- Click "Load Model" to initialize the NLP pipeline

### 2. Input Text
Choose from three input methods:
- **Manual Text**: Type or paste text directly
- **Website URL**: Extract text from any webpage
- **PDF Upload**: Upload and process PDF documents

### 3. Analyze
- Click "Analyze Text" to process the input
- View extracted entities in a formatted table
- Results show entity text, label, source (NER/Matcher), and position

## 🔍 Supported Entity Types

The application can identify various medical entities including:
- Medical conditions
- Medications
- Procedures
- Anatomical terms
- Symptoms
- And more (depends on your trained model)

## 🌐 Live Demo

**Deployed on Render**: [(https://medical-text-ner-keyword-matcher.onrender.com)]

## 🚀 Deployment

### Deploy to Render

1. **Fork this repository**

2. **Create a Render account** at [render.com](https://render.com)

3. **Create a new Web Service**
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Your app will be deployed automatically

4. **Configure your model**
   - Update the model path for your deployment environment
   - Consider using cloud storage for large models

### Deploy to Other Platforms

- **Heroku**: Use `Procfile` with `web: gunicorn app:app`
- **Google Cloud Run**: Containerize with Docker
- **AWS Lambda**: Use Zappa or similar framework

## ⚙️ Configuration

### Environment Variables

- `SECRET_KEY`: Flask secret key (auto-generated on Render)
- `PORT`: Application port (set by hosting platform)

### Model Configuration

For deployment, you have several options:

1. **Include model in repository** (for smaller models)
2. **Use cloud storage** (Google Drive, S3, etc.)
3. **Download model during build** process
4. **Use pre-trained spaCy models**

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application interface |
| `/load_model` | POST | Load spaCy model and patterns |
| `/extract_url` | POST | Extract text from URL |
| `/upload_pdf` | POST | Process uploaded PDF file |
| `/analyze` | POST | Analyze text and extract entities |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/alamgirkabir9/)

## 🙏 Acknowledgments

- spaCy team for the excellent NLP library
- Flask community for the web framework
- Contributors and testers

## 📞 Support

If you have any questions or issues:

1. Check the [Issues](https://github.com/yourusername/medical-nlp-app/issues) page
2. Create a new issue if your problem isn't already listed
3. Contact:alomgirkabir720@gmail.com

## 🔄 Updates

- **v1.0.0** - Initial release with basic NER functionality
- **v1.1.0** - Added PDF upload support
- **v1.2.0** - Improved UI and deployment configuration

## 🔒 Security

- File uploads are limited to 16MB
- Only PDF files are accepted for upload
- Uploaded files are automatically deleted after processing
- Input sanitization for web scraping

## 📈 Performance

- Optimized for small to medium-sized documents
- Concurrent request handling with Flask
- Memory-efficient text processing
- Responsive web interface

---

**⭐ Star this repository if you find it helpful!**
