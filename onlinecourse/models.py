import sys
from django.http import request
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid

# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username

# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation

# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

# Enrollment model
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

# Question Model
class Question(models.Model):
    courses = models.ManyToManyField(Course)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_content = models.TextField(null=False)
    grade_point = models.CharField(max_length=5)

    def is_get_score(self, selected_ids):
        all_choices = self.choice_set.filter(is_correct=True).count()
        if all_choices == selected_ids:
            return True
        else:
            return False

# Choice Model with:
class Choice(models.Model):
    questions = models.ManyToManyField(Question)
    choice = models.CharField(max_length=5)
    
    def correct_choice(self, ans, grade):
        if ans == grade:
            return True
        else:
            return False

# The submission model
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submission = models.CharField(max_length=5)



# VIEWS
# клиент(браузер) -=  хтмл страницу(там же яваскрипт формы и прочее) ----//

# ---------> sends request  ----------|
#                                     |
# server <-----------------------------

# middleware

# function myMiddleware(request) {
#     doing some stuff(logging, defense, ........)
#     call_next_middleware(request)
# }

# 1
# 2
# 3
# 4
# 5
# 6
# 7
# 8
# 9
# 10
# 11

# MVC !!!!

# через роутинг, система котороя мапит урл запроса на класс Контроллер и дальше на его экшн
# -----> request to controller -----> some action calls ------|   <<<<<<<<<<<<<<<<<<<<<<<<<<<<<< you can call Model абстракция над доступом в бд
#                                                             |
# ответ(json, html, just status code) <------------------------
# |
# |
# --------------> обрабатывает ответ (яваскриптом парсит json и чет выводит)