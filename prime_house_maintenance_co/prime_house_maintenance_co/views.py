from django.http import HttpResponse
from django.shortcuts import render, redirect
from Users.models import *
from django.contrib import messages
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone

def homePage(request):
    numbers = range(9)
    # property = Property.objects.all()s
    # Check if the user is logged in
    prop = Property.objects.filter(AvailabilityStatus=True)

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=user_id)
        prop = Property.objects.filter(AvailabilityStatus=True)

        return render(request, 'homepage.html', {'user': user, 'property':prop,'numbers':numbers})
    elif prop:
        return render(request, 'homepage.html', {'numbers': numbers,'property':prop})
    else:
        return render(request,'homepage.html', {'numbers': numbers})

def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstName')
        Username = request.POST.get('username')
        middlename = request.POST.get('middleName')
        lastname = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        contact1 = request.POST.get('contact1')
        contact2 = request.POST.get('contact2')
        try:
            contact1 = Decimal(contact1) if contact1 else None
        except InvalidOperation:
            contact1 = None

        try:
            contact2 = Decimal(contact2) if contact2 else None
        except InvalidOperation:
            contact2 = None

        user = User(FirstName=firstname, Username=Username, MiddleName=middlename, LastName=lastname,
                     Email=email, Password=password, ContactNumber1=contact1, ContactNumber2=contact2)
        user.save()
        messages.success(request, 'Successfully registered!')
        return redirect('login')
    return render(request, 'register.html')


def adminPortal(request):
    if 'admin_logged_in' in request.session:
        admin_logged_in = request.session['admin_logged_in']
        if admin_logged_in:
            return redirect('/admin/')


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user is an admin
        if email == 'admin@email.com' and password == 'admin':
            # Set a flag in session to indicate admin login
            request.session['admin_logged_in'] = True
            messages.success(request, 'Admin login successful!')
            return redirect('admin-portal')  # Redirect to admin dashboard
        else:
            try:
                user = User.objects.get(Email=email, Password=password)
                # Store user id in session to indicate user is logged in
                request.session['user_id'] = user.UserID
                messages.success(request, 'Login successful!')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
    return render(request, 'login.html')

def logoutUser(request):
    # Clear the user id from the session to indicate user logout
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, "Log Out Successful!")
    return redirect('home')


def privacyPolicy(request):
  return render(request,'privacypolicy.html')

def termsCondition(request):
  return render(request,'termscondition.html')

def listProperty(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(UserID=user_id)
    if request.method == "POST":
        # Extract user ID from session
        if user_id:
            try:
                # Extract property information from the form
                description = request.POST.get('description')
                price = request.POST.get('price')
                availability = request.POST.get('availability')
                street_address = request.POST.get('streetAddress')
                street_number = request.POST.get('streetNumber')
                land_number = request.POST.get('landNumber')
                state = request.POST.get('state')
                zip_code = request.POST.get('zipCode')
                country = request.POST.get('country')
                images = request.FILES.getlist('images')
                latitude = request.POST.get('latitude')
                longitude= request.POST.get('longitude')

                if price == '':
                    price = 0

                if availability == '0':
                    availability=False
                else:
                    availability=True

                # Create Property object with the owner instance
                property_obj = Property.objects.create(
                    OwnerID=user,
                    Description=description,
                    Price=price,
                    AvailabilityStatus=availability

                    # Add more fields as needed
                )

                # Create Location object
                location_obj = Location.objects.create(
                    PropertyID=property_obj,
                    StreetAddress=street_address,
                    StreetNumber=street_number,
                    LandNumber=land_number,
                    State=state,
                    ZipCode=zip_code,
                    Country=country,
                    Longitude=longitude,
                    Latitude=latitude
                    # Add more fields as needed
                )

                # Create PropertyImage objects for each uploaded image
                for image in images:
                    PropertyImage.objects.create(
                        Property=property_obj,
                        image = image
                    )

                messages.success(request, 'Property listed successfully!')
                return redirect('home')  # Redirect to home page after successful submission

            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
                return redirect('home')  # Redirect to home page if user does not exist
        else:
            messages.error(request, 'User not logged in.')
            return redirect('login')  # Redirect to login page if user is not logged in

    return render(request, 'property_upload.html',{'user':user,'user_id':user_id})

def propertyPage(request, pk):
    # Retrieve property information
    try:
        property_ = Property.objects.get(PropertyID=pk)
        location = Location.objects.filter(PropertyID=pk).first()
        all_properties = Property.objects.exclude(PropertyID=pk).order_by('?')[:3]
    except Property.DoesNotExist:
        return redirect('home')  # Redirect to home page if property does not exist

    if request.method == 'POST':
        if 'user_id' in request.session:
            user_id = request.session['user_id']
            user = User.objects.get(UserID=user_id)

            # Create a proposal object
            Proposal.objects.create(user=user, property_id=pk,)

            return HttpResponse('Proposal saved successfully')
        else:
            return HttpResponse('User not logged in')  # Handle case where user is not logged in

    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=user_id)

        # Check if a proposal exists for the current user and property ID
        proposal_sent = Proposal.objects.filter(user=user, property_id=pk).exists()

        return render(request, 'property_page.html', {
            'user_id': user_id,
            'user': user,
            'property': property_,
            'location': location,
            'all': all_properties,
            'proposal_sent': proposal_sent  # Pass this variable to the template
        })

    return render(request, 'property_page.html', {
        'property': property_,
        'location': location,
        'all': all_properties
    })


