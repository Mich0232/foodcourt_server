from django import forms

from .models import RecipeComment

COMMENT_RATINGS = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5)
)


class CommentForm(forms.Form):
    content = forms.CharField(max_length=2000, required=True)
    rating = forms.ChoiceField(choices=COMMENT_RATINGS)

    def clean_content(self):
        content = self.cleaned_data['content']
        if content == '':
            raise forms.ValidationError("Comment content not defined")
        return content
