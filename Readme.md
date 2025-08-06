# 🎓 AI-Powered Mentorship Platform

An intelligent Django-based mentorship platform that connects students with mentors, featuring AI-powered answer generation and multi-language translation capabilities.

## 🌟 Features

### 🤖 AI-Powered Features
- **AI Answer Generation**: Mentors can generate detailed, comprehensive answers using a pre-trained Qwen language model
- **Smart Translation**: Real-time translation of questions and answers in multiple languages (English, Chinese, Japanese, Hindi)
- **AI Answer Enhancement**: Mentors can improve their responses using AI assistance

### 👨‍🎓 Student Dashboard
- **Question Management**: Post questions with categories (Programming, Career, Project Help, General Learning)
- **Real-time Updates**: View mentor responses as they arrive
- **Multi-language Support**: Translate questions and answers to preferred languages
- **Progress Tracking**: Monitor question status (Pending, Answered, Closed)

### 👨‍🏫 Mentor Dashboard
- **Question Overview**: View all student questions with filtering options
- **AI-Assisted Responses**: Generate or enhance answers using AI
- **Translation Tools**: Communicate effectively across language barriers
- **Student Analytics**: Track mentoring activities and statistics

### 🔧 Technical Features
- **Django Framework**: Modern web framework with robust security
- **User Authentication**: Role-based access (Student/Mentor)
- **Database Persistence**: SQLite database for storing questions, answers, and user data
- **Responsive Design**: Bootstrap for mobile-friendly interface
- **AJAX Operations**: Seamless user experience without page reloads

## 🏗️ Project Structure

```
mentor/
├── web/                          # Django project root
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── db.sqlite3               # SQLite database
│   ├── projectname/             # Django project settings
│   │   ├── __init__.py
│   │   ├── settings.py          # Django configuration
│   │   ├── urls.py              # URL routing
│   │   ├── wsgi.py              # WSGI configuration
│   │   └── asgi.py              # ASGI configuration
│   ├── auth/                    # Authentication app
│   │   ├── models.py            # Database models (User, Question, Answer)
│   │   ├── views.py             # View controllers and AI integration
│   │   ├── admin.py             # Django admin configuration
│   │   ├── apps.py              # App configuration
│   │   ├── templates/           # HTML templates
│   │   │   ├── Login.html       # Login page
│   │   │   ├── Register.html    # Registration page
│   │   │   ├── Student.html     # Student dashboard
│   │   │   └── Mentor.html      # Mentor dashboard
│   │   ├── templatetags/        # Custom template filters
│   │   │   └── mentor_filters.py
│   │   └── migrations/          # Database migrations
│   └── home/                    # Home app
│       ├── models.py
│       ├── views.py
│       ├── admin.py
│       ├── Templates/           # Home app templates
│       │   ├── Base.html        # Base template
│       │   ├── Home.html        # Landing page
│       │   └── About.html       # About page
│       └── migrations/
├── saved_qwen_model/            # Pre-trained AI model (config files only)
│   ├── config.json              # Model configuration
│   ├── tokenizer.json           # Tokenizer configuration
│   ├── vocab.json               # Vocabulary
│   └── ...                      # Other model config files
├── translate.ipynb              # Translation development notebook
├── Untitled.ipynb              # Additional notebooks
├── output_audio.mp3             # Audio file
└── README.md                    # Project documentation
```
├── translate.ipynb              # Translation development notebook
├── anaconda_projects/           # Anaconda project files
└── README.md                    # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.2
- PyTorch
- Transformers library

### 1. Clone the Repository
```bash
git clone https://github.com/Praharsh7270/Mentor.git
cd Mentor
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
cd web
pip install -r requirements.txt
```

### 4. Model Setup
**Important Note**: The large AI model file (`model.safetensors`) is not included in the repository due to GitHub's file size limitations. You will need to:

1. Download the Qwen model separately from Hugging Face or another source
2. Place the `model.safetensors` file in the `saved_qwen_model/` directory
3. Ensure all model configuration files are present

Alternatively, you can modify the code to use a different model or implement a different AI solution.

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 6. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the platform.

## 🎯 Usage Guide

### For Students
1. **Register/Login** as a student
2. **Post Questions**: 
   - Write clear question titles and descriptions
   - Select appropriate categories
   - Use translation features if needed
3. **View Answers**: 
   - Monitor your dashboard for mentor responses
   - Translate answers to your preferred language
   - Track question status

### For Mentors
1. **Register/Login** as a mentor
2. **Browse Questions**: 
   - View all student questions
   - Filter by status and category
   - Use translation tools to understand questions in different languages
3. **Provide Answers**:
   - Write comprehensive responses
   - Use "Answer with AI" for AI-generated responses
   - Use "AI Assist" to enhance your existing answers
   - Submit answers with real-time updates

## 🤖 AI Integration

### Qwen Language Model
The platform integrates a pre-trained Qwen model for:
- **Generating detailed mentor responses**
- **Enhancing existing answers**
- **Providing context-aware suggestions**

### Translation Service
- **Multi-language support**: English, Chinese (中文), Japanese (日本語), Hindi (हिंदी)
- **Real-time translation** of questions and answers
- **Context preservation** during translation

## 📊 Database Schema

### Models
- **UserProfile**: Extends Django User with role-based access
- **Question**: Student questions with categories and status tracking
- **Answer**: Mentor responses linked to questions

### Relationships
- One-to-Many: User → Questions
- One-to-Many: User → Answers  
- One-to-Many: Question → Answers

## 🛠️ Technology Stack

### Backend
- **Django**: Web framework
- **SQLite**: Database
- **PyTorch**: AI model framework (if using local model)
- **Transformers**: Hugging Face library

### Frontend
- **Bootstrap**: CSS framework
- **JavaScript ES6**: Dynamic interactions
- **AJAX**: Asynchronous operations

### AI/ML
- **Qwen Model**: Language model for answer generation (model file not included)
- **Custom Translation API**: Multi-language support

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the web directory:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### AI Model Configuration
The Qwen model configuration files are in `saved_qwen_model/`. The large model file (`model.safetensors`) needs to be downloaded separately due to size constraints.

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure ALLOWED_HOSTS
5. Use environment variables for sensitive data

### Docker Deployment (Optional)
```dockerfile
# Dockerfile example
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Praharsh7270**
- GitHub: [@Praharsh7270](https://github.com/Praharsh7270)
- Project Link: [https://github.com/Praharsh7270/Mentor](https://github.com/Praharsh7270/Mentor)

## 🙏 Acknowledgments

- Hugging Face for the Transformers library
- Qwen model developers
- Django community
- Bootstrap team for the UI framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Praharsh7270/Mentor/issues) section
2. Create a new issue with detailed information
3. Contact the maintainer

## ⚠️ Important Notes

- **Large Model File**: The `model.safetensors` file (3.1GB) is not included in this repository due to GitHub's file size limitations
- **Model Setup**: You'll need to download the Qwen model separately or configure an alternative AI solution
- **Dependencies**: Ensure all Python dependencies are installed as specified in `requirements.txt`

---

⭐ **Star this repository if you find it helpful!** ⭐