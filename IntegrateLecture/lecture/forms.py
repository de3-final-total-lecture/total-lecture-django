from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

LANGUAGE_CHOICES = [
    ("None", "Language"), 
    ("Python", "Python"), ("Java", "Java"), ("JavaScript", "JavaScript"), ("HTML/CSS", "HTML/CSS"), ("Kotlin", "Kotlin"),
    ("C", "C"), ("C++","C++"), ("C#", "C#"), ("MYSQL", "MYSQL"),
    ("Golang", "Go"), ("TypeScript", "TypeScript"), ("Rust", "Rust"), ("Swift", "Swift"),
]

SKILL_CHOICES = [
    ("None", "Select Your Skill"),
    ("Machine Learning", "Machine Learning"), ("Deeplearning", "Deeplearning"), ("Data Science", "Data Science"), ("LLM", "LLM"),
    ("Prompt Engineering", "Prompt Engineering"), ("Computer Vision", "Computer Vision"), ("NLP", "NLP"), ("Pytorch", "Pytorch"),
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
    ("GCP", "GCP"), ("Azure", "Azure"), ("Git", "Git"),("Linux", "Linux"),
    ("TDD", "TDD"), ("Embedded System", "Embedded System"), ("Computer Science", "Computer Science")
]


class CustomSignUpForm(UserCreationForm):
    Language = forms.ChoiceField(choices=LANGUAGE_CHOICES, required=True, label='Language')
    skill1 = forms.ChoiceField(choices=SKILL_CHOICES, required=False, label='배우고 싶은 기술_1')
    skill2 = forms.ChoiceField(choices=SKILL_CHOICES, required=False, label='배우고 싶은 기술_2')

    class Meta:
        model = Users
        fields = ('user_email', 'user_name', 'password1', 'password2', 'Language', 'skill1', 'skill2')
        
    def clean(self):
        cleaned_data = super().clean()
        skills = [cleaned_data.get('Language'), cleaned_data.get('skill1'), cleaned_data.get('skill2')]
        skills = [skill for skill in skills if skill] # None 값 제거
        if len(set(skills)) != len(skills):
            raise forms.ValidationError("중복되지 않은 기술을 선택하세요.")
        cleaned_data['skills'] = {skill: 1 for skill in skills if skill}
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.skills = self.cleaned_data['skills']
        if commit:
            user.save()
        return user