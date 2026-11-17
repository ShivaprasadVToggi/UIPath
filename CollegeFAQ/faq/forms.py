from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'category']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the question...',
            }),
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter the answer...',
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_question(self):
        q = self.cleaned_data.get('question', '').strip()
        if not q:
            raise forms.ValidationError("Question cannot be empty.")
        return q

    def clean_answer(self):
        a = self.cleaned_data.get('answer', '').strip()
        if not a:
            raise forms.ValidationError("Answer cannot be empty.")
        return a
