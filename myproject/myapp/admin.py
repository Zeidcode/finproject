from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from myapp.models import CustomUser, Recipe, Category


@admin.register(CustomUser)
class ClientAdmin(BaseUserAdmin):
    pass


class RecipeImageListFilter(admin.SimpleListFilter):
    title = _("Изображение")
    parameter_name = "image"

    def lookups(self, request, model_admin):
        return [
            ("yes", _("имеется")),
            ("no", _("отсутствует")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "no":
            return queryset.exclude(
                image__icontains='recipes'
            )
        if self.value() == "yes":
            return queryset.filter(
                image__icontains='recipes'
            )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'description',
                    'cooking_time',
                    'image',
                    'author',
                    'category']
    search_fields = ['title']
    search_help_text = 'Поиск рецепта по названию'
    list_filter = ['is_visible', 'author', 'category', RecipeImageListFilter, ]
    readonly_fields = ['entry_date']
    actions = ['make_hidden']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['title'],
            },
        ),
        (
            'Описание',
            {
                'classes': ['wide'],
                'description': 'Описание блюда',
                'fields': ['description', 'image'],
            },
        ),
        (
            'Способ приготовления',
            {
                'classes': ['collapse'],
                'fields': ['cooking_steps', 'cooking_time'],
            }
        ),
        (
            'Характеристика рецепта',
            {
                'fields': ['author', 'category'],
            }
        ),
    ]

    @admin.action(description="Hide recipe")
    def make_hidden(self, request, queryset):
        queryset.update(is_visible=False)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
