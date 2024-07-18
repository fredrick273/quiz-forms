from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, TextQuestion,McqOption,MCQ,Response,TextAnswer,McqAnswer

def index(request):
    return render(request, 'quiz/index.html')

# Create your views here.
@login_required
def createquiz(request):
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        viewanswer = 'viewans' in request.POST
        showscore = 'showscore' in request.POST

        quiz = Quiz.objects.create(
            title=title,
            user=request.user,
            viewanswer=viewanswer,
            showscore=showscore
        )
        text_question_count = 1
        while True:
            text_question = request.POST.get(f'textquestion_{text_question_count}')
            if not text_question:
                break
            TextQuestion.objects.create(
                question=text_question,
                quiz=quiz
            )
            text_question_count += 1

        mcq_question_count = 1
        while True:
            mcq_question = request.POST.get(f'mcq_{mcq_question_count}')
            if not mcq_question:
                break
            points = request.POST.get(f'points_{mcq_question_count}')
            mcq = MCQ.objects.create(
                question=mcq_question,
                quiz=quiz,
                points=points
            )

            option_count = 1
            while True:
                option_text = request.POST.get(f'option_{mcq_question_count}_{option_count}')
                if not option_text:
                    break
                is_correct = f'correct_{mcq_question_count}_{option_count}' in request.POST
                McqOption.objects.create(
                    text=option_text,
                    is_correct=is_correct,
                    mcq=mcq
                )
                option_count += 1

            mcq_question_count += 1
        return redirect('quiz_list')
    return render(request,"quiz/createquiz.html")

def quizlist(request):
    return render(request,'quiz/quizlist.html',{'quizes': Quiz.objects.all()})

def attemptquiz(request,id):
    quiz = get_object_or_404(Quiz,id = id)
    if request.method == 'POST':
        
        res = Response(
            quiz = quiz
        )
        res.save()
        for i in request.POST:
            key = i.split('_')
            if key[0] == 'text':
                textans = TextAnswer(
                    question = TextQuestion.objects.get(id = int(key[1])),
                    response = res,
                    answer = request.POST.get(i)
                )
                textans.save()
            elif key[0] == 'mcq':
                print(MCQ.objects.get(id = int(key[1])),McqOption.objects.get(id = int(request.POST.get(i))))
                mcqans = McqAnswer(
                    question = MCQ.objects.get(id = int(key[1])),
                    response = res,
                    answer = McqOption.objects.get(id = int(request.POST.get(i)))
                )
                mcqans.save()
                print()
            print(key)
        return redirect('view_attempted_response', res.id)
    
    quiz = get_object_or_404(Quiz,id = id)
    textquestions = TextQuestion.objects.filter(quiz= quiz)
    mcqs = MCQ.objects.filter(quiz=quiz)
    mcqqustions = []
    for i in mcqs:
        options = McqOption.objects.filter(mcq = i)
        mcqqustions.append({
            'question': i,
            'options': options
        })
    print(mcqqustions)

    return render(request,'quiz/attemptquiz.html', {'quiz':quiz,'text':textquestions,'mcqs':mcqqustions})



def view_attempted_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    quiz = response.quiz
    points = 0
    max_points = 0

    text_answers = TextAnswer.objects.filter(response=response)
    mcq_answers = McqAnswer.objects.filter(response=response)

    for i in mcq_answers:
        max_points += i.answer.mcq.points
        if i.answer.is_correct:
            points += i.answer.mcq.points

    text_answers_list = [{'question': answer.question.question, 'answer': answer.answer} for answer in text_answers]
    mcq_answers_list = [
        {
            'question': answer.question.question,
            'answer': answer.answer.text,
            'options': McqOption.objects.filter(mcq = answer.question),
            'is_correct': answer.answer.is_correct if quiz.viewanswer else None,
            'points': answer.question.points if quiz.showscore else None,
            'correct_ans': McqOption.objects.get(mcq = answer.question, is_correct = True).text
        }
        for answer in mcq_answers
    ]

    attempted_response = {
        'response_id': response.id,
        'time': response.time,
        'text_answers': text_answers_list,
        'mcq_answers': mcq_answers_list,
        
    }

    context = {
        'quiz': quiz,
        'attempted_response': attempted_response,
        'viewanswer': quiz.viewanswer,
        'showscore': quiz.showscore,
        'points': points,
        'max_points':max_points
    }

    return render(request, 'quiz/view_attempted_response.html', context)



def admin_viewresponse(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    quiz = response.quiz
    points = 0
    max_points = 0

    text_answers = TextAnswer.objects.filter(response=response)
    mcq_answers = McqAnswer.objects.filter(response=response)

    for i in mcq_answers:
        max_points += i.answer.mcq.points
        if i.answer.is_correct:
            points += i.answer.mcq.points

    text_answers_list = [{'question': answer.question.question, 'answer': answer.answer} for answer in text_answers]
    mcq_answers_list = [
        {
            'question': answer.question.question,
            'answer': answer.answer.text,
            'options': McqOption.objects.filter(mcq = answer.question),
            'is_correct': answer.answer.is_correct if quiz.viewanswer else None,
            'points': answer.question.points if quiz.showscore else None,
            'correct_ans': McqOption.objects.get(mcq = answer.question, is_correct = True).text
        }
        for answer in mcq_answers
    ]

    attempted_response = {
        'response_id': response.id,
        'time': response.time,
        'text_answers': text_answers_list,
        'mcq_answers': mcq_answers_list,
        
    }

    context = {
        'quiz': quiz,
        'attempted_response': attempted_response,
        'viewanswer': quiz.viewanswer,
        'showscore': quiz.showscore,
        'points': points,
        'max_points':max_points
    }

    return render(request, 'quiz/admin_viewresponse.html', context)


@login_required
def view_quiz_reponses(request, id):
    quiz = get_object_or_404(Quiz,id = id)
    responses = Response.objects.filter(quiz = quiz)
    return render(request,'quiz/view_quiz_response.html', {'responses': responses})