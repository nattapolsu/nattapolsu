import datetime
import pytz
from django.shortcuts import render, redirect
from online.models import Course
from app_quiz.models import Quiz, Question, StudentAnswer
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def quiz(request, code):
    #try:
        course = Course.objects.get(code=code)
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            start = request.POST.get('start')
            end = request.POST.get('end')
            publish_status = request.POST.get('checkbox')
            quiz = Quiz(title=title, description=description, start=start,end=end, publish_status=publish_status, course=course)
            quiz.save()
            return redirect('addQuestion', code=code, quiz_id=quiz.id)
        else:
            return render(request, 'quiz.html', {'course': course,})

    #except:
        return render(request, 'error.html')


def addQuestion(request, code, quiz_id):
    #try:
        course = Course.objects.get(code=code)
        quiz = Quiz.objects.get(id=quiz_id)
        if request.method == 'POST':
            question = request.POST.get('question')
            option1 = request.POST.get('option1')
            option2 = request.POST.get('option2')
            option3 = request.POST.get('option3')
            option4 = request.POST.get('option4')
            answer = request.POST.get('answer')
            marks = request.POST.get('marks')
            explanation = request.POST.get('explanation')
            question = Question(question=question, option1=option1, option2=option2,
                                option3=option3, option4=option4, answer=answer, quiz=quiz, marks=marks, explanation=explanation)
            question.save()
            messages.success(request, 'Question added successfully')
        else:
            return render(request, 'addQuestion.html', {'course': course, 'quiz': quiz})
        if 'saveOnly' in request.POST:
            return redirect('allQuizzes', code=code)
        return render(request, 'addQuestion.html', {'course': course, 'quiz': quiz})
    #except:
        return render(request, 'error.html')


def allQuizzes(request, code):
    course = Course.objects.get(code=code)
    quizzes = Quiz.objects.filter(course=course)

    # set time zone
    tz = pytz.timezone('Asia/Bangkok')

    for quiz in quizzes:
        quiz.total_questions = Question.objects.filter(quiz=quiz).count()

        # convert quiz start time to time zone
        quiz_start_time = quiz.start.astimezone(tz)

        # convert current time to time zone
        now = datetime.datetime.now().astimezone(tz)

        if quiz_start_time < now:
            quiz.started = True
        else:
            quiz.started = False
        quiz.save()

    return render(request, 'allQuizzes.html', {'course': course, 'quizzes': quizzes})


def myQuizzes(request, code):
    #if is_student_authorised(request, code):
        course = Course.objects.get(code=code)
        quizzes = Quiz.objects.filter(course=course)

        tz = pytz.timezone('Asia/Bangkok')
        # check if that student has already attempted this quiz
        for quiz in quizzes:
            student_answers = StudentAnswer.objects.filter( quiz=quiz)
            if student_answers.count() > 0:
                quiz.attempted = True
            else:
                quiz.attempted = False

        active_quizzes = []
        previous_quizzes = []

        for quiz in quizzes:
            student_answers = StudentAnswer.objects.filter( quiz=quiz)
            if quiz.end < datetime.datetime.now(tz) or student_answers.count() > 0:
                previous_quizzes.append(quiz)
            else:
                active_quizzes.append(quiz)

        for previousQuiz in previous_quizzes:
            total_marks_obtained = 0
            student_answers = StudentAnswer.objects.filter( quiz=previousQuiz)

            for student_answer in student_answers:
                total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
            previousQuiz.total_marks_obtained = total_marks_obtained

            previousQuiz.total_marks = 0
            for question in previousQuiz.question_set.all():
                previousQuiz.total_marks += question.marks

            try:
                previousQuiz.percentage = (total_marks_obtained / previousQuiz.total_marks) * 100
                previousQuiz.percentage = round(previousQuiz.percentage, 2)
            except ZeroDivisionError:
                previousQuiz.percentage = 0

        for previousQuiz in previous_quizzes:
            previousQuiz.total_questions = Question.objects.filter(quiz=previousQuiz).count()
        for activeQuiz in active_quizzes:
            activeQuiz.total_questions = Question.objects.filter(quiz=activeQuiz).count()

        return render(request, 'myQuizzes.html', {'course': course, 'quizzes': quizzes, 'active_quizzes': active_quizzes, 'previous_quizzes': previous_quizzes})
    #else:
        return redirect('std_login')


def startQuiz(request, code, quiz_id):
    #if is_student_authorised(request, code):
        course = Course.objects.get(code=code)
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        total_questions = questions.count()

        marks = 0
        for question in questions:
            marks += question.marks
        quiz.total_marks = marks

        context = { 'course': course, 
                    'quiz': quiz, 
                    'questions': questions, 
                    'total_questions': total_questions
                }
        return render(request, 'portalStdNew.html', context)
    #else:
        return redirect('std_login')


def studentAnswer(request, code, quiz_id):
    #if is_student_authorised(request, code):
        course = Course.objects.get(code=code)
        quiz = Quiz.objects.get(id=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        #student = Student.objects.get(student_id=request.session['student_id'])

        for question in questions:
            answer = request.POST.get(str(question.id))
            student_answer = StudentAnswer( quiz=quiz, question=question,answer=answer, marks=question.marks if answer == question.answer else 0)
            # prevent duplicate answers & multiple attempts
            try:
                student_answer.save()
            except:
                redirect('myQuizzes', code=code)
        return redirect('myQuizzes', code=code)
    #else:
        return redirect('std_login')


def quizSummary(request, code, quiz_id):
    #if is_faculty_authorised(request, code):
        course = Course.objects.get(code=code)
        quiz = Quiz.objects.get(id=quiz_id)

        questions = Question.objects.filter(quiz=quiz)
        time = datetime.datetime.now()
        total_students = User.objects.filter(course=course).count()
        for question in questions:
            question.A = StudentAnswer.objects.filter(
                question=question, answer='A').count()
            question.B = StudentAnswer.objects.filter(
                question=question, answer='B').count()
            question.C = StudentAnswer.objects.filter(
                question=question, answer='C').count()
            question.D = StudentAnswer.objects.filter(
                question=question, answer='D').count()
        # students who have attempted the quiz and their marks
        students = User.objects.filter(course=course)
        for student in students:
            student_answers = StudentAnswer.objects.filter(
                student=student, quiz=quiz)
            total_marks_obtained = 0
            for student_answer in student_answers:
                total_marks_obtained += student_answer.question.marks if student_answer.answer == student_answer.question.answer else 0
            student.total_marks_obtained = total_marks_obtained

        if request.method == 'POST':
            quiz.publish_status = True
            quiz.save()
            return redirect('quizSummary', code=code, quiz_id=quiz.id)
        # check if student has attempted the quiz
        for student in students:
            if StudentAnswer.objects.filter(student=student, quiz=quiz).count() > 0:
                student.attempted = True
            else:
                student.attempted = False
        for student in students:
            student_answers = StudentAnswer.objects.filter(
                student=student, quiz=quiz)
            for student_answer in student_answers:
                student.submission_time = student_answer.created_at.strftime(
                    "%a, %d-%b-%y at %I:%M %p")

        context = { 'course': course, 
                    'quiz': quiz, 
                    'questions': questions, 
                    'time': time, 
                    'total_students': total_students,
                    'students': students
                   }
        return render(request, 'quizSummaryFaculty.html', context)

    #else:
        return redirect('std_login')