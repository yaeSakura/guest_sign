from django.db import models
import datetime

# Create your models here.

class Route(models.Model):
    name = models.CharField(max_length=40, unique=True)
    spots = models.CharField(max_length=800, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = "indoor_patrol_route"

    def __repr__(self):
        return "{}_{}".format(self._meta.verbose_name, self.name)

    __str__ = __repr__

class Plan(models.Model):
    name = models.CharField(max_length=40, blank=True)
    remark = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    executive_group = models.ForeignKey('Guard',
                                        on_delete=models.SET_NULL,
                                        blank=True,
                                        null=True,)

    MODE_EVERYDAY = 0
    MODE_SINGLE = 1
    MODE_DOUBLE = 2
    MODE_CHOICES = (
        (MODE_EVERYDAY, 'everyday'),
        (MODE_SINGLE, 'single'),
        (MODE_DOUBLE, 'double'),
    )
    mode = models.IntegerField(choices=MODE_CHOICES, default=MODE_EVERYDAY)
    route = models.ForeignKey('indoor_patrol.Route',
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    intervals = models.IntegerField(default=30, verbose_name='每次巡检之间的时间间隔（分钟）',)
    rounds = models.IntegerField(default=1, verbose_name='巡逻轮次',)

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return 'indoor patrol plan {}'.format(self.name)

    __str__ = __repr__

    @property
    def attributes(self):
        attr = {}
        for field in self._meta.get_fields():
            field_name = field.name
            attr[field_name] = getattr(self, field_name, None)
        return attr

# guard\models
class Guard(models.Model):
    name = models.CharField(max_length=40, blank=True, default="")
    phone = models.CharField(max_length=40, blank=True, default="")
    uniform_id = models.CharField(max_length=40, blank=True, default="")
    terminal = models.OneToOneField("Terminal",
                                    on_delete=models.SET_NULL,
                                    related_name='guard',
                                    blank=True,
                                    null=True)

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return 'guard: {}, uniform_id: {}'.format(self.name,
                                                  self.uniform_id,
                                                  )

    __str__ = __repr__

# terminal\models
class Terminal(models.Model):
    name = models.CharField(max_length=40, blank=True)
    serial_number = models.IntegerField(max_length=10, unique=True)
    type = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __repr__(self):
        return 'name: {}, serial_number: {}'.format(self.name,
                                                    self.serial_number,)

    __str__ = __repr__

class Record(models.Model):
    PATROL_RECORD = 0
    WARNING_MSG = 1
    MODE_CHOICES = (
        (PATROL_RECORD, 'patrol record'),
        (WARNING_MSG, 'warning msg'),
    )
    type = models.IntegerField(choices=MODE_CHOICES, default=PATROL_RECORD)
    dvice_id = models.IntegerField(max_length=10)
    spot = models.CharField(max_length=10)
    time = models.DateTimeField()
    events = models.CharField(max_length=20)

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return 'type: {}, dvice_id: {}'.format(self.type,
                                               self.dvice_id,)

    __str__ = __repr__