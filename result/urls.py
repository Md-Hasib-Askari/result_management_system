from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import add_result, view_results, student_marksheet_view, generate_reports

urlpatterns = [
    path('add/', add_result, name='add_result'),
    path('view/', view_results, name='view_results'),
    path('view/<int:student_id>/', student_marksheet_view, name='student_marksheet'),
    path('generate_pdf/<str:section>/', generate_reports, name='generate_report')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)