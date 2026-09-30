from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SingletonBase, TimeStampedModel, SEOModel


admin.site.site_header = 'KISA Shop — Админ-панель'
admin.site.site_title = 'KISA Shop'
admin.site.index_title = 'Управление магазином'