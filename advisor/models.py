from django.db import models

# Create your models here.
class Advisor(models.Model):

    # basic information
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email_address = models.EmailField()
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    STATE_CHOICES = (
        # tonys work area
        ("Massachusetts", "Massachusetts"),
        ("Maine", "Maine"),

    )
    state = models.CharField(max_length=200, choices=STATE_CHOICES, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profileImage/')



    # licences
    health_insurance = models.BooleanField(null=True, blank=True)
    life_insurance = models.BooleanField(null=True, blank=True)
    disability = models.BooleanField(null=True, blank=True)
    series6 = models.BooleanField(null=True, blank=True)
    series63 = models.BooleanField(null=True, blank=True)
    series65 = models.BooleanField(null=True, blank=True)
    series67 = models.BooleanField(null=True, blank=True)
    series7 = models.BooleanField(null=True, blank=True)
    sie = models.BooleanField(null=True, blank=True)
    cfp = models.BooleanField(null=True, blank=True)
    cpa = models.BooleanField(null=True, blank=True)

    # education
    school = models.CharField(max_length=200, blank=True, null=True)
    MAJORS = [
        ("Accounting", "Accounting"),
        ("Applied Business", "Applied Business"),
        ("Biomedical Marketing", "Biomedical Marketing"),
        ("Business Analytics", "Business Analytics"),
        ("Computer Information Systems", "Computer Information Systems"),
        ("Entrepreneurship & Innovation", "Entrepreneurship & Innovation"),
        ("Finance", "Finance"),
        ("Health Care Management", "Health Care Management"),
        ("Human Resources Management", "Human Resources Management"),
        ("International Business", "International Business"),
        ("Management", "Management"),
        ("Marketing", "Marketing"),
        ("Supply Chain Management", "Supply Chain Management"),
        ("Talent Management", "Talent Management"),



    ]
    major = models.CharField(max_length=200, choices=STATE_CHOICES, null=True, blank=True)
    start_date = models.CharField(max_length=200, null=True, blank=True)
    end_date = models.CharField(max_length=200, null=True, blank=True)


    # interests / hobbies
    interest1 = models.CharField(max_length=200, null=True, blank=True)
    interest2 = models.CharField(max_length=200, null=True, blank=True)
    interest3 = models.CharField(max_length=200, null=True, blank=True)