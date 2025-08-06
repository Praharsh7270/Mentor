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
- **Django 5.2 Framework**: Modern web framework with robust security
- **User Authentication**: Role-based access (Student/Mentor)
- **Database Persistence**: SQLite database for storing questions, answers, and user data
- **Responsive Design**: Bootstrap 5.3.7 for mobile-friendly interface
- **AJAX Operations**: Seamless user experience without page reloads

## 🏗️ Project Structure

```
Mentorship/
├── web/                          # Django project root
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   ├── db.sqlite3               # SQLite database
│   ├── projectname/             # Django project settings
│   ├── auth/                    # Authentication app
│   │   ├── models.py            # Database models (User, Question, Answer)
│   │   ├── views.py             # View controllers and AI integration
│   │   ├── templates/           # HTML templates
│   │   │   ├── Base.html        # Base template
│   │   │   ├── student.html     # Student dashboard
│   │   │   ├── mentor.html      # Mentor dashboard
│   │   │   └── index.html       # Landing page
│   │   └── templatetags/        # Custom template filters
│   └── home/                    # Home app
├── saved_qwen_model/            # Pre-trained AI model
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
git clone https://github.com/Praharsh7270/Mentorship.git
cd Mentorship
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

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 5. Run the Server
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
- **Django 5.2**: Web framework
- **SQLite**: Database
- **PyTorch**: AI model framework
- **Transformers**: Hugging Face library

### Frontend
- **Bootstrap 5.3.7**: CSS framework
- **JavaScript ES6**: Dynamic interactions
- **AJAX**: Asynchronous operations

### AI/ML
- **Qwen Model**: Language model for answer generation
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
The Qwen model is pre-configured in `saved_qwen_model/`. Ensure the model files are present for AI features to work.

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
- Project Link: [https://github.com/Praharsh7270/Mentorship](https://github.com/Praharsh7270/Mentorship)

## 🙏 Acknowledgments

- Hugging Face for the Transformers library
- Qwen model developers
- Django community
- Bootstrap team for the UI framework

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/Praharsh7270/Mentorship/issues) section
2. Create a new issue with detailed information
3. Contact the maintainer

---

⭐ **Star this repository if you find it helpful!** ⭐