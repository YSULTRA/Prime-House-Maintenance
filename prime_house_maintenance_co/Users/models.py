from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50, unique=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    MiddleName = models.CharField(max_length=50, null=True, blank=True)
    LastName = models.CharField(max_length=50,null=True, blank=True)
    Password = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    ContactNumber1 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)
    ContactNumber2 = models.DecimalField(max_digits=20, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.FirstName+" "+self.MiddleName+" "+self.LastName



class Property(models.Model):
    PropertyID = models.AutoField(primary_key=True)
    OwnerID = models.ForeignKey(User, on_delete=models.CASCADE)
    Description = models.TextField()
    Price = models.FloatField(null=True, blank=True)
    AvailabilityStatus = models.BooleanField()

    def __str__(self):
        return f"{self.PropertyID} {self.Description}"


class Proposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)  # ForeignKey to Property model
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True) # Add a new field called 'status'

    # Additional fields if needed

    def __str__(self):
        return f"Proposal for Property ID: {self.property_id} by User ID: {self.user_id}"

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


class Buys(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    Status = models.BooleanField(default=False)
    class Meta:
        unique_together = (('UserID', 'PropertyID'),)



class PropertyImage(models.Model):
    Property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.FileField(null=True,blank=True,upload_to='img/')  # Assumes you're storing images on the server


class Employee(models.Model):
    EmpID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=255)
    MiddleName = models.CharField(max_length=255,null=True,blank=True)
    LastName = models.CharField(max_length=255)
    ContactNumber1 = models.BigIntegerField()
    ContactNumber2 = models.BigIntegerField(null=True,blank=True)
    Ratings = models.FloatField(null=True,blank=True)
    IsAvailable = models.BooleanField()

    def __str__(self):
        return f'{self.EmpID} {self.FirstName} {self.LastName}'


class Services(models.Model):
    ServiceID = models.AutoField(primary_key=True)
    ServiceName = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.FloatField()
    image = models.FileField(null=True, blank=True, upload_to='img/')
    def __str__(self):
        return self.ServiceName


class Provides(models.Model):
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.ServiceName} - {self.employee}"



class Booking(models.Model):
    BookingID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    PropertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    ServiceID = models.ForeignKey(Services, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Date = models.DateField()
    Time = models.TimeField()
    Status = models.BooleanField()

    def __str__(self):
        return f"Booking ID: {self.BookingID}"