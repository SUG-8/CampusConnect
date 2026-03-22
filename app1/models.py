from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from datetime import date


# this class manages the add ons which is admin managed
class AddOn(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (£{self.price})"

class CourseSlot(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    duration = models.PositiveSmallIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} course duration: {self.duration} years"
        


#this class will allow for admin controlled time slots
class TimeSlot(models.Model):
    time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["time"]

    def __str__(self):
        return self.time.strftime("%H:%M")

#this class will allow for admin controlled date slots
class AvailableDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime("%d %b %Y").upper()



class Booking(models.Model):
#the group size is a dropdown because, it is the easiest way to make sure that users won't select higher groups
#the maximum group size will be stated on the site
    Group_Size=[
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
    ]

#these have been placed as placeholders for potetial campuses for Riverview.
    Campus=[
        ("Campus 1", "Campus 1"),
        ("Campus 2", "Campus 2"),
        ("Campus 3", "Campus 3"),
    ]

    Needs=[
        ("Accessibility accommodations", "Accessibility accommodations: ramps, elevators, seating."),
        ("Food and dietery options","Food and dietary options: vegetarian, vegan, halal, kosher, or allergy-aware refreshments."),
        ("N/A",'N/A')

    ]

    Booking_ID=models.AutoField(primary_key=True)
    Booking_Name= models.CharField(max_length=30)
    # Time dropdown controlled by admin
    Booking_Time = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE
    )

    Booking_email= models.EmailField(
        max_length=254,
        )

    Booking_Date= models.ForeignKey(
        AvailableDate, 
        on_delete=models.PROTECT)
     
    Booking_Party_Size=models.CharField(max_length=5, choices=Group_Size, default="1") #drop down, so that the maximum group size isn’t surpassed)
    Booking_Location=models.CharField(max_length=10, choices=Campus, default="Campus 1") #dropdown with all the campuses
    Booking_Additional_Needs=models.CharField(max_length=50, choices= Needs, default="N/A"
    )

    #addons FK
    addons = models.ManyToManyField(AddOn, blank=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.Booking_Name} - {self.Booking_Date}"





#the StudentModel contains all information regarding the student, which will be otained when they apply for a course
class StudentModel(models.Model):

    Student_ID = models.AutoField(primary_key=True)


    Student_Name = models.CharField(max_length=50)
    Student_Surname = models.CharField(max_length=50)

    username= models.OneToOneField(User,on_delete=models.CASCADE)

    Student_Address = models.TextField()

    Student_Email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    Student_Number = models.CharField(max_length=15)

    Student_DOB = models.DateField()

    Course = models.ForeignKey(
        CourseSlot,
        on_delete=models.CASCADE
    )

    Student_Age = models.PositiveIntegerField(editable=False)

    #this validates whether the age corrisponds with the DOB given 
    def save(self, *args, **kwargs):
        if self.Student_DOB:
            today = date.today()
            self.Student_Age = (
                today.year - self.Student_DOB.year
                - ((today.month, today.day) < (self.Student_DOB.month, self.Student_DOB.day))
            )
        else:
            self.Student_Age = None

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.Student_Name} {self.Student_Surname}"

     
#the GuardianModel contains all information regarding the student's guardian, which will be otained when they apply for a course
class GuardianModel(models.Model):

    RELATIONSHIP_CHOICES = [
        ("mother", "Mother"),
        ("father", "Father"),
        ("legal_guardian", "Legal Guardian"),
        ("step_parent", "Step Parent"),
        ("foster_parent", "Foster Parent"),
        
    ]

    Guardian_ID = models.AutoField(primary_key=True)

    Guardian_Name = models.CharField(max_length=50)
    Guardian_Surname = models.CharField(max_length=50)

    Guardian_Address = models.TextField()

    Guardian_Number = models.CharField(max_length=15)

    Guardian_Email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    Guardian_Relationship_to_student = models.CharField(
        max_length=20,
        choices=RELATIONSHIP_CHOICES
    )

    student = models.ForeignKey(
    StudentModel,
    on_delete=models.CASCADE,
    related_name="guardians",
    null=True,
    blank=True
)



    def __str__(self):
        return f"{self.Guardian_Name} {self.Guardian_Surname}"




