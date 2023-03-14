from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from app.models import UploadedFile
import pandas as pd
import openpyxl
import csv


@login_required
def admin_panel(request):
    uploaded_files = UploadedFile.objects.all()
    return render(request, 'admin_panel.html', {'uploaded_files': uploaded_files})


   
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_panel')
    return render(request, 'login.html')


@login_required
def admin_panel(request):
    uploaded_files = UploadedFile.objects.all()
    return render(request, 'admin_panel.html', {'uploaded_files': uploaded_files})



@login_required
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        new_file = UploadedFile(file=uploaded_file)
        new_file.save()
        return redirect('admin_panel')
    return render(request, 'upload_file.html')




@login_required
def open_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_extension = uploaded_file.get_file_extension()
    file_path = uploaded_file.file.path
    if file_extension == '.csv':
        df = pd.read_csv(file_path)
    elif file_extension == '.xlsx':
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        df = pd.DataFrame(sheet.values)
    else:
        return HttpResponse("Unsupported file type")
    return render(request, 'file_data.html', {'data': df.to_html()})
    



@login_required
def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    file_path = uploaded_file.file.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        return response

