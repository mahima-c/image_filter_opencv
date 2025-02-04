from django.db import models
from .utils import get_filtered_image
from PIL import Image
import  numpy as np
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.
ACTION_CHOICES=(
    ("NO_FILTER",'no filtered'),
    ("COLORIZED",'colorized'),
    ("GRAYSCALE",'grayscale'),
    ('BLURRED','blurred'),
    ('BINARY','binany'),
    ('INVERT','invert')
)


class Upload(models.Model):
    image=models.ImageField(upload_to='images',default="")
    action=models.CharField(max_length=50,choices=ACTION_CHOICES)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id)


    def save(self,*args,**kwargs):
        #open image
        pil_img=Image.open(self.image)
        # convert the image to array and processing
        cv_img=np.array(pil_img)
        img=get_filtered_image(cv_img,self.action)
        # convert back to image 
        img_pil=Image.fromarray(img)

        # save
        buffer=BytesIO()
        img_pil.save(buffer,format='png')
        image_png=buffer.getvalue()
        self.image.save(str(self.image),ContentFile(image_png),save=False)
        super().save(*args,**kwargs)