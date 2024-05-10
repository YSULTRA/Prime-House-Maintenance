from django.db import models
from django import forms
from django.forms import inlineformset_factory

class Users(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    MiddleName = models.CharField(max_length=50, null=True, blank=True)
    LastName = models.CharField(max_length=50)
    Password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    ContactNumber1 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    ContactNumber2 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)

class Owners(models.Model):
    OwnerID = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    Username = models.CharField(max_length=255)
    FirstName = models.CharField(max_length=255, null=True, blank=True)
    MiddleName = models.CharField(max_length=255, null=True, blank=True)
    LastName = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    ContactNumber1 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    ContactNumber2 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)

class Property(models.Model):
    PropertyID = models.AutoField(primary_key=True)
    OwnerID = models.ForeignKey(Owners, on_delete=models.CASCADE)
    Description = models.TextField()
    Price = models.FloatField()
    AvailabilityStatus = models.BooleanField()

class PropertyImage(models.Model):
    Property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')  # Assumes you're storing images on the server

class Employees(models.Model):
    EmpID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=255)
    MiddleName = models.CharField(max_length=255, null=True, blank=True)
    LastName = models.CharField(max_length=255)
    ContactNumber1 = models.DecimalField(max_digits=20, decimal_places=0)
    ContactNumber2 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    Ratings = models.FloatField()
    IsAvailable = models.BooleanField()

class Location(models.Model):
    LocationID = models.AutoField(primary_key=True)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    Latitude = models.DecimalField(max_digits=10, decimal_places=8)
    Longitude = models.DecimalField(max_digits=11, decimal_places=8)
    StreetAddress = models.CharField(max_length=255)
    StreetNumber = models.CharField(max_length=20)
    LandNumber = models.CharField(max_length=20)
    State = models.CharField(max_length=100)
    ZipCode = models.CharField(max_length=20)
    Country = models.CharField(max_length=100)

class Services(models.Model):
    ServiceID = models.AutoField(primary_key=True)
    ServiceName = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.FloatField()
    EmpID = models.ForeignKey(Employees, on_delete=models.CASCADE)

class Booking(models.Model):
    BookingID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    ServiceID = models.ForeignKey(Services, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()
    Status = models.CharField(max_length=50)

class Payment(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentMethod = models.CharField(max_length=255)
    TransactionStatus = models.CharField(max_length=50)

class Rating(models.Model):
    RatingID = models.AutoField(primary_key=True)
    ServiceID = models.ForeignKey(Services, on_delete=models.CASCADE)
    Score = models.IntegerField()
    Comments = models.TextField()

class ExpertConsultation(models.Model):
    ConsultationID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    ExpertID = models.IntegerField()
    Topics = models.TextField()

class ProfessionalProfile(models.Model):
    ExpertID = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    Expertise = models.CharField(max_length=255)
    Bio = models.TextField()
    ServicesOffered = models.TextField()

class Buys(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    Status = models.CharField(max_length=50)
    class Meta:
        unique_together = (('UserID', 'PropertyID'),)

class Ownership(models.Model):
    OwnerID = models.ForeignKey(Owners, on_delete=models.CASCADE)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    LocationID = models.ForeignKey(Location, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('OwnerID', 'PropertyID', 'LocationID'),)

class Provides(models.Model):
    UserID = models.ForeignKey(Users, on_delete=models.CASCADE)
    ServiceID = models.ForeignKey(Services, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employees, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('UserID', 'ServiceID', 'EmployeeID'),)

# Form for Property Image
class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']

# Formset for Property Images
PropertyImageFormSet = inlineformset_factory(Property, PropertyImage, form=PropertyImageForm, extra=3)
