from django import forms
#from .models import Review
# class ReviewForm(forms.Form):
#     user_name = forms.CharField(label="your name",max_length=70,error_messages={
#         "required":"must not empty",
#         "max-length":"please enter a short name!"
#         })
#     review_text = forms.CharField(label="your Feedback",max_length=200,
#                                   widget=forms.Textarea)
#     rating = forms.IntegerField(label="your rating",min_value=1,max_value=5)

# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = '__all__'
#         # exclude = ['owner_comment']
#         labels={
#             'user_name':'Your Name',
#             "review_text":"your Feedback",
#             "rating":"your Rating"
#         }
#         error_messages={
#             "user_name":{
#                 "required":"Your name must not be empty",
#                 "max-length":"please enter a short name!"
#             }
#         }
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']
        labels = {
            'user_name':"Your Name",
            "user_email":"Your Email",
            "comment_text":"your Comment",
            "rating":"Your Rating",
        }