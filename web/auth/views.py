from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UserProfile, Question, Answer
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import torch
import os


# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Validate required fields
        if not email or not password:
            messages.error(request, "Please fill in all required fields")
            return render(request, "Login.html")
        
        if not email.strip() or not password.strip():
            messages.error(request, "Email and password cannot be empty")
            return render(request, "Login.html")
        
        # Django's default authentication uses username, but we can find user by email
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Check user role and redirect accordingly
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.role == 'mentor':
                        messages.success(request, f"Welcome back, {user.first_name}! (Mentor)")
                        return redirect("mentor")  # Redirect to mentor dashboard
                    elif user_profile.role == 'student':
                        messages.success(request, f"Welcome back, {user.first_name}! (Student)")
                        return redirect("student")  # Redirect to student dashboard
                except UserProfile.DoesNotExist:
                    # If no profile exists, create a default one
                    UserProfile.objects.create(user=user, role='student')
                    messages.info(request, "Profile created with default role.")
                    return redirect("student")
                
                return redirect("home")
            else:
                messages.error(request, "Invalid email or password")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, "Login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        # Validate required fields
        if not username or not fullname or not email or not password or not role:
            messages.error(request, "Please fill in all required fields")
            return render(request, "Register.html")
        
        # Validate field content
        if not username.strip() or not fullname.strip() or not email.strip() or not password.strip():
            messages.error(request, "All fields must contain valid information")
            return render(request, "Register.html")
        
        # Validate password length
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, "Register.html")
        
        # Validate email format (basic check)
        if "@" not in email or "." not in email:
            messages.error(request, "Please enter a valid email address")
            return render(request, "Register.html")

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, "Register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use a different email address.")
            return render(request, "Register.html")

        # Validate role selection
        if role not in ['mentor', 'student']:
            messages.error(request, "Please select a valid role")
            return render(request, "Register.html")

        try:
            # Create the user
            user = User.objects.create(
                username=username,
                email=email,
                first_name=fullname,
            )
            user.set_password(password)
            user.save()
            
            # Create the user profile with role
            UserProfile.objects.create(
                user=user,
                role=role
            )
            
            messages.success(request, f"Account created successfully as {role.title()}! Please login.")
            return redirect("login")
            
        except Exception as e:
            messages.error(request, "An error occurred while creating your account. Please try again.")
            return render(request, "Register.html")

    return render(request, "Register.html")


def logout(request): 
    auth_logout(request)
    return redirect("login")


@login_required
def mentor(request):
    # Check if user has mentor role
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'mentor':
            messages.error(request, "Access denied. Mentor role required.")
            return redirect("home")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("home")
    
    # Handle answer submission
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_content = request.POST.get('answer_content')
        
        if question_id and answer_content:
            try:
                question = Question.objects.get(id=question_id)
                answer = Answer.objects.create(
                    question=question,
                    mentor=request.user,
                    content=answer_content
                )
                
                # Update question status to answered
                question.status = 'answered'
                question.save()
                
                return JsonResponse({
                    'success': True,
                    'answer': {
                        'id': answer.id,
                        'content': answer.content,
                        'mentor_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                        'created_at': answer.created_at.strftime('%B %d, %Y at %I:%M %p')
                    }
                })
            except Question.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Question not found'
                }, status=404)
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Question ID and answer content are required'
            }, status=400)
    
    # Get all questions with student information
    questions = Question.objects.select_related('student').prefetch_related('answers__mentor').order_by('-created_at')
    
    context = {
        'questions': questions
    }
    
    return render(request, "Mentor.html", context)


@login_required
def student(request):
    # Check if user has student role
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.role != 'student':
            messages.error(request, "Access denied. Student role required.")
            return redirect("home")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("home")
    
    # Handle question posting
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        
        if title and content and category:
            try:
                question = Question.objects.create(
                    student=request.user,
                    title=title,
                    content=content,
                    category=category
                )
                messages.success(request, "Question posted successfully!")
                return JsonResponse({
                    'success': True,
                    'question': {
                        'id': question.id,
                        'title': question.title,
                        'content': question.content,
                        'category': question.category,
                        'status': question.status,
                        'created_at': question.created_at.strftime('%B %d, %Y at %I:%M %p')
                    }
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=500)
        else:
            return JsonResponse({
                'success': False,
                'error': 'All fields are required'
            }, status=400)
    
    # Get user's questions for display
    questions = Question.objects.filter(student=request.user).order_by('-created_at')
    
    context = {
        'questions': questions
    }
    
    return render(request, "Student.html", context)


# AI Translation Service
def load_qwen_model():
    """Load the saved Qwen model for translation"""
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
    
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saved_qwen_model")
        
        if os.path.exists(model_path):
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype="auto",
                device_map="auto"
            )
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            return model, tokenizer, device
        else:
            return None, None, None
    except Exception as e:
        print(f"Error loading Qwen model: {e}")
        return None, None, None


def translate_text_with_qwen(text, target_language):
    """Translate text using the Qwen model"""
    try:
        model, tokenizer, device = load_qwen_model()
        
        if not model or not tokenizer:
            return None
        
        # Create translation prompt based on target language
        language_prompts = {
            "chinese": f"Please translate the following text into Chinese: {text}",
            "japanese": f"Please translate the following text into Japanese: {text}",
            "hindi": f"Please translate the following text into Hindi: {text}",
            "english": f"Please translate the following text into English: {text}"
        }
        
        prompt = language_prompts.get(target_language.lower(), f"Please translate the following text into {target_language}: {text}")
        
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant specialized in translation."},
            {"role": "user", "content": prompt}
        ]
        
        text_input = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = tokenizer([text_input], return_tensors="pt").to(device)
        
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True
        )
        
        output_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        
        output_text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
        
        return output_text.strip()
        
    except Exception as e:
        print(f"Translation error: {e}")
        return None


