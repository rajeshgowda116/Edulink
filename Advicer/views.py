from django.shortcuts import render
from utils.Codegen import Code
# Create your views here.
def generate_code(request):
  code_gen=Code()
  if request.method=='POST':
    code=request.POST.get('')
