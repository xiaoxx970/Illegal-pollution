from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='请选择数据文件（CSV格式）')
