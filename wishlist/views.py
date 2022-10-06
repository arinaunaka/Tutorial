from django.shortcuts import render, redirect
from wishlist.models import BarangWishlist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse

@login_required(login_url='/wishlist/login/')
def show_wishlist(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Arina Aunaka',
    'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist.html", context)

def show_xml(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = BarangWishlist.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = BarangWishlist.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Akun telah berhasil dibuat!')
            return redirect('wishlist:login')
    
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("wishlist:show_wishlist"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('wishlist:login'))
    response.delete_cookie('last_login')
    return response

def wishlist_ajax(request):
    data_barang_wishlist = BarangWishlist.objects.all()
    context = {
    'list_barang': data_barang_wishlist,
    'nama': 'Arina Aunaka',
    'last_login': request.COOKIES['last_login'],
    }
    return render(request, "wishlist_ajax.html", context)

def submit_wishlist_ajax(request):
    if request.is_ajax and request.method == "POST":
        nama = request.POST.get('nama_barang')
        harga = request.POST.get('harga_barang')
        deskripsi = request.POST.get('deskripsi_barang')

        if nama != "" and harga != "" and deskripsi != "":
            barang = BarangWishlist(nama_barang = nama, harga_barang = harga, deskripsi = deskripsi)
            barang.save()
            ser_barang = serializers.serialize('json', [ barang, ])
            return JsonResponse({"barang": ser_barang}, status=200)

    return JsonResponse({"error": ""}, status=400)