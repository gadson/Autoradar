from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Geo(models.Model):
 #  title = models.CharField(_('title'), max_length=128)
 #  created_at = models.DateTimeField(_('created at'), auto_now_add=True)
 #  announce_text = models.TextField(_('announce'), max_length=512, blank=True)
 #  text = models.TextField(_('text'), max_length=4096)
    ID_obj = models.CharField(_('ID объекта'), max_length=20, blank=False)
    name = models.CharField(_('Имя объекта'), max_length=200, blank=False)
    dop = models.CharField(_('Дополнительное описание'), max_length=250, blank=True)
    telephone = models.CharField(_('telephone'), max_length=19, blank=True)
    email = models.CharField(_('email'), max_length=55, blank=True)
    admin = models.BooleanField(_('Администрирование'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    user_name = models.CharField(_('user_name'), max_length = 75, blank = True, )

    def __str__(self):
       return self.ID_obj


    def publish(self):
        self.save

    def save(self, *args, **kwargs):
        if (self.user is None) and (self.user_name != ''):
            self.user = User.objects.get(user_name=str(self.user_name))
        else:
            if (self.user is None) and (self.user_name == ''):
                self.user = User.objects.get(user_name=str('admin'))
        super(Geo, self).save(*args, **kwargs)


    @property
    def announce(self):
        return self.announce_text or self.text[:512].rsplit(' ', 1)[0]

    class Meta:
        ordering = ['-ID_obj']
        verbose_name = _('Объект')
        verbose_name_plural = _('Объекты')
        #unique_together = ('num', 'fio')


class movement(models.Model):
 #  title = models.CharField(_('title'), max_length=128)
 #  created_at = models.DateTimeField(_('created at'), auto_now_add=True)
 #  announce_text = models.TextField(_('announce'), max_length=512, blank=True)
    ID_obj = models.ForeignKey(Geo, on_delete=models.CASCADE)
    datetime = models.DateTimeField(
            blank=True, null=True)
    Latitude = models.CharField(_('Широта'), max_length=55, blank=True)
    Longitude = models.CharField(_('Долгота'), max_length=55, blank=True)


    def publish(self):
        self.datetime = timezone.now()
        self.datetime = datetime.datetime.now()
        self.save()


    def save(self, *args, **kwargs):
        self.datetime = datetime.datetime.now()
        super(movement, self).save()


    class Meta:
        ordering = ['-datetime']
        verbose_name = _('Передвижения')
        verbose_name_plural = _('Передвижения')
        #unique_together = ('num', 'fio')


class events(models.Model):
 #  title = models.CharField(_('title'), max_length=128)
 #  created_at = models.DateTimeField(_('created at'), auto_now_add=True)
 #  announce_text = models.TextField(_('announce'), max_length=512, blank=True)
    ID_obj = models.ForeignKey('Geo', on_delete=models.CASCADE)
    datetime = models.DateTimeField(
            blank=True, null=True)
    event = models.CharField(_('событие'), max_length=2, blank=True)
    dop = models.CharField(_('описание'), max_length=255, blank=True)
    logic = models.BooleanField(_('Открыто/Закрыто'))


    def publish(self):
        self.datetime = timezone.now()
        self.datetime = datetime.datetime.now()
        self.save()


    def save(self, *args, **kwargs):
        self.datetime = datetime.datetime.now()
        super(events, self).save()

    class Meta:
        ordering = ['-datetime']
        verbose_name = _('События')
        verbose_name_plural = _('События')
        #unique_together = ('num', 'fio')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(_('Телефон'), max_length=200, blank=True)
    zoom = models.CharField(_('Zoom'), max_length=2, blank=True)
    #ID_obj = models.ForeignKey(Geo, on_delete=None, blank=True)
    select = models.CharField(_('Select'), max_length=200, blank=True)
    maxobject = models.PositiveIntegerField(default=3)
    active = models.BooleanField(default=True)

class Push_ID(models.Model):
    ID_Push = models.CharField(max_length=200)
    User = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.zoom="14"
    instance.profile.save()


#def own_clients(request):
#    return Zayavky.objects.filter(user_name=request.user.id).order_by('-id')[:30]

#def own_bd(request):
#    return Zayavky.objects.filter(id = request.GET.get('id'))[0]

def user_email(username_in): # получаем значение поля email пользователя
   email = User.objects.get(username = username_in)
   return email.email

def user_id(username_in): # получаем значение поля email пользователя
   user_id = User.objects.get(username = username_in)
   return user_id.id

def object_name(ID_obj_in): # получаем значение поля email пользователя
   obj_name = Geo.objects.get(ID_obj = ID_obj_in)
   return obj_name.name

def own_clients(request):
    return movement.objects.filter(ID_obj__user=request.user.id).values("ID_obj", "Latitude", "Longitude").order_by('-datetime')[:1]

#def own_bd(request):
#    return Zayavky.objects.filter(id = request.GET.get('id'))[0]