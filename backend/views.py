from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import connection
import openai
from .models import APCourse, CollegeStats, ExtracurricularActivity
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Award 
from django.http import JsonResponse

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'college.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('college_stats')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('homepage')

@login_required(login_url='login')
def college_stats(request):
    existing_college_stats = CollegeStats.objects.filter(user=request.user).exists()
    if existing_college_stats:
        return redirect('extracurriculars')
    
    if request.method == 'POST':
        gpa = request.POST.get('gpa')
        sat = request.POST.get('sat')
        act = request.POST.get('act')
        race = request.POST.get('race')
        gender = request.POST.get('gender')
        income = request.POST.get('income')

        user = request.user

        college_stat = CollegeStats.objects.create(
            user=user,
            gpa=gpa,
            sat=sat,
            act=act,
            race=race,
            gender=gender,
            income=income
        )


        college_stat.save()

        request.session['college_stats'] = {
            'gpa': gpa,
            'sat': sat,
            'act': act,
            'race': race,
            'gender': gender,
            'income': income,
        }
        return redirect('extracurriculars')

    return render(request, 'college_stats.html')


@login_required(login_url='login')
def extracurricular_activities(request):
    existing_extracurriculars = ExtracurricularActivity.objects.filter(user=request.user).exists()
    if existing_extracurriculars:
        return redirect('homepage')
    if request.method == 'POST':
        user = request.user
        form_data = {}
        for i in range(1, 11):
            extracurricular = request.POST.get(f'extracurricular_{i}')
            extracurricular_type = request.POST.get(f'extracurricular_type_{i}')
            ranking = request.POST.get(f'ranking_{i}')
            if extracurricular:
                try:
                    ExtracurricularActivity.objects.create(
                        user=user,
                        activity_name=extracurricular,
                        activity_type=extracurricular_type,
                        ranking=ranking
                    )
                    form_data[f'extracurricular_{i}'] = extracurricular
                    form_data[f'extracurricular_type_{i}'] = extracurricular_type
                    form_data[f'ranking_{i}'] = ranking
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('homepage')  
        
        messages.success(request, "Extracurricular activities saved successfully.")
        return redirect('awards')
    
    return render(request, 'extracurricular.html', {'extracurricular_numbers': range(1, 11)})

@login_required(login_url='login')


@login_required(login_url='login')
def awards(request):
    existing_awards = Award.objects.filter(user=request.user).exists()
    if existing_awards:
        return redirect('homepage')
    if request.method == 'POST':
        user = request.user
        form_data = {}
        for i in range(1, 11):
            award_name = request.POST.get(f'award_{i}')
            award_type = request.POST.get(f'award_type_{i}')
            ranking = request.POST.get(f'ranking_{i}')
            if award_name:
                try:
                    Award.objects.create(
                        user=user,
                        award_name=award_name,
                        award_type=award_type,
                        ranking=ranking
                    )
                    form_data[f'award_{i}'] = award_name
                    form_data[f'award_type_{i}'] = award_type
                    form_data[f'ranking_{i}'] = ranking
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('ap_courses')  
        
        messages.success(request, "Awards saved successfully.")
        return redirect('ap_courses')
    
    return render(request, 'awards.html', {'award_numbers': range(1, 11)})


AP_COURSES = [
    'AP Biology', 'AP Calculus AB', 'AP Calculus BC', 'AP Chemistry', 'AP Chinese Language and Culture',
    'AP Comparative Government and Politics', 'AP Computer Science A', 'AP Computer Science Principles',
    'AP English Language and Composition', 'AP English Literature and Composition', 'AP Environmental Science',
    'AP European History', 'AP French Language and Culture', 'AP German Language and Culture', 'AP Human Geography',
    'AP Italian Language and Culture', 'AP Japanese Language and Culture', 'AP Macroeconomics', 'AP Microeconomics',
    'AP Music Theory', 'AP Physics 1', 'AP Physics 2', 'AP Physics C: Electricity and Magnetism', 'AP Physics C: Mechanics',
    'AP Psychology', 'AP Spanish Language and Culture', 'AP Spanish Literature and Culture', 'AP Statistics',
    'AP Studio Art: 2-D Design', 'AP Studio Art: 3-D Design', 'AP Studio Art: Drawing', 'AP United States Government and Politics',
    'AP United States History', 'AP World History'
]

