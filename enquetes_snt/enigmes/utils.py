""" import random
from .models import Enquete

def generer_code_enquete_unique():
    enquetes = Enquete.objects.all()
    codes_existants = set(enquete.code for enquete in enquetes)
    carac = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code = "".join(random.choices(carac, k=8))
    while code in codes_existants:
        code = "".join(random.choices(carac, k=8))
    return code """