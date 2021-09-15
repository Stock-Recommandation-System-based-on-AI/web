from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': "글 제목을 입력해주세요",
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder':"이렇게 예측하신 이유를 작성해주세요",
            }
        )
    )
    position = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'list': 'position-list',
                'autocomplete': 'off',

            }
        )
    )
    stock = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'list': 'stock-list',
            }
        )
    )
    price = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    class Meta:
        model = Post
        fields = ("title", "stock", "content", "position", "predict_date", "price")
