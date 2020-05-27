# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.conf import settings
from barahlochannel.settings import ChannelEnum
from enum import Enum, auto


class CategoriesEnum(Enum):
    ROAD = auto()
    CYCLOCROSS = auto()
    FIX = auto()
    SINGLE = auto()
    GRAVEL = auto()
    TOURING = auto()
    FRAMES = auto()
    FORKS = auto()
    RIMBRAKES = auto()
    DISCBRAKES = auto()
    BRAKELEVERS = auto()
    BRAKECABLES = auto()
    HANDLEBARS = auto()
    STEMS = auto()
    HEADSETS = auto()
    TOPCAPS = auto()
    SPACERS = auto()
    BARTAPES = auto()
    GRIPS = auto()
    SADDLES = auto()
    SEATPOSTS = auto()
    CLAMPS = auto()
    GROUPSETS = auto()
    CHAINSETS = auto()
    CHAINS = auto()
    BOTTOMBRACKETS = auto()
    CHAINRINGS = auto()
    FRONTDERAILLEURS = auto()
    CASSETES = auto()
    FREEHUBS = auto()
    REARDERAILLEURS = auto()
    GEARLEVERS = auto()
    MECHHANGERS = auto()
    GEARCABLES = auto()
    PEDALS = auto()
    CLEATS = auto()
    STRAPS = auto()
    TOECLIPS = auto()
    CLEATCOVERS = auto()
    WHEELS = auto()
    HUBS = auto()
    TYRES = auto()
    RIMS = auto()
    TUBES = auto()
    SPOKES = auto()
    PUMPS = auto()
    TOOLS = auto()
    STANDS = auto()
    GLASSES = auto()
    LOCKS = auto()
    LIGHTS = auto()
    BOTTLES = auto()
    BOTTLECAGES = auto()
    COMPUTERS = auto()
    MUDGUARDS = auto()
    RACKS = auto()
    TRAINERS = auto()
    BIKEBAGS = auto()
    FRAMEBAGS = auto()
    BAUL = auto()
    ROLLTOPS = auto()
    MESSENGERS = auto()
    HANDLEBARBAGS = auto()
    WAISTBAGS = auto()
    CLOTHING = auto()
    FOOTWEAR = auto()
    HELMETS = auto()


class CurrencyEnum(Enum):
    RUB = 'RUB/₽'
    USD = 'USD/$'
    EUR = 'EUR/€'
    UAH = 'UAH/Гривна'


class ShippingEnum(Enum):
    DO_NOT_SHIP = "Не отправляю"
    WILL_SHIP_BY_CUSTOMER = "За счет покупателя"
    WILL_SHIP_SAINT = "За свой счёт"


class BarahlochannelAlbums(models.Model):
    owner_id = models.BigIntegerField(primary_key=True)
    album_id = models.BigIntegerField()
    title = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    photo = models.CharField(max_length=1024, blank=True, null=True)

    def is_group(self):
        if self.owner_id < 0:
            return True
        return False

    class Meta:
        managed = False
        db_table = 'albums'
        unique_together = (('owner_id', 'album_id'),)


class GoodsManager(models.Manager):
    def has_duplicates(self, photo_hash):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM {t} 
                WHERE hash = %s;
                """.format(t=self.model._meta.db_table), (photo_hash,))
            result = cursor.fetchone()
            return result[0]


class BarahlochannelGoods(models.Model):
    vk_owner_id = models.IntegerField(primary_key=True)
    vk_photo_id = models.IntegerField()
    photo_link = models.CharField(max_length=1024)
    photo_preview = models.CharField(max_length=1024)
    seller = models.ForeignKey('Sellers', models.DO_NOTHING)
    descr = models.CharField(max_length=6666, blank=True, null=True)
    comments = models.CharField(max_length=1024, blank=True, null=True)
    tg_post_id = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True, null=True)

    objects = GoodsManager()

    def has_duplicates(self):
        if self.hash is None:
            return False
        return BarahlochannelGoods.objects.has_duplicates(self.hash) != 1

    def duplicates_number(self):
        return BarahlochannelGoods.objects.filter(hash=self.hash).count()

    def get_preview_photo(self):
        if not self.photo_preview:
            return self.photo_link
        return self.photo_preview

    class Meta:
        managed = False
        db_table = 'goods'
        unique_together = (('vk_owner_id', 'vk_photo_id'),)


class Cities(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cities'


class Groups(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1024, blank=True, null=True)
    screen_name = models.CharField(max_length=1024, blank=True, null=True)
    photo = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Sellers(models.Model):
    vk_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)
    photo = models.CharField(max_length=1024, blank=True, null=True)

    def is_group(self):
        if self.vk_id < 0:
            return True
        return False

    def goods_counter(self):
        return BarahlochannelGoods.objects.filter(seller__vk_id=self.vk_id).count()

    class Meta:
        managed = False
        db_table = 'sellers'


class TgGoods(models.Model):
    CATEGORY_CHOICES = [(c.name, c.name) for c in CategoriesEnum]
    SHIP_CHOICES = [(s.name, s.value) for s in ShippingEnum]
    CURRENCY_CHOICES = [(c.name, c.value) for c in CurrencyEnum]

    tg_user = models.ForeignKey('TgSellers', models.DO_NOTHING, blank=True, null=True)
    photo_link = models.CharField(max_length=1024, blank=True, null=True)
    caption = models.CharField(max_length=4096, blank=True, null=True)
    descr = models.CharField(max_length=4096, blank=True, null=True)
    tg_post_id = models.IntegerField(primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    hash = models.CharField(max_length=64, blank=True, null=True)
    category = models.TextField(blank=True, null=True, choices=CATEGORY_CHOICES)
    price = models.IntegerField(blank=True, null=True)
    currency = models.TextField(blank=True, null=True, choices=CURRENCY_CHOICES)
    ship = models.TextField(blank=True, null=True, choices=SHIP_CHOICES)
    vk_owner_id = models.IntegerField(blank=True, null=True)
    vk_photo_id = models.IntegerField(blank=True, null=True)

    def get_preview_photo(self):
        return self.photo_link

    class Meta:
        managed = False
        db_table = 'tg_goods'


class TgSellers(models.Model):
    tg_user_id = models.IntegerField(primary_key=True)
    full_name = models.CharField(max_length=512, blank=True, null=True)
    username = models.CharField(max_length=512, blank=True, null=True)
    tg_chat_id = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(Cities, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tg_sellers'
