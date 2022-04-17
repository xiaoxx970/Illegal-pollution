import os
from django.shortcuts import redirect, render
from .models import Document, Results
from .forms import DocumentForm


def my_view(request):
    message = '上传企业排污数据后点击上方链接下载结果'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            result = Results().objects.all(docfile="ressult.csv")

            print(f'-i {newdoc.docfile.path} -o {result.docfile.path}')
            print(result.docfiel.url)
            try:
                code = os.system(f'python kmeans_calc.py -i {newdoc.docfile.path} -o {newdoc.docfile.path}')
            except Exception as e:
                message = str(e)
            if code != 0:
                message = f'Exec script failed, code: {code}'

            # Redirect to the document list after POST
            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    result = Results().objects.all()[0]
    # Render list page with the documents and the form
    context = {'result': result, 'form': form, 'message': message}
    return render(request, 'list.html', context)