def generate_ai_answer(question_title, question_content, context_prompt=""):
    """Generate AI answer using the Qwen model for mentoring"""
    try:
        model, tokenizer, device = load_qwen_model()
        
        if not model or not tokenizer:
            return None
        
        # Create a detailed prompt for generating mentoring answers
        if context_prompt:
            # If there's existing content, improve it
            user_prompt = f"""
{context_prompt}

Please enhance and expand this response to make it more comprehensive, detailed, and helpful for the student.
"""
        else:
            # Generate fresh answer
            user_prompt = f"""
A student has asked the following question:

Title: {question_title}
Question: {question_content}

Please provide a detailed, comprehensive answer that will help the student learn and understand the topic better. Your response should be:
1. Educational and thorough
2. Encouraging and supportive
3. Include practical examples when relevant
4. Break down complex topics into understandable parts
5. Provide actionable advice when appropriate
6. Be written in a mentoring tone
"""
        
        messages = [
            {"role": "system", "content": "You are an experienced mentor and educator who provides detailed, helpful, and encouraging answers to students' questions."},
            {"role": "user", "content": user_prompt}
        ]
        
        text_input = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = tokenizer([text_input], return_tensors="pt").to(device)
        
        generated_ids = model.generate(
            model_inputs.input_ids,
            max_new_tokens=1024,  # Longer response for detailed answers
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
        
        output_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        
        output_text = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
        
        return output_text.strip()
        
    except Exception as e:
        print(f"AI answer generation error: {e}")
        return None


@csrf_exempt
@login_required
def delete_question(request, question_id):
    """Handle question deletion"""
    if request.method == 'DELETE':
        try:
            question = Question.objects.get(id=question_id, student=request.user)
            question.delete()
            return JsonResponse({'success': True, 'message': 'Question deleted successfully'})
        except Question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def generate_ai_answer_view(request):
    """Handle AI answer generation requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_id = data.get('question_id')
            context_prompt = data.get('context_prompt', '')
            
            if not question_id:
                return JsonResponse({'error': 'Question ID is required'}, status=400)
            
            # Get the question
            try:
                question = Question.objects.get(id=question_id)
            except Question.DoesNotExist:
                return JsonResponse({'error': 'Question not found'}, status=404)
            
            # Generate AI answer
            ai_answer = generate_ai_answer(
                question.title, 
                question.content, 
                context_prompt
            )
            
            if ai_answer:
                return JsonResponse({
                    'success': True,
                    'ai_answer': ai_answer,
                    'question_title': question.title,
                    'question_content': question.content
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to generate AI answer. Please try again.'
                }, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@login_required
def translate_content(request):
    """Handle AJAX requests for content translation"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            target_language = data.get('language', 'english')
            
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            
            # Use the Qwen model for translation
            translated_text = translate_text_with_qwen(text, target_language)
            
            if translated_text:
                return JsonResponse({
                    'success': True,
                    'translated_text': translated_text,
                    'original_text': text,
                    'target_language': target_language
                })
            else:
                # Fallback translations if model fails
                fallback_translations = {
                    'chinese': {
                        'Welcome back': '欢迎回来',
                        'Ask Your Mentor': '询问您的导师',
                        'Question Title': '问题标题',
                        'Question Details': '问题详情',
                        'Category': '类别',
                        'Post Question': '发布问题',
                        'What would you like to ask?': '您想问什么？',
                        'Describe your question in detail...': '详细描述您的问题...',
                        'Ready to continue your learning journey? Explore your progress, connect with mentors, and achieve your goals!': '准备继续您的学习之旅？探索您的进步，与导师联系，实现您的目标！'
                    },
                    'japanese': {
                        'Welcome back': 'おかえりなさい',
                        'Ask Your Mentor': 'メンターに質問する',
                        'Question Title': '質問のタイトル',
                        'Question Details': '質問の詳細',
                        'Category': 'カテゴリー',
                        'Post Question': '質問を投稿',
                        'What would you like to ask?': '何を質問したいですか？',
                        'Describe your question in detail...': '質問を詳しく説明してください...',
                        'Ready to continue your learning journey? Explore your progress, connect with mentors, and achieve your goals!': '学習の旅を続ける準備はできていますか？進歩を探り、メンターとつながり、目標を達成しましょう！'
                    },
                    'hindi': {
                        'Welcome back': 'वापसी पर स्वागत है',
                        'Ask Your Mentor': 'अपने मेंटर से पूछें',
                        'Question Title': 'प्रश्न का शीर्षक',
                        'Question Details': 'प्रश्न का विवरण',
                        'Category': 'श्रेणी',
                        'Post Question': 'प्रश्न पोस्ट करें',
                        'What would you like to ask?': 'आप क्या पूछना चाहते हैं?',
                        'Describe your question in detail...': 'अपने प्रश्न का विस्तार से वर्णन करें...',
                        'Ready to continue your learning journey? Explore your progress, connect with mentors, and achieve your goals!': 'अपनी सीखने की यात्रा जारी रखने के लिए तैयार हैं? अपनी प्रगति देखें, मेंटर्स से जुड़ें, और अपने लक्ष्य हासिल करें!'
                    }
                }
                
                translated = fallback_translations.get(target_language.lower(), {}).get(text, text)
                
                return JsonResponse({
                    'success': True,
                    'translated_text': translated,
                    'original_text': text,
                    'target_language': target_language,
                    'fallback': True
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