@login_required(login_url='login')
def ap_courses(request):
    if request.method == 'POST':
        user = request.user
        form_data = {}
        for i in range(1, 11):
            course = request.POST.get(f'course_{i}')
            score = request.POST.get(f'score_{i}')
            if course:
                try:
                    APCourse.objects.create(
                        user=user,
                        course=course,
                        score=score
                    )
                    form_data[f'course_{i}'] = course
                    form_data[f'score_{i}'] = score
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('homepage')
        
        messages.success(request, "AP Courses saved successfully.")
        return redirect('homepage')
    
    return render(request, 'ap_courses.html', {
        'course_numbers': range(1, 11),  
        'ap_course_list': AP_COURSES
    })
from django.db.models import Count
from django.shortcuts import get_object_or_404
from decimal import Decimal


@login_required(login_url='login')
def college(request):
	college_gpa_averages = {
			"Harvard University": Decimal('4.0'),
			"Stanford University": Decimal('3.95'),
			"Massachusetts Institute of Technology (MIT)": Decimal('4.19'),
			"Princeton University": Decimal('3.95'),
			"Yale University": Decimal('4.13'),
			"California Institute of Technology (Caltech)": Decimal('4.19'),
			"University of Chicago": Decimal('4.0'),
			"Columbia University": Decimal('4.15'),
			"University of Pennsylvania": Decimal('3.90'),
			"Johns Hopkins University": Decimal('3.93'),
			"Northwestern University": Decimal('4.10'),
			"Duke University": Decimal('4.13'),
			"University of Michigan - Ann Arbor": Decimal('3.90'),
			"University of California, Berkeley": Decimal('3.90'),
			"Cornell University": Decimal('4.07'),
			"University of California, Los Angeles (UCLA)": Decimal('3.93'),
			"University of Southern California (USC)": Decimal('3.83'),
			"Washington University in St. Louis": Decimal('4.0'),
			"Brown University": Decimal('4.10'),
			"University of Notre Dame": Decimal('4.06')
		}
	college_sat_averages = {
			"Harvard University": 1520,
			"Stanford University": 1505,
			"Massachusetts Institute of Technology (MIT)": 1543,
			"Princeton University": 1535,
			"Yale University": 1540,
			"California Institute of Technology (Caltech)": 1545,
			"University of Chicago": 1520,
			"Columbia University": 1524,
			"University of Pennsylvania": 1500,
			"Johns Hopkins University": 1545,
			"Northwestern University": 1530,
			"Duke University": 1530,
			"University of Michigan - Ann Arbor": 1490,
			"University of California, Berkeley": 1415,
			"Cornell University": 1480,
			"University of California, Los Angeles (UCLA)": 1455,
			"University of Southern California (USC)": 1440,
			"Washington University in St. Louis": 1527,
			"Brown University": 1535,
			"University of Notre Dame": 1500
		}
	college_act_averages = {
			"Harvard University": 34,
			"Stanford University": 34,
			"Massachusetts Institute of Technology (MIT)": 35,
			"Princeton University": 35,
			"Yale University": 34,
			"California Institute of Technology (Caltech)": 36,
			"University of Chicago": 34,
			"Columbia University": 35,
			"University of Pennsylvania": 34,
			"Johns Hopkins University": 34,
			"Northwestern University": 34,
			"Duke University": 34,
			"University of Michigan - Ann Arbor": 33,
			"University of California, Berkeley": 31,
			"Cornell University": 34,
			"University of California, Los Angeles (UCLA)": 32,
			"University of Southern California (USC)": 32,
			"Washington University in St. Louis": 34,
			"Brown University": 34,
			"University of Notre Dame": 34
		}
	user = request.user
	college_stats = get_object_or_404(CollegeStats, user=user)
	extracurriculars = ExtracurricularActivity.objects.filter(user=user)
	awards = Award.objects.filter(user=user)
	ap_courses = APCourse.objects.filter(user=user)
	gpa = college_stats.gpa
	act = college_stats.act
	sat = college_stats.sat

	context = {'username': user.username}
	admission_probabilities = {}

	for college in college_gpa_averages.keys():
		gpa_score = (gpa / sum(college_gpa_averages.values())) * 100
		act_score = (act / sum(college_act_averages.values())) * 100
		sat_score = (sat / sum(college_sat_averages.values())) * 100
		academic_score = (gpa_score + Decimal(act_score) + Decimal(sat_score)) / 3

		extracurricular_score = sum([4 if activity.ranking == 'A' else
									2.5 if activity.ranking == 'B' else
									1.5 if activity.ranking == 'C' else
									0.5 if activity.ranking == 'D' else
									0 for activity in extracurriculars])

		award_score = sum([4 if award.ranking == 'A' else
						2.5 if award.ranking == 'B' else
						1.5 if award.ranking == 'C' else
						0.5 if award.ranking == 'D' else
						0 for award in awards])

		ap_course_score = sum([course.score for course in ap_courses]) / ap_courses.count() if ap_courses.exists() else 0

		race_adjustment = 1
		socio_status_adjustment = 1
		college_acceptance_rates = {
		"Harvard University": 0.032,
		"Stanford University": 0.037,
		"Massachusetts Institute of Technology (MIT)": 0.040,
		"Princeton University": 0.060,
		"Yale University": 0.046,
		"California Institute of Technology (Caltech)": 0.027,
		"University of Chicago": 0.054,
		"Columbia University": 0.039,
		"University of Pennsylvania": 0.065,
		"Johns Hopkins University": 0.073,
		"Northwestern University": 0.072,
		"Duke University": 0.063,
		"University of Michigan - Ann Arbor": 0.177,
		"University of California, Berkeley": 0.113,
		"Cornell University": 0.075,
		"University of California, Los Angeles (UCLA)": 0.086,
		"University of Southern California (USC)": 0.092,
		"Washington University in St. Louis": 0.118,
		"Brown University": 0.051,
		"University of Notre Dame": 0.130
	}

		admission_probability = (((float(academic_score) + float(extracurricular_score) + float(award_score) + float(
    	ap_course_score)) / 4) * race_adjustment * socio_status_adjustment * (college_acceptance_rates[college] / 100)) * 20

		admission_probabilities[college] = admission_probability
		context['admission_probabilities'] = admission_probabilities
		context['admission_probabilities'] = admission_probabilities
		print(context)
	return render(request, 'college.html', context)
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import CollegeStats


