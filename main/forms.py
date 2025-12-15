from django import forms
from .models import Product, SkinAnalysis, MpesaPayment, UserProfile, Order, OrderItem, ForumPost, ForumComment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = SkinAnalysis
        fields = ['image']
        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total_price', 'paid']

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content']
        

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Write your comment...',
                'class': 'form-control'
            }),
        }




class MpesaPaymentForm(forms.ModelForm):
    class Meta:
        model = MpesaPayment
        fields = ['phone_number', 'amount']