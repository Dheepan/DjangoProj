from django.http import HttpResponse
from Msee.models import Images
from django.core.serializers.json import Serializer, DjangoJSONEncoder
from django.utils import simplejson
import datetime
from django.utils.timezone import utc

#now = datetime.datetime.utcnow().replace(tzinfo=utc)
class MySerializer(Serializer):
    def end_serialization(self):
        cleaned_objects = []

        for obj in self.objects:
            del obj['pk']
            del obj['model']
            cleaned_objects.append(obj)

        simplejson.dump(cleaned_objects, self.stream, cls=DjangoJSONEncoder, **self.options)

   
def process(request):
    if request.method == 'GET':
        img_id=request.GET.get('id', '')
        result=get_handler(img_id)
        return HttpResponse(result['data'],status=result['status'],content_type="application/json")

def get_handler(img_id):
    template={"status":"","data":""}
    if img_id=="":
        template['status']=400 #bad request
        template['data']='''{"Result":"false","Reason":"Image id not provided"}'''
        return template
    template={"status":"","data":""}
    objects=Images.objects.filter(image_id=img_id)
    if len(objects)==0:
        template['status']=200 #ok but no result
        template['data']='''{"Result":"false","Reason":"Image not found"}'''
        return template
        
    s=MySerializer()
    temp=s.serialize(objects)
    result_list=simplejson.loads(temp)
    result=[]
    for ele in result_list:
         result.append(ele['fields'])
    res=str(result).replace("'","\"")
    template['data']='''{"Result":"true","Reason":"","ImageData":'''+res+'''}'''
    template['status']=200 #ok
    return template

