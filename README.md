# GitHub Activity Analyzer

A powerful web application that analyzes and visualizes GitHub repository activity for GDGAAU projects. Built with FastAPI and Chart.js.

## 🌟 Features

- Real-time GitHub repository analytics
- Multiple repository comparison
- Interactive visualization dashboards
- Commit trend analysis
- Contributor statistics
- Rate limit handling
- Beautiful glass-morphism UI design

## Preview

![Project Preview](https://res.cloudinary.com/dgckkacgl/image/upload/v1741353266/photo_2025-03-07_16-14-06_tqobgt.jpg)

## 🚀 Live Demo

[Click Here](https://github-activity-tracker.onrender.com/)

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Frontend**: HTML, TailwindCSS, Chart.js
- **API**: GitHub REST API
- **Deployment**: Ready for Render, DigitalOcean, or Railway

## 📋 Prerequisites

- Python 3.8+
- GitHub Personal Access Token
- Modern web browser

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/GDGAAU/GITHUB-ACTIVITY-TRACKER
cd github-activity-analyzer
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
GITHUB_TOKEN=your_github_personal_access_token
DEBUG=True
PORT=8002
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8002` in your browser.

## 🔒 Environment Variables

- `GITHUB_TOKEN`: Your GitHub Personal Access Token
- `DEBUG`: Enable/disable debug mode (True/False)
- `PORT`: Application port (default: 8002)
- `HOST`: Host address (default: 0.0.0.0)

## 📊 API Documentation

When debug mode is enabled, access the API documentation at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## 🚀 Deployment

The project includes deployment configurations for:
- Render (`render.yaml`)
- DigitalOcean (`do-app.yaml`)
- Railway (`railway.json`)

## 👨‍💻 Author

- **Alpha-Mintamir**
  - GitHub: [@Alpha-Mintamir](https://github.com/Alpha-Mintamir)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- GDGAAU for the repository access
- FastAPI community
- Chart.js team
