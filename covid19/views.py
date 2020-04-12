import time

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .estimator import estimator
from .models import ResponseTime


# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_json(request):
    t1 = time.time()
    output = estimator(request.data)
    resp = Response(output, status=status.HTTP_200_OK,
                    content_type='application/json')
    t2 = time.time()
    time_taken = round((t2 - t1) * 1000)
    method = request.method
    path = request.path
    status_code = resp.status_code
    ResponseTime.objects.create(
        method=method,
        path=path,
        status_code=status_code,
        time_taken=time_taken)
    return resp


@api_view(['POST'])
@renderer_classes([XMLRenderer])
def get_xml(request):
    t1 = time.time()
    output = estimator(request.data)
    resp = Response(output, status=status.HTTP_200_OK,
                    content_type='application/xml')
    t2 = time.time()
    time_taken = round((t2 - t1) * 1000)
    method = request.method
    path = request.path
    status_code = resp.status_code
    ResponseTime.objects.create(
        method=method,
        path=path,
        status_code=status_code,
        time_taken=time_taken)
    return resp


@api_view(['GET'])
def get_logs(request):
    output = ""
    for obj in ResponseTime.objects.all():
        output += "{}\t\t{}\t\t{}\t\t{:02d}ms\n".format(obj.method,
                                                        obj.path,
                                                        obj.status_code,
                                                        obj.time_taken)
    return HttpResponse(output, status=status.HTTP_200_OK, content_type='text/plain')
