from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('UserID', 'Username', 'FirstName', 'MiddleName', 'LastName', 'Email', 'ContactNumber1', 'ContactNumber2')

admin.site.register(User, UserAdmin)



# Register the Property model
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('PropertyID', 'OwnerID', 'Description', 'Price', 'AvailabilityStatus')

admin.site.register(Property, PropertyAdmin)

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'timestamp','status')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'property__Description')  # Adjust fields as needed
admin.site.register(Proposal,ProposalAdmin)
# Register the Location model
class LocationAdmin(admin.ModelAdmin):
    list_display = ('LocationID', 'PropertyID', 'Latitude', 'Longitude', 'StreetAddress', 'StreetNumber', 'LandNumber', 'State', 'ZipCode', 'Country')

admin.site.register(Location, LocationAdmin)

# Register the Buys model
class BuysAdmin(admin.ModelAdmin):
    list_display = ('UserID', 'PropertyID', 'Status')

admin.site.register(Buys, BuysAdmin)

class PropertyImageAdmin(admin.ModelAdmin):
    list_display=('Property','image')

admin.site.register(PropertyImage,PropertyImageAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('EmpID', 'FirstName', 'MiddleName', 'LastName', 'ContactNumber1', 'ContactNumber2', 'Ratings', 'IsAvailable')

# Register the Employee model with the custom EmployeeAdmin class
admin.site.register(Employee, EmployeeAdmin)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('ServiceID', 'ServiceName', 'Description', 'Price')

# Register the Services model with the custom ServicesAdmin class
admin.site.register(Services, ServicesAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('BookingID', 'UserID', 'PropertyID', 'ServiceID','EmployeeID', 'Date', 'Time', 'Status')

# Register the Booking model with the custom BookingAdmin class
admin.site.register(Booking, BookingAdmin)


class ProvidesAdmin(admin.ModelAdmin):
    list_display = ('service', 'employee')

admin.site.register(Provides, ProvidesAdmin)