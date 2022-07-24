from django.shortcuts import render, redirect

# Create your views here.
# my_imports
from django.conf import settings
from django.http import HttpResponse
import random
import qrcode
import qrcode.image.svg
from io import BytesIO
from PIL import Image
from pathlib import *


def getit(request):
    if request.method == 'POST':

        title = str(request.POST.get('qr_text'))
        if title != None:  # on refresh an empty form is initiated with title None, if the title is not None proceed
            return title


def getwhat(request):
    if request.method == 'POST':
        title = str(getit(request))

        # title = request.POST.get('qr_text')
        if title != None:  # on refresh an empty form is initiated with title None, if the title is not None proceed
            img = qrcode.make(request.POST.get('qr_text', ''), box_size=10)
            return img


def getsvg(request):
    if request.method == 'POST':
        title = str(getit(request))

        if title != None:  # on refresh an empty form is initiated with title None, if the title is not None proceed

            # generate a qr code as svgimage
            factory = qrcode.image.svg.SvgImage

            # image factory is inbuilt in qrcode, gets input from user and pass it to generate with imagefactory
            img = qrcode.make(request.POST.get('qr_text', ''), image_factory=factory,
                              box_size=25)

            # BytesIO prevents from writing to file, output is rendered instead
            stream = BytesIO()
            img.save(stream)

            svg = stream.getvalue().decode()

            return (svg)


def main(request):
    context = {}

    title = str(getit(request))
    svg = getsvg(request)

    context = {
        'svg': svg,
        'title': title,
    }
    return render(request, 'app/main.html', context)


def pngView(request):

    # title = str(getit(request))
    title = str(request.POST.get('title'))

    # title = str(request.POST.get('qr_text'))
    if title != 'None':  # on refresh an empty form is initiated with title None, if the title is not None proceed
        img = qrcode.make(request.POST.get('title', ''), box_size=15)

        # type(img)
        # name IMG with "title" entered in form concatenated with .png
        imgName = title + '.png'
        # specifies the folder it is saved to
        path = str(settings.MEDIA_ROOT)
        img.save(path + '/' + imgName)

        # # assign random number as name
        # title = str(random.randrange(00000, 99999))
        # img.save(title + '.png')

        response = HttpResponse(
            #    # open("static/downloads/pdfs/43456.pdf", 'rb').read())
            open(path+'/'+imgName, 'rb').read())

        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=%s' % (imgName)
        return response

    # return render(request, 'app/main.html', context)
    return render(request, 'app/pngview.html')


def pdfView(request):

    # title = str(getit(request))
    title = str(request.POST.get('title'))

    if title != 'None':  # on refresh an empty form is initiated with title None, if the title is not None proceed

        # img = getwhat(request)
        img = qrcode.make(request.POST.get('title', ''), box_size=10)

        # convert image to pdf with Pillow library
        pdf = img.convert('RGB')
        # name PDF with "title" entered in form concatenated with .pdf
        pdfName = title + '.pdf'
        # specifies the folder it is saved to
        path = str(settings.MEDIA_ROOT)
        pdf.save(path + '/' + pdfName)

        response = HttpResponse(
            open(path+'/'+pdfName, 'rb').read())

        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=%s' % (pdfName)
        return response

        return render(request, 'app/pdfview.html')
