import random
from django.contrib.auth.backends import ModelBackend

def generate_random_number(model, field,length=10):
    ref_no = str(random.randint(10 ** (length - 1), (10 ** length) - 1)).zfill(length)
    if model.objects.values(field).filter(**{field: ref_no}):
        return generate_random_number(model, field, length)
    return ref_no


def random_number(model,var,field):
    if var == 'in':
        return generate_random_number(model, field)
    elif var == 'out':
        return generate_random_number(model, field)
    else:
        return generate_random_number(model, field)

    
def limit_off(model, request, serial):
        query_params = request.query_params
        id = query_params['id'] if query_params.get('id') else False
        limit = query_params['limit'] if query_params.get('limit') else False
        offset  = query_params['offset'] if query_params.get('offset')  else False

        if id:
            query = model.objects.filter(id=id)
        elif limit and offset:
            query = model.objects.all()[int(offset):int(limit)+int(offset)]
        elif limit or offset:
            if limit:
                query = model.objects.all()[:int(limit)]
            else:
                query = model.objects.all()[int(offset):]        
        else:
            query = model.objects.all() 

        serializer = serial(query, many=True)
        return serializer.data 
    
class LowercaseEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get('email')
        if email is not None:
            email = email.lower()
        return super().authenticate(request, email, password, **kwargs) 