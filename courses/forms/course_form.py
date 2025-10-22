from django import forms



class CourseForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':"border border-gray-300 rounded-md p-2 w-full"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':"border border-gray-300 rounded-md p-2 w-full"}))