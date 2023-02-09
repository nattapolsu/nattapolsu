from django.shortcuts import render, redirect
from django.core.mail import send_mail
from onsite.models import Contact, Course

# Create your views here.
def TrainingPage(request):
    all_course = Course.objects.all()
    return render(request,"training.html",{"courses":all_course})

def AddCourse(request):
    if request.method == 'POST':
        course_code = request.POST["course_code"]
        course_name = request.POST["course_name"]
        course_days = request.POST["course_days"]
        course_fee = request.POST["course_fee"]
        course_date = request.POST["course_date"]

        course = Course.objects.create(
            course_code = course_code,
            course_name = course_name,
            course_days = course_days,
            course_fee = course_fee,
            course_date = course_date 
        )
        course.save()
        return redirect("training-page")
    else:
        return render(request,"addcourse.html")

def EditForm(request,course_id):
    course = Course.objects.get(id = course_id)
    if request.method == "POST":
        course.course_code = request.POST["course_code"]
        course.course_name = request.POST["course_name"]
        course.course_days = request.POST["course_days"]
        course.course_fee = request.POST["course_fee"]
        course.course_date = request.POST["course_date"]
        course.save()
        return redirect("training-page")

    else:
        course = Course.objects.get(id = course_id)
        return render(request,"editCourse.html",{"course":course})

def DeleteForm(request,course_id):
    course = Course.objects.get(id = course_id)
    course.delete()
    return redirect("training-page")

def FormPage(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        position = request.POST.get('position')
        cusemail = request.POST.get('cusemail')
        phone = request.POST.get('phone')
        fax = request.POST.get('fax')
        concompany = request.POST.get('con-company')
        conaddress = request.POST.get('con-address')
        numtax = request.POST.get('numtax')
        concontact = request.POST.get('con-contact')
        title = request.POST.get('title')
        conphone = request.POST.get('con-phone')
        concusemail = request.POST.get('con-cusemail')
        confax = request.POST.get('con-fax')
        reqtraincourse = request.POST.get('req-train-course')
        nunpartic = request.POST.get('nun-partic')
        datetrain = request.POST.get('date-train')
        addcouse1 = request.POST.get('addcouse1')
        adddate1 = request.POST.get('adddate1')
        addcouse2 = request.POST.get('addcouse2')
        adddate2 = request.POST.get('adddate2')

        newcontact = Contact()
        newcontact.company = company
        newcontact.address = address
        newcontact.position = position
        newcontact.cusemail = cusemail
        newcontact.date = datetrain
        newcontact.save()

        data = {
            'company' : company,
            'address' : address,
            'contact' : contact,
            'position': position,
            'phone' : phone,
            'cusemail':  cusemail,
            'fax' : fax,
            'con-company' : concompany,
            'con-address' : conaddress,
            'numtax' : numtax,
            'con-contact' : concontact,
            'title' : title,
            'con-phone' : conphone,
            'con-cusemail' : concusemail,
            'con-fax' : confax,
            'req-train-course' : reqtraincourse,
            'nun-partic' : nunpartic,
            'date-train' : datetrain,
            'addcouse1' : addcouse1,
            'adddate1' : adddate1,
            'addcouse2': addcouse2,
            'adddate2' : adddate2,


        }
        body = '''
        Company :{}
        Address :{}  
        Contact :{}     Position :{}     
        Phone :{}       Email :{}       Fax :{}
        
        Billing to:
        (ออกใบเสร็จรับเงินให้)
        Company: {}
        Address: {}
        Tax id: {}      Contact: {}     Title: {}
        Phone :{}       Email :{}       Fax :{}

        Request for training course :
        (ระบุหลักสูตรที่ต้องการ)    {}
        The number of participants: {}      Required date of training: {}
        Request for other courses ระบุหลักสูตรอื่นๆ (หากมี):
        1.Course 1  {}                    Required date: {}
        2.Course 2  {}                    Required date: {}
        '''.format(data['company'],data['address'],data['contact'],data['position'],data['phone'],
        data['cusemail'],data['fax'],data['con-company'],data['con-address'],data['numtax'],data['con-contact'],
        data['title'],data['con-phone'],data['con-cusemail'],data['con-fax'],data['req-train-course'],
        data['nun-partic'],data['date-train'],data['addcouse1'],data['adddate1'],data['addcouse2'],data['adddate2'])

        send_mail('Contact Form',body, '', [cusemail])#('subject',เนื้อหา,อีเมลล์ที่ส่ง)
    return render(request, "form.html")


def courseRegistration(request):
    all_contact = Contact.objects.all()
    context = {'all_contact':all_contact}
    return render(request,"onsite_course_registration.html",context)

def contactEdit(request,contact_id):
    contact = Contact.objects.get(id = contact_id)
    if request.method == "POST":
        contact.company = request.POST["company"]
        contact.address = request.POST["address"]
        contact.position = request.POST["position"]
        contact.cusemail = request.POST["cusemail"]
        contact.save()
        return redirect('courseRegistration')

    else:
        contact = Contact.objects.get(id = contact_id)
        return render(request,"editRegisCourse.html",{"contact":contact})

def contactDelete(request,contact_id):
    contact = Contact.objects.get(id = contact_id)
    contact.delete()
    return redirect('courseRegistration')