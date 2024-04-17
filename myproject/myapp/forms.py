from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import CustomUser, Category, Recipe


class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=100,
                            label="Наименование блюда",
                            widget=forms.TextInput(attrs={'class': 'recipe-form__title'}))
    description = forms.CharField(max_length=250,
                                  label="Описание блюда",
                                  widget=forms.Textarea(attrs={'class': 'recipe-form__description'}))
    cooking_steps = forms.CharField(max_length=10000,
                                    label="Как приготовить",
                                    widget=forms.Textarea(attrs={'class': 'recipe-form__cooking'}))
    cooking_time = forms.TimeField(label="Время приготовления",
                                   help_text='Укажите время приготовления блюда',
                                   widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}))
    image = forms.ImageField(required=False, label="Изображение блюда")

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'cooking_steps', 'cooking_time', 'image', 'category')

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget = forms.Select()
        self.fields['category'].queryset = Category.objects.only('title').all()
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['category'].label = 'Категория блюда'
        self.fields['category'].required = False


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'placeholder': 'Пароль'}),
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Имя'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Пароль'
        self.fields['password1'].widget.attrs[
            'title'] = 'Минимум 8 символов. По одному из: заглавная и строчная буква, цифра и спецсимвол.'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email
