from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator
from .models import Booking, StudentModel, GuardianModel, TimeSlot, AddOn





# -------------------------
# Booking Form (for Open Day / event booking)
# -------------------------
class BookingForm(forms.ModelForm):
    
    addons = forms.ModelMultipleChoiceField(
        queryset=AddOn.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Booking
        fields = [
            "Booking_Name",
            "Booking_email",
            "Booking_Date",
            "Booking_Time",
            "Booking_Party_Size",
            "Booking_Location",
            "Booking_Additional_Needs",
            "addons"
        ]

        widgets = {
            "Booking_Name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "Booking_email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "Booking_Date": forms.Select(),
            "Booking_Time": forms.Select(),  # Dropdown, admin-managed
            "Booking_Party_Size": forms.Select(),  # Dropdown from Group_Size
            "Booking_Location": forms.Select(),  # Dropdown from Campus
            "Booking_Additional_Needs": forms.Select(),  # Dropdown from Needs
        }



# -------------------------
# Student Form
# -------------------------
class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = StudentModel
        fields = [
            "Student_Name",
            "Student_Surname",
            "Student_Address",
            "Student_Email",
            "Student_Number",
            "Student_DOB",
            "Course"
        ]

        widgets = {
            "Student_Name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "Student_Surname": forms.TextInput(attrs={"placeholder": "Surname"}),
            "Student_Address": forms.Textarea(attrs={"rows": 3, "placeholder": "Address"}),
            "Student_Email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "Student_Number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "Student_DOB": forms.DateInput(attrs={"type": "date"}),
            "Course": forms.Select()
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    # Age will be calculated automatically in the model's save() method

# -------------------------
# Guardian Form
# -------------------------
class GuardianForm(forms.ModelForm):
    class Meta:
        model = GuardianModel
        fields = [
            "Guardian_Name",
            "Guardian_Surname",
            "Guardian_Address",
            "Guardian_Number",
            "Guardian_Email",
            "Guardian_Relationship_to_student",
        ]

        widgets = {
            "Guardian_Name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "Guardian_Surname": forms.TextInput(attrs={"placeholder": "Surname"}),
            "Guardian_Address": forms.Textarea(attrs={"rows": 3, "placeholder": "Address"}),
            "Guardian_Number": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "Guardian_Email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "Guardian_Relationship_to_student": forms.Select(),  # Dropdown for legal relationship
        }

#REGRISTRATION FORM, INCLUDES ALL FIELDS NEEDED FOR USER REGRISTRATION
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name= forms.TextInput(attrs={'class': 'form-control'}),
    last_name = forms.TextInput(attrs={'class': 'form-control'}),

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

