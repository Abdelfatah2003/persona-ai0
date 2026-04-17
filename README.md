# AI Personality & Career Recommendation System

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Deploy](https://vercel.com/badge?theme=github)

An intelligent system for analyzing user personality and recommending career paths and friends using the Big Five Personality Model and AI/ML techniques.

## Features

- **Personality Analysis**: Comprehensive analysis using the Big Five (OCEAN) personality model
- **ML-Enhanced Predictions**: Neural network-based personality predictions
- **Career Recommendations**: Personalized career suggestions based on personality traits
- **User Similarity**: Find and connect with like-minded individuals
- **Text Analysis**: NLP-powered analysis of free-text descriptions
- **Bilingual Support**: Full English and Arabic language support
- **Security**: JWT authentication, rate limiting, input validation
- **Vercel Ready**: Full deployment support on Vercel

## Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/Abdelfatah2003/persona-ai.git
cd persona-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB URI

# Start MongoDB (required)
mongod --dbpath /path/to/data

# Run the application
python app.py
```

### Vercel Deployment

1. Push to GitHub
2. Connect to Vercel: https://vercel.com/new
3. Import repository
4. Set environment variables:
   - `MONGO_URI`: Your MongoDB connection string
   - `SECRET_KEY`: Random secret key
   - `JWT_SECRET_KEY`: JWT secret key
5. Deploy!

## Project Structure

```
persona-ai/
├── api/                    # Vercel serverless functions
├── ai_engine/              # AI/ML modules
│   ├── ml_predictor.py     # ML-based personality prediction
│   ├── personality_analyzer.py
│   ├── text_processor.py
│   └── recommender/
├── backend/                # Flask backend
│   ├── routes/            # API endpoints
│   ├── models/            # Data models
│   ├── security.py        # Security utilities
│   ├── logging_config.py  # Logging setup
│   └── email_service.py   # Email service
├── frontend/              # Web interface
│   ├── css/
│   ├── js/
│   └── *.html
├── database/             # Database schemas
├── docs/                 # Documentation
├── tests/                # Test suite
└── app.py               # Main application
```

## Environment Variables

Create a `.env` file with:

```env
# MongoDB
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/persona_ai

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# Flask
FLASK_ENV=production
FLASK_DEBUG=0
```

## API Documentation

Full API documentation is available in [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | User login |
| POST | /api/personality/analyze | Analyze quiz answers |
| POST | /api/personality/analyze-text | Analyze free text |
| POST | /api/personality/save | Save personality results |
| POST | /api/recommendations/careers | Get career recommendations |
| POST | /api/recommendations/users | Find similar users |

## Testing

```bash
# Run all tests
pytest tests/test_comprehensive.py -v

# Run with coverage
pytest --cov=. --cov-report=html
```

## Tech Stack

- **Backend**: Flask, Python
- **Database**: MongoDB
- **AI/ML**: NumPy, NLTK
- **Frontend**: HTML5, CSS3, JavaScript
- **Security**: JWT, bcrypt
- **Deployment**: Vercel

## Security Features

- JWT Authentication
- Bcrypt password hashing (12 rounds)
- Rate limiting
- Input validation & sanitization
- Audit logging

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Abdelfatah2003**

---

For support, open an issue on GitHub.