def XHomePage(request):
    user = request.user
    context = {'username': user.username}

    return render(request, 'index.html', context)






@login_required(login_url='login')
def college_tips(request):
    college_gpa_averages = {
        "Harvard University": Decimal('4.0'),
        "Stanford University": Decimal('3.95'),
        "Massachusetts Institute of Technology (MIT)": Decimal('4.19'),
        "Princeton University": Decimal('3.95'),
        "Yale University": Decimal('4.13'),
        "California Institute of Technology (Caltech)": Decimal('4.19'),
        "University of Chicago": Decimal('4.0'),
        "Columbia University": Decimal('4.15'),
        "University of Pennsylvania": Decimal('3.90'),
        "Johns Hopkins University": Decimal('3.93'),
        "Northwestern University": Decimal('4.10'),
        "Duke University": Decimal('4.13'),
        "University of Michigan - Ann Arbor": Decimal('3.90'),
        "University of California, Berkeley": Decimal('3.90'),
        "Cornell University": Decimal('4.07'),
        "University of California, Los Angeles (UCLA)": Decimal('3.93'),
        "University of Southern California (USC)": Decimal('3.83'),
        "Washington University in St. Louis": Decimal('4.0'),
        "Brown University": Decimal('4.10'),
        "University of Notre Dame": Decimal('4.06')
    }
    college_sat_averages = {
        "Harvard University": 1520,
        "Stanford University": 1505,
        "Massachusetts Institute of Technology (MIT)": 1543,
        "Princeton University": 1535,
        "Yale University": 1540,
        "California Institute of Technology (Caltech)": 1545,
        "University of Chicago": 1520,
        "Columbia University": 1524,
        "University of Pennsylvania": 1500,
        "Johns Hopkins University": 1545,
        "Northwestern University": 1530,
        "Duke University": 1530,
        "University of Michigan - Ann Arbor": 1490,
        "University of California, Berkeley": 1415,
        "Cornell University": 1480,
        "University of California, Los Angeles (UCLA)": 1455,
        "University of Southern California (USC)": 1440,
        "Washington University in St. Louis": 1527,
        "Brown University": 1535,
        "University of Notre Dame": 1500
    }
    college_act_averages = {
        "Harvard University": 34,
        "Stanford University": 34,
        "Massachusetts Institute of Technology (MIT)": 35,
        "Princeton University": 35,
        "Yale University": 34,
        "California Institute of Technology (Caltech)": 36,
        "University of Chicago": 34,
        "Columbia University": 35,
        "University of Pennsylvania": 34,
        "Johns Hopkins University": 34,
        "Northwestern University": 34,
        "Duke University": 34,
        "University of Michigan - Ann Arbor": 33,
        "University of California, Berkeley": 31,
        "Cornell University": 34,
        "University of California, Los Angeles (UCLA)": 32, 
        "University of Southern California (USC)": 32,
        "Washington University in St. Louis": 34,
        "Brown University": 34,
        "University of Notre Dame": 34
    }
    user = request.user
    college_stats = get_object_or_404(CollegeStats, user=user)
    extracurriculars = ExtracurricularActivity.objects.filter(user=user)
    awards = Award.objects.filter(user=user)
    ap_courses = APCourse.objects.filter(user=user)
    gpa = college_stats.gpa
    act = college_stats.act
    sat = college_stats.sat

    context = {'username': user.username}
    admission_probabilities = {}

    for college in college_gpa_averages.keys():
        gpa_score = (gpa / sum(college_gpa_averages.values())) * 100
        act_score = (act / sum(college_act_averages.values())) * 100
        sat_score = (sat / sum(college_sat_averages.values())) * 100
        academic_score = (gpa_score + Decimal(act_score) + Decimal(sat_score)) / 3

        extracurricular_score = sum([4 if activity.ranking == 'A' else
                                    2.5 if activity.ranking == 'B' else
                                    1.5 if activity.ranking == 'C' else
                                    0.5 if activity.ranking == 'D' else
                                    0 for activity in extracurriculars])

        award_score = sum([4 if award.ranking == 'A' else
                        2.5 if award.ranking == 'B' else
                        1.5 if award.ranking == 'C' else
                        0.5 if award.ranking == 'D' else
                        0 for award in awards])

        ap_course_score = sum([course.score for course in ap_courses]) / ap_courses.count() if ap_courses.exists() else 0

        race_adjustment = 1
        socio_status_adjustment = 1
        college_acceptance_rates = {
            "Harvard University": 0.032,
            "Stanford University": 0.037,
            "Massachusetts Institute of Technology (MIT)": 0.040,
            "Princeton University": 0.060,
            "Yale University": 0.046,
            "California Institute of Technology (Caltech)": 0.027,
            "University of Chicago": 0.054,
            "Columbia University": 0.039,
            "University of Pennsylvania": 0.065,
            "Johns Hopkins University": 0.073,
            "Northwestern University": 0.072,
            "Duke University": 0.063,
            "University of Michigan - Ann Arbor": 0.177,
            "University of California, Berkeley": 0.113,
            "Cornell University": 0.075,
            "University of California, Los Angeles (UCLA)": 0.086,
            "University of Southern California (USC)": 0.092,
            "Washington University in St. Louis": 0.118,
            "Brown University": 0.051,
            "University of Notre Dame": 0.130
        }

        admission_probability = (((float(academic_score) + float(extracurricular_score) + float(award_score) + float(ap_course_score)) / 4) * race_adjustment * socio_status_adjustment * (college_acceptance_rates[college] / 100)) * 20

        admission_probabilities[college] = admission_probability

    context['admission_probabilities'] = admission_probabilities

    gpa_scaled = gpa / max(college_gpa_averages.values())
    act_scaled = act / max(college_act_averages.values())
    sat_scaled = sat / max(college_sat_averages.values())
    extracurricular_scaled = extracurricular_score / 20 
    if ap_course_score > 0:
        ap_course_scaled = ap_course_score / ap_courses.count()/2
    else: 
        ap_course_scaled= 0

    
    min_score = min(gpa_scaled, act_scaled, sat_scaled, extracurricular_scaled, ap_course_scaled)
    if min_score == gpa_scaled:
        min_score_type = "GPA"
    elif min_score == act_scaled:
        min_score_type = "ACT"
    elif min_score == sat_scaled:
        min_score_type = "SAT"
    elif min_score == extracurricular_scaled:
        min_score_type = "Extracurricular Activities"
    elif min_score == ap_course_scaled:
        min_score_type = "AP Courses"
        context = {'min_score': min_score}
    context = {
    'username': user.username,
    'lowest_score': min_score,
    'lowest_score_type': min_score_type
}
    return render(request, 'college_tips.html', context)


