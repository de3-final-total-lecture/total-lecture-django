from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lecture.models import LectureInfo, Category

#강의 관련 테스트 코드

class LectureListViewTest(APITestCase):
    def setUp(self):
        self.lecture1 = LectureInfo.objects.create(
            lecture_id='L001',
            lecture_name='Test Lecture 1',
            price=1000,
            level='입문',
            platform_name='Inflearn',
            tag='Python|Django|REST',
            is_new=0,
            is_recommend=1,
        )
        self.lecture2 = LectureInfo.objects.create(
            lecture_id='L002',
            lecture_name='Test Python Lecture',
            price=2000,
            level='초급',
            platform_name='Coursera',
            tag = 'Java|Spring',
            is_new=1,
            is_recommend=0,
        )

    def test_get_lecture_list_api(self):
        response = self.client.get(reverse('lecture_list_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),2)
    
    def test_search_lecture(self):
        response = self.client.get(reverse('lecture_list_api'), {'q': 'python', 'level':'초급','sort_type':'RECENT'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_get_lecture_list_page(self): 
        response = self.client.get(reverse('lecture_list_page'))
        self.assertTemplateUsed(response, 'index.html')
        
        

class LectureDetailViewTest(APITestCase):
    def setUp(self):
        self.lecture = LectureInfo.objects.create(
            lecture_id='L003',
            lecture_name='Test Lecture 1',
            price=1000,
            level='입문',
            teacher='김영한',
            platform_name='Inflearn',
            is_new=0,
            is_recommend=1,
        )

    def test_get_lecture_detail(self):
        response = self.client.get(reverse('lecture_detail_api', kwargs={'pk': self.lecture.lecture_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['lecture_name'], self.lecture.lecture_name)

    def test_get_none_detail(self):
        response = self.client.get(reverse('lecture_detail_api', kwargs={'pk': 'L001'}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_detail_page(self):
        response = self.client.get(reverse('lecture_detail',kwargs={'pk':self.lecture.lecture_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'detail.html')
        


class CategoryListViewTest(APITestCase):
    def setUp(self):
        # 테스트용 카테고리 데이터 생성
        Category.objects.create(main_category_name="Programming", mid_category_name="Python")
        Category.objects.create(main_category_name="Programming", mid_category_name="JavaScript")
        Category.objects.create(main_category_name="Data", mid_category_name="Airflow")
        Category.objects.create(main_category_name="Data", mid_category_name="Hadoop")

    def test_get_categories(self):
        response = self.client.get(reverse('category_list_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = { "Programming": {"Python", "JavaScript"}, "Data": {"Airflow", "Hadoop"}}
        
        response_data = {
            main: set(mid)
            for main, mid in response.json().items()
        }
        
        self.assertEqual(response_data, expected_data)