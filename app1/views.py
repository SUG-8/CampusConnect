from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, StudentForm, GuardianForm
from .models import Booking, StudentModel, GuardianModel, TimeSlot, AddOn, CourseSlot
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

# -------------------- Helper --------------------
def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

#----------------------- View All Courses ------------------------------
def all_courses(request):
    return render(request, 'all_courses.html', {})


# -------------------- Pages --------------------
def homepage(request):
    return render(request, 'homepage.html')

def college_Links(request):
    return render(request, 'college_Links.html', {})

# -------------------- Booking --------------------
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, Booking_ID=booking_id)
    return render(request, "booking_success.html", {"booking": booking})

def payment(request):
    booking_id = request.session.get('booking_id')
    addon_ids = request.session.get('addon_ids', [])

    if not booking_id:
        return redirect('openday')


    booking = Booking.objects.get(Booking_ID=booking_id)
    addons = AddOn.objects.filter(id__in=addon_ids)

    total = Decimal("0.00")
    has_lunch = any("lunch" in addon.name.lower() for addon in addons)
    has_merch = any("merch" in addon.name.lower() for addon in addons)

    for addon in addons:
        price = addon.price
        if has_lunch and "merch" in addon.name.lower():
            price *= Decimal("0.9")  # 10% discount on merch
        total += price

    total = total.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
    booking.total_price = total
    booking.save()

    if request.method == "POST":
        booking.is_paid = True
        booking.save()
        request.session.pop('booking_id', None)
        request.session.pop('addon_ids', None)
        request.session.pop('total_amount', None)
        return redirect('booking_success', booking_id=booking.Booking_ID)

    return render(request, 'payment.html', {'booking_id': booking.Booking_ID, 'addons': addons, 'total': total})

def openday(request):
    open_day_booking = None
    success = False

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            open_day_booking = form.save(commit=False)
            open_day_booking.save()
            selected_addons = form.cleaned_data.get('addons')

            if selected_addons.exists():
                request.session['booking_id'] = open_day_booking.Booking_ID
                request.session['addon_ids'] = list(selected_addons.values_list('id', flat=True))
                total = sum(addon.price for addon in selected_addons)
                request.session['total_amount'] = float(total)
                return redirect('payment')

            return redirect('booking_success', booking_id=open_day_booking.Booking_ID)
        else:
            return render(request, 'BookOpenDay.html', {'form': form, 'open_day_booking': open_day_booking, 'success': success})
    else:
        form = BookingForm()
    return render(request, 'BookOpenDay.html', {'form': form, 'open_day_booking': open_day_booking, 'success': success})

# -------------------- Student Application --------------------
def ApplyToCourse(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # Create User
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('Student_Email')

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose another.')
                return render(request, 'ApplyToCourse.html', {'form': form})

            user = User.objects.create_user(username=username, password=password, email=email)

            # Create StudentModel
            student = form.save(commit=False)
            student.username = user
            student.save()

            # Check age
            age = calculate_age(student.Student_DOB)
            if age < 18:
                return redirect(f'/GuardianSection?student_id={student.Student_ID}')

            # Auto-login
            login(request, user)
            messages.success(request, "You have successfully applied to your course!")
            return redirect('ApplicationSuccess', application_id=student.Student_ID)
    else:
        form = StudentForm()

    return render(request, 'ApplyToCourse.html', {'form': form})

# -------------------- Guardian Section --------------------
def GuardianSection(request):
    student_id = request.GET.get('student_id')  # get student ID from query
    student = get_object_or_404(StudentModel, Student_ID=student_id) if student_id else None

    if request.method == "POST":
        form = GuardianForm(request.POST)
        if form.is_valid():
            guardian = form.save(commit=False)
            if student:
                guardian.student = student
                guardian.save()
        messages.success(request, "You have successfully registered the guardian")
        return redirect('ApplicationSuccess', application_id=student.Student_ID)
    else:
        form = GuardianForm()
    return render(request, 'GuardianSection.html', {'form': form, 'student': student})





# -------------------- Student Account --------------------
@login_required
def StudentAccount(request, student_id):
    student = get_object_or_404(StudentModel, Student_ID=student_id)
    course = student.Course
    return render(request, 'StudentAccount.html', {'student': student, 'course':course})


#------------------------------ View Course ----------------------
@login_required
def view_course(request,course_id):
    course = get_object_or_404(CourseSlot, id=course_id)
    end_year = course.start_date.year + course.duration

    # Find the student who is enrolled in this course 
    student = StudentModel.objects.filter(Course=course).first()
    return render(request, 'view_course.html', {'course': course,'student': student, 'end_year':end_year})


#-------------------------- View Account -------------------------------
@login_required
def view_account(request):
    try:
        student = StudentModel.objects.get(username=request.user)
    except StudentModel.DoesNotExist:
        messages.error(request, "No student profile found for this account.")
        return redirect("ApplyToCourse")

    course = student.Course
    return render(request, 'view_account.html', {'student': student, 'course': course})

# -------------------- Login / Logout --------------------
def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            try:
                student = StudentModel.objects.get(username=user)
                return redirect('StudentAccount', student_id=student.Student_ID)

            except StudentModel.DoesNotExist:
                messages.error(request, "This user has no student profile. Please apply first.")
                return redirect('student_login')

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('student_login')

    return render(request, 'student_login.html', {})


def student_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('homepage')

# -------------------- Application Success --------------------
def ApplicationSuccess(request, application_id):
    application = get_object_or_404(StudentModel, Student_ID=application_id)
    return render(request, "ApplicationSuccess.html", {"application": application})

#----------------------------- Admin-----------------------


def Admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username") 
        password = request.POST.get("password") 
        
        user = authenticate(request, username=username, password=password) 
        if user is not None: 
            login(request, user) 
            return redirect('/admin/') # send them to Django admin 
            
        else: 
            messages.error(request, "Invalid username or password") 
        

    return render(request, "Admin_login.html",{})

#------------------------- Contact --------------------------------
def contact(request):

    return render(request, "contact.html", {})


#------------------------- Campus --------------------------------
def campus(request):

    return render(request, "campus.html", {})    

#----------------------------- About ---------------------------------
def about(request):

    return render(request, "about.html", {})  
