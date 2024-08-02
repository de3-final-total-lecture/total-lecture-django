from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

LANGUAGE_CHOICES = [
    ("None", "Language"),
    ("Python", "Python"), ("Java", "Java"), ("JavaScript", "JavaScript"), ("HTML/CSS", "HTML/CSS"),
    ("Kotlin", "Kotlin"),
    ("C", "C"), ("C++", "C++"), ("C#", "C#"), ("MYSQL", "MYSQL"),
    ("Golang", "Go"), ("TypeScript", "TypeScript"), ("Rust", "Rust"), ("Swift", "Swift"),
]

SKILL_CHOICES = [
    ("None", "Select Your Skill"),
    ("Machine Learning", "Machine Learning"), ("Deeplearning", "Deeplearning"), ("Data Science", "Data Science"),
    ("LLM", "LLM"),
    ("Prompt Engineering", "Prompt Engineering"), ("Computer Vision", "Computer Vision"), ("NLP", "NLP"),
    ("Pytorch", "Pytorch"),
    ("Tensorflow", "Tensorflow"), ("Data Engineering", "Data Engineering"), ("Kafka", "Kafka"), ("Spark", "Spark"),
    ("Airflow", "Airflow"), ("Hadoop", "Hadoop"), ("BigData", "BigData"), ("MongoDB", "MongoDB"),
    ("Crawling", "Crawling"), ("Web Development", "Web Development"), ("Spring", "Spring"), ("Node.js", "Node.js"),
    ("React", "React"), ("Redis", "Redis"), ("OS", "OS"), ("Network", "Network"),
    ("Data Structure", "Data Structure"), ("Algorithm", "Algorithm"), ("DBMS", "DBMS"), ("SQL", "SQL"),
    ("Oracle", "Oracle"), ("PostgreSQL", "PostgreSQL"), ("Android", "Android"), ("iOS", "iOS"),
    ("Flutter", "Flutter"), ("React Native", "React Native"), ("DevOps", "DevOps"), ("CI/CD", "CI/CD"),
    ("MSA", "MSA"), ("Terraform", "Terraform"), ("Docker", "Docker"), ("Kubernetes", "Kubernetes"),
    ("IaC", "IaC"), ("Cybersecurity", "Cybersecurity"), ("Reversing", "Reversing"), ("Blockchain", "Blockchain"),
    ("Unity", "Unity"), ("Unreal", "Unreal"), ("Cloud Computing", "Cloud Computing"), ("AWS", "AWS"),
    ("GCP", "GCP"), ("Azure", "Azure"), ("Git", "Git"), ("Linux", "Linux"),
    ("TDD", "TDD"), ("Embedded System", "Embedded System"), ("Computer Science", "Computer Science")
]


class CustomSignUpForm(UserCreationForm):
    user_email = forms.EmailField(required=True, label='Email')
    user_name = forms.CharField(max_length=4, required=True, label='Username')
    Language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True, label='Language')
    skill1 = forms.ChoiceField(choices=SKILL_CHOICES, required=False, label='Skill 1')
    skill2 = forms.ChoiceField(choices=SKILL_CHOICES, required=False, label='Skill 2')

    class Meta:
        model = Users
        fields = ('user_name', 'user_email', 'password1', 'password2', 'Language', 'skill1', 'skill2')

    def clean(self):
        cleaned_data = super().clean()
        language = cleaned_data.get('Language')
        skill1 = cleaned_data.get('skill1')
        skill2 = cleaned_data.get('skill2')

        if not language:
            raise forms.ValidationError("Please select a language.")

        skills = [language, skill1, skill2]
        skills = [skill for skill in skills if skill]  # 빈 문자열 제거
        if len(set(skills)) != len(skills):
            raise forms.ValidationError("Please select unique skills.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_email = self.cleaned_data['user_email']
        user.user_name = self.cleaned_data['user_name']

        skills = {}
        language = self.cleaned_data.get('Language')
        if language:
            skills[language] = 8

        for skill in ['skill1', 'skill2']:
            skill_value = self.cleaned_data.get(skill)
            if skill_value:
                skills[skill_value] = 4

        user.skills = skills

        if commit:
            user.save()
        return user
