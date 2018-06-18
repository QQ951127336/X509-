import datetime

from django.core import serializers
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import Authority
from .models import Key
from .models import CerApply
from .models import Certificate,ApplyForRevok,Revoke
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
def home(request):
    return render(request,"home.html")
@csrf_exempt
def userPage(request):
    if request.method == 'POST':
        username = request.POST['account']
        userKey = Key.objects.filter(account=username)
        userKey = userKey[0].file
        userKey = userKey.path
        urlList = userKey.split(u"\\")
        url = "/static/keys/"+urlList[-1]
        print(url)
        return render(request,'userPage.html',{'username':username,'privateKey':url})
@csrf_exempt
def registerBehavior(request):
    if request.method == 'POST':
        account = request.POST['account']
        password = request.POST['password']
        accountList = User.objects.filter(account=account)
        if(accountList.__len__() != 0):
            return HttpResponse("000")
        User.objects.create(account=account,password=password,authority=Authority.objects.get(authority=0))
        privateKey = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        with open("key.pem", "wb") as f:
            f.write(privateKey.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
            ))
        myFile = open("key.pem", "rb")
        myFile = File(myFile)
        Key.objects.create(account=account,file=myFile)
        return HttpResponse("200")
@csrf_exempt
def loginBehavior(request):
    if request.method == 'POST':
        account  = request.POST['account']
        password = request.POST['password']
        accountList = User.objects.filter(account=account)
        if(accountList.__len__() == 0):
            return HttpResponse("000")
        if(accountList[0].password != password):
            return HttpResponse("001")
        if((accountList[0].authority.__str__() == "0")):
            return HttpResponse("002")
        return HttpResponse("200")
@csrf_exempt
def applyCerBehavior(request):
    if request.method == 'POST':
        username = request.POST['username']
        country = request.POST['countryApply']
        province = request.POST['provinceApply']
        locality = request.POST['localityApply']
        organization = request.POST['organization']
        common = request.POST['common']
        dsn = request.POST['dsn']
        CerApply.objects.create(username=username,country=country,province=province,locality=locality,organization=organization,common=common,dsn=dsn,authority=Authority.objects.get(authority=0))
        return HttpResponse("200")
    else:
        return("000")
@csrf_exempt
def showApplyCerList(request):
    if request.method == 'POST':
        username = request.POST['username']
        cerApplyList = CerApply.objects.filter(username=username)
        data = serializers.serialize("json",cerApplyList)
        return HttpResponse(data)

@csrf_exempt
def getCertificate(request):
    if request.method == 'POST':
        username = request.POST['username']
        cerApplyList = CerApply.objects.filter(username=username,authority=Authority.objects.get(authority=1))

        keyList = Key.objects.filter(account=username)
        keyPath = keyList[0].file
        key = File(keyPath)
        key = serialization.load_pem_private_key(key.read(),b"passphrase",default_backend())
        serialNumber = x509.random_serial_number()
        for cerApply in cerApplyList:
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME,u"US"),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME,cerApply.province),
                x509.NameAttribute(NameOID.LOCALITY_NAME,cerApply.locality),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME,cerApply.organization),
                x509.NameAttribute(NameOID.COMMON_NAME,cerApply.common),
            ])
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                key.public_key()
            ).serial_number(
                serialNumber
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=10)
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName(cerApply.dsn)]),
                critical=False,
            ).sign(key,hashes.SHA256(),default_backend())
            with open("certificate.pem","wb") as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            tmpCertificate = open("certificate.pem","rb")
            tmpFile = File(tmpCertificate)
            Certificate.objects.create(username=username,serialNumber=serialNumber,file=tmpFile)
        cerApplyList.delete()
        return HttpResponse("200")
@csrf_exempt
def showCertificate(request):
    if request.method == "POST":
        username = request.POST["username"]
        certificateList = Certificate.objects.filter(username=username)
        data = serializers.serialize("json",certificateList)
        return HttpResponse(data)
@csrf_exempt
def applyForRevoke(request):
    if request.method == "POST":
        username = request.POST["username"]
        serialNumber = request.POST["serialNumber"]
        hasCer = Certificate.objects.filter(username=username,serialNumber=serialNumber)
        if hasCer.__len__() == 0:
            return HttpResponse("000")
        hasRevoke = ApplyForRevok.objects.filter(username=username,serialNumber=serialNumber)
        if hasRevoke.__len__() != 0:
            return HttpResponse("001")
        ApplyForRevok.objects.create(username=username,serialNumber=serialNumber,authority=Authority.objects.get(authority=0))
        return HttpResponse("200")
@csrf_exempt
def showApplyForRevokeList(request):
    if request.method == "POST":
        username = request.POST["username"]
        applyRevokeList = ApplyForRevok.objects.filter(username=username)
        data = serializers.serialize("json",applyRevokeList)
        return HttpResponse(data)
@csrf_exempt
def doRevoke(request):
    if request.method == "POST":
        username = request.POST["username"]
        applyRevokeList = ApplyForRevok.objects.filter(username=username,authority=Authority.objects.get(authority=1))
        for revokeDeal in applyRevokeList:
            Revoke.objects.create(serialNumber=revokeDeal.serialNumber)
        applyRevokeList.delete()
        return HttpResponse("200")
@csrf_exempt
def checkRevoke(request):
    if request.method == "POST":
        serialNumber = request.POST["serialNumber"]
        hasCer = Certificate.objects.filter(serialNumber=serialNumber)
        if hasCer.__len__() == 0:
            return HttpResponse("000")
        ifRevoke = Revoke.objects.filter(serialNumber=serialNumber)
        if ifRevoke.__len__() == 0:
            return HttpResponse("200")
        else:
            return HttpResponse("001")