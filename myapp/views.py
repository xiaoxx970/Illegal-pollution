import os
from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm


def my_view(request):
    message = '上传企业排污数据后点击上方链接下载结果'
    # Handle file upload
    outurl = ""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()
            documents = Document.objects.all()
            filepath = documents[0].docfile.path
            url = documents[0].docfile.url
            outpath = "/".join(filepath.split("/")[:-1]) + "/ressult.csv"
            outurl = "/".join(url.split("/")[:-1]) + "/ressult.csv"
            print(f'-i {filepath} -o {outpath}')
            print(outurl)
            try:
                code = os.system(f'python kmeans_calc.py -i {filepath} -o {outpath}')
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


    # Render list page with the documents and the form
    context = {'outurl': outurl, 'form': form, 'message': message}
    return render(request, 'list.html', context)
