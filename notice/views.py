import os
from django.shortcuts import render,get_object_or_404,redirect
from .forms import NoticeForm
from .models import Notice
from django.utils import timezone
#from django.conf import settings
#from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger

# Create your views here.
def post(request):
    if request.method=="POST":
        form=NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice=form.save(commit=False)
            notice.update_date=timezone.now()
            notice.save()
            return HttpResponseRedirect('/notice/post_list')
    else:
        form=NoticeForm()
        return render(request,'post.html',{'form':form})

#def show(request):
    #notices=Notice.objects.order_by('-id')
    #return render(request,'show.html',{'notices':notices})

def detail(request,notice_id):
    notice_detail=get_object_or_404(Notice, pk=notice_id)
    return render(request,'detail.html',{'notice':notice_detail})

def edit(request,pk):
    notice=get_object_or_404(Notice,pk=pk)
    if request.method=="POST":
        form=NoticeForm(request.POST,request.FILES,instance=notice)
        if form.is_valid():
            notice=form.save(commit=False)
            notice.update_date=timezone.now()
            notice.save()
            return HttpResponseRedirect('/notice/post_list')

    else:
        form=NoticeForm(instance=notice)
        return render(request,'edit.html',{'form':form})


def delete(request,pk):
    notice=Notice.objects.get(id=pk)
    notice.delete()
    return redirect('post_list')

def post_list(request):
        PAGE_ROW_COUNT=10
        PAGE_DISPLAY_COUNT=5

        total_list=Notice.objects.all().order_by('-id')
        paginator=Paginator(total_list,PAGE_ROW_COUNT)
        pageNum=request.GET.get('pageNum')

        toPageCount=paginator.num_pages

        try:
                total_list=paginator.page(pageNum)
        except PageNotAnInteger:
                total_list=paginator.page(1)
                pageNum=1
        except EmptyPage:
                total_list=paginator.page(paginator.num_pages)
                pageNum=paginator.num_pages
        pageNum=int(pageNum)

        if pageNum<=PAGE_DISPLAY_COUNT:
                startPageNum=1
        else:
                startPageNum=1+((pageNum-1)/PAGE_DISPLAY_COUNT)*PAGE_DISPLAY_COUNT

        endPageNum=startPageNum+PAGE_DISPLAY_COUNT-1
        if toPageCount<endPageNum:
                endPageNum=toPageCount

        bottomPages=range(int(startPageNum),int(endPageNum+1))

        #no

        noticesnum=range(int(Notice.objects.count()),int(1))

        return render(request,'show.html',{
                'noticesnum':noticesnum,
                'total_list':total_list,
                'pageNum':pageNum,
                'bottomPages':bottomPages,
                'toPageCount':toPageCount,
                'startPageNum':startPageNum,
                'endPageNum':endPageNum})


def download(request,pk):
    notice_download=get_object_or_404(Notice,pk=pk)
    file_url=notice_download.file.url[1:]
    if os.path.exists(file_url):
        with open(file_url,'rb') as fh:
            response=HttpResponse(fh.read(),content_type="application/octet-stream")
            response['attachment']='inline:filename='+os.path.basename(file_url)
            return response
        raise Http404   