def updateOwnership(request,user_id,property_id):
    if request.method == "POST":
        if 'user_id' in request.session:

            user = User.objects.get(UserID=user_id)

            # Update ownership of the property
            property = Property.objects.get(PropertyID=property_id)
            oldid= property.OwnerID.UserID
            property.OwnerID =user
            property.AvailabilityStatus=False
            property.save()

            # Create entry in Buys model
            buys=Buys(UserID=user,PropertyID=property,Status=True)
            buys.save()
            # Remove proposal entry for this property
            Proposal.objects.filter(property=property).delete()

            messages.success(request, "Property Ownership Updated Successfully")
            return redirect('profile-page', pk=oldid)
        else:
            return redirect('home')

    elif 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=pk)

        # Filter properties owned by the user
        properties = Property.objects.filter(OwnerID=user)

        # Filter proposals related to the properties owned by the user
        myPropertyProposals = Proposal.objects.filter(property__in=properties)

        # Filter proposals sent by someone to the user
        proposals_received = Proposal.objects.filter(property__in=properties).exclude(user=user)

        # Filter proposals sent by the user to someone else
        proposals_sent = Proposal.objects.filter(user=user)

        return render(request, 'profile_page.html', {'user_id': user_id, 'user': user, 'proposals_received': proposals_received, 'proposals_sent': proposals_sent, 'myPropertyProposals': myPropertyProposals, 'properties': properties})

def cancel_proposal(request, property_id, user_id):
    if request.method == 'POST':
        # Verify that the user initiating the cancellation is the logged-in user
        property_id_=Property.objects.get(PropertyID=property_id)
        old_id = property_id_.OwnerID.UserID
        if 'user_id' in request.session and request.session['user_id'] == old_id:
            # Get the proposal, ensuring it exists and belongs to the current user and specified property
            user=User.objects.get(UserID=user_id)
            proposal = Proposal.objects.get(property=property_id, user=user_id)
            proposal.delete()
            messages.success(request, "The proposal has been successfully cancelled.")
        else:
            messages.error(request, "You do not have permission to cancel this proposal.")

        return redirect('profile-page', pk=old_id)
    else:
        messages.error(request, "Invalid request method.")
        return redirect('home')


def showProfilePage(request, pk):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=pk)

        # Filter properties owned by the user
        properties = Property.objects.filter(OwnerID=user)

        # Filter proposals related to the properties owned by the user
        myPropertyProposals = Proposal.objects.filter(property__in=properties)

        # Filter proposals sent by someone to the user
        proposals_received = Proposal.objects.filter(property__in=properties).exclude(user=user)

        # Filter proposals sent by the user to someone else
        proposals_sent = Proposal.objects.filter(user=user)

        # Filter bookings associated with the user
        bookings = Booking.objects.filter(UserID=user)

        return render(request, 'profile_page.html', {'user_id': user_id, 'user': user, 'proposals_received': proposals_received, 'proposals_sent': proposals_sent, 'myPropertyProposals': myPropertyProposals, 'properties': properties, 'bookings': bookings})


def removeFromSale(request,user_id,property_id):
    if request.method == "POST":
        property=Property.objects.get(PropertyID=property_id)
        property.AvailabilityStatus=False
        property.save()
        messages.success(request,"Property Remove From Sale!")
        return redirect('profile-page',pk=user_id)



def putonSaleProperty(request,user_id,property_id):
    if request.method == "POST":
        property=Property.objects.get(PropertyID=property_id)
        property.AvailabilityStatus=True
        property.save()
        messages.success(request,"Property Put on Sale!")
        return redirect('profile-page',pk=user_id)


