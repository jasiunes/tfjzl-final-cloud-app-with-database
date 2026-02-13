
Kurulum / Entegrasyon (kısa):
1) Bu zip içeriğini Django projenizin köküne açın.
2) settings.py -> INSTALLED_APPS içine 'exams' ekleyin.
3) project/urls.py dosyanıza aşağıyı ekleyin:

   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('exams/', include('exams.urls', namespace='exams')),
   ]

4) Migrasyonlar:
   python manage.py makemigrations
   python manage.py migrate

5) Admin kullanıcı oluşturma (gerekirse):
   python manage.py createsuperuser

6) Admin panelden Course, Question, Choice girin.

7) Kurs detay sayfası:
   /exams/courses/<id>/

8) Formu gönderince sonuç sayfasına yönlendirilirsiniz.
