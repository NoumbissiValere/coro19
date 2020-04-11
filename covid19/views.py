from silk.models import Response as Silk
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.decorators import api_view, renderer_classes
from .estimator import estimator


# Create your views here.
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def get_json(request):
    output = estimator(request.data)
    return Response(output, status=status.HTTP_200_OK, content_type='application/json')


@api_view(['POST'])
@renderer_classes([XMLRenderer])
def get_xml(request):
    output = estimator(request.data)
    return Response(output, status=status.HTTP_200_OK, content_type='application/xml')


@api_view(['GET'])
def get_logs(request):
    output = []
    for obj in Silk.objects.all():
        method = obj.request.method
        path = obj.request.path
        status_code = obj.status_code
        time_taken = round(obj.request.time_taken)
        output.append("{0}        {1}        {2}        {3} ms".format(method,
                                                                       path,
                                                                       status_code,
                                                                       time_taken))
    return Response("\n".join(output), status.HTTP_200_OK, content_type='text/plain')
