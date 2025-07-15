from django.urls import path
from . import views

urlpatterns = [
    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    
    # Department About URLs
    path('departments/<int:department_id>/about/', views.department_about_list, name='department_about_list'),
    path('about/<int:pk>/', views.department_about_detail, name='department_about_detail'),
    
    # Number Data URLs
    path('departments/<int:department_id>/numbers/', views.number_data_list, name='number_data_list'),
    path('numbers/<int:pk>/', views.number_data_detail, name='number_data_detail'),
    
    # Quick Links URLs
    path('departments/<int:department_id>/quick-links/', views.quick_links_list, name='quick_links_list'),
    path('quick-links/<int:pk>/', views.quick_link_detail, name='quick_link_detail'),
    
    # Programs URLs
    path('departments/<int:department_id>/programs/', views.programs_list, name='programs_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    
    # Curriculum URLs
    path('departments/<int:department_id>/curriculum/', views.curriculum_list, name='curriculum_list'),
    path('curriculum/<int:pk>/', views.curriculum_detail, name='curriculum_detail'),
    
    # Benefits URLs
    path('departments/<int:department_id>/benefits/', views.benefits_list, name='benefits_list'),
    path('benefits/<int:pk>/', views.benefit_detail, name='benefit_detail'),
    
    # Contact URLs
    path('contacts/', views.department_contact_list, name='contact_list'),
    path('contacts/<int:pk>/', views.contact_detail, name='contact_detail'),
    
    # CTA URLs
    path('departments/<int:department_id>/ctas/', views.cta_list, name='cta_list'),
    path('ctas/<int:pk>/', views.cta_detail, name='cta_detail'),
    
    # PO-PSO-PEO URLs
    path('departments/<int:department_id>/popsopeo/', views.popsopeo_list, name='popsopeo_list'),
    path('popsopeo/<int:pk>/', views.popsopeo_detail, name='popsopeo_detail'),
    
    # Facilities URLs
    path('departments/<int:department_id>/facilities/', views.facilities_list, name='facilities_list'),
    path('facilities/<int:pk>/', views.facility_detail, name='facility_detail'),
    
    # Banner URLs
    path('departments/<int:department_id>/banners/', views.banners_list, name='banners_list'),
    path('banners/<int:pk>/', views.banner_detail, name='banner_detail'),
] 