def updateProperty(request, property_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(UserID=user_id)
    if request.method == "POST":
        if user_id:
            try:
                # Get the property object to update
                property_obj = Property.objects.get(PropertyID=property_id)

                # Check if the logged-in user is the owner of the property
                if property_obj.OwnerID.UserID == user_id:
                    # Extract updated property information from the form
                    description = request.POST.get('description')
                    price = request.POST.get('price')
                    availability = request.POST.get('availability')
                    street_address = request.POST.get('streetAddress')
                    street_number = request.POST.get('streetNumber')
                    land_number = request.POST.get('landNumber')
                    state = request.POST.get('state')
                    zip_code = request.POST.get('zipCode')
                    country = request.POST.get('country')
                    images = request.FILES.getlist('images')
                    latitude = request.POST.get('latitude')
                    longitude = request.POST.get('longitude')

                    # Update property object fields
                    property_obj.Description = description
                    property_obj.Price = price
                    property_obj.AvailabilityStatus = bool(availability)
                    property_obj.save()

                    # Update location object fields
                    location_obj = Location.objects.get(PropertyID=property_id)
                    location_obj.StreetAddress = street_address
                    location_obj.StreetNumber = street_number
                    location_obj.LandNumber = land_number
                    location_obj.State = state
                    location_obj.ZipCode = zip_code
                    location_obj.Country = country
                    location_obj.Longitude = longitude
                    location_obj.Latitude = latitude
                    location_obj.save()

                    # Delete existing property images


                    # Create new PropertyImage objects for each uploaded image
                    for image in images:
                        PropertyImage.objects.create(
                            Property=property_obj,
                            image=image
                        )
                    messages.success(request, 'Property updated successfully!')
                    return redirect('home')  # Redirect to home page after successful

                else:
                    messages.error(request, 'You are not authorized to update this property.')
                    return redirect('home')

            except Property.DoesNotExist:
                messages.error(request, 'Property does not exist.')
                return redirect('home')  # Redirect to home page if property does not exist
        else:
            messages.error(request, 'User not logged in.')
            return redirect('login')  # Redirect to login page if user is not logged in

    # Fetch property details to pre-fill the update form
    try:
        property_obj = Property.objects.get(PropertyID=property_id)
        location_obj = Location.objects.get(PropertyID=property_id)
        return render(request, 'property_update.html', {'user': user, 'user_id': user_id, 'property_obj': property_obj, 'location_obj': location_obj})

    except Property.DoesNotExist:
        messages.error(request, 'Property does not exist.')
        return redirect('home')  # Redirect to home page if property does not exist



def deleteProperty(request,user_id,property_id):
    if request.method == "POST":
        property = Property.objects.get(PropertyID=property_id)
        property.delete()
        messages.success(request,"Property Deleted Successfully!")
        return redirect('profile-page',pk=user_id)



def showServices(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=user_id)
        services = Services.objects.all()
        return render(request,'services.html',{'user':user,'services':services})
    else:
        services = Services.objects.all()
        return render(request,'services.html',{'services':services})

def servicePage(request,pk):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=user_id)
        services = Services.objects.get(ServiceID=pk)
        return render(request,'service_detail.html',{'user':user,'user_log':True,'services':services})
    else:
        services = Services.objects.get(ServiceID=pk)
        return render(request,'service_detail.html',{'services':services,'user_log':False})




def bookService(request, sk):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(UserID=user_id)
        myproperties = Property.objects.filter(OwnerID=user)

        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            property_id = request.POST.get('property_id')
            date = request.POST.get('date')
            time = request.POST.get('time')

            date_time = timezone.datetime.combine(timezone.datetime.strptime(date, '%Y-%m-%d'), timezone.datetime.strptime(time, '%H:%M').time())

            property_instance = Property.objects.get(PropertyID=property_id)

            # Get all available employees for the service
            available_employees = Provides.objects.filter(service=sk)
            for employee_provides in available_employees:
                employee = employee_provides.employee
                # Check if the employee is available at the requested date and time and not already booked
                if not Booking.objects.filter(Date=date_time.date(), Time=date_time.time(), EmployeeID=employee).exists():
                    # Create booking and mark the employee as unavailable
                    booking = Booking.objects.create(
                        UserID=user,
                        PropertyID=property_instance,
                        ServiceID=Services.objects.get(ServiceID=sk),
                        EmployeeID=employee,
                        Date=date_time.date(),
                        Time=date_time.time(),
                        Status=True
                    )
                    employee.IsAvailable = False
                    employee.save()

                    messages.success(request, 'Booking successful!')
                    return redirect('service-page', pk=sk)

            # If no available employee is found at the specified date and time or already booked
            messages.warning(request, 'No available employee for this service at the specified date and time or already booked.')
            return redirect('service-page', pk=sk)

        return render(request, 'booking.html', {'user': user, 'myproperties': myproperties, 'sk': sk})
    else:
        return render(request, 'booking.html')