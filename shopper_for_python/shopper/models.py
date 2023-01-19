from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Area(models.Model):
    name = models.CharField(max_length=100)
    prefecture = models.ForeignKey('Prefecture', models.DO_NOTHING)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'area'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    store = models.ForeignKey('Store', models.DO_NOTHING)
    sub_item = models.ForeignKey('SubItem', models.DO_NOTHING)
    image = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'coupon'


class CouponUse(models.Model):
    coupon = models.ForeignKey(Coupon, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    used_flag = models.IntegerField()
    start_date = models.DateTimeField()

    def __str__(self):
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'coupon_use'


class Discount(models.Model):
    store = models.ForeignKey('Store', models.DO_NOTHING)
    item = models.ForeignKey('Item', models.DO_NOTHING)
    detail = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField()
    amount = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'discount'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        'DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Favorite(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    product = models.ForeignKey('Product', models.DO_NOTHING)

    def __str__(self):
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'favorite'


class Flyer(models.Model):
    store = models.ForeignKey('Store', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    click = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    main_image = models.CharField(max_length=100, blank=True, null=True)
    sub_image = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'flyer'


class Follow(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, related_name='user')
    follow_user = models.ForeignKey(
        'User', models.DO_NOTHING, related_name='follow_user')

    def __str__(self):
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'follow'


class Unit(models.Model):
    name = models.CharField(max_length=6)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'unit'


class Item(models.Model):
    name = models.CharField(max_length=100)
    unit = models.ForeignKey('Unit', models.DO_NOTHING)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'item'


class MainItem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'main_item'


class NewTable(models.Model):
    name = models.CharField(max_length=45)
    address = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'new_table'


class Prefecture(models.Model):
    name = models.CharField(max_length=10)
    region = models.ForeignKey('Region', models.DO_NOTHING)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'prefecture'


class Product(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    item = models.ForeignKey(Item, models.DO_NOTHING)
    detail = models.CharField(max_length=100, blank=True, null=True)
    store = models.ForeignKey('Store', models.DO_NOTHING)
    amount = models.IntegerField(blank=True, null=True)
    price = models.IntegerField()
    date = models.DateField()
    discount = models.IntegerField()
    comment = models.CharField(max_length=1000, blank=True, null=True)
    price_per_amount = models.DecimalField(max_digits=11, decimal_places=1)

    def create(self, **kwargs):
        print('オーバーライドがうまくいってるか')
        if not self.price_per_amount:
            print('オーバーライドのif文がうまくいってるか')
            self.price_per_amount = (self.price / self.amount)
            print(self.price_per_amount)
            # super(Product, self).create(**kwargs)
            super().create(**kwargs)

    def save(self, *args, **kwargs):
        print('オーバーライドがうまくいってるか')
        if not self.price_per_amount:
            print('オーバーライドのif文がうまくいってるか')
            self.price_per_amount = (self.price / self.amount)
            print(self.price_per_amount)
            # super(Product, self).create(**kwargs)
            super().save(*args, **kwargs)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.detail
        # 名前表示
        # return self.detail
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'product'


class Recipe(models.Model):
    store = models.ForeignKey('Store', models.DO_NOTHING)
    name = models.CharField(max_length=100)
    click = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image_1 = models.CharField(max_length=100, blank=True, null=True)
    image_2 = models.CharField(max_length=100, blank=True, null=True)
    image_3 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'recipe'


class Region(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'region'


class Store(models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(Area, models.DO_NOTHING)
    address = models.CharField(max_length=100)
    start_hour = models.TimeField(blank=True, null=True)
    end_hour = models.TimeField(blank=True, null=True)
    business_hours = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    tel = models.CharField(max_length=12, blank=True, null=True)
    payment = models.CharField(max_length=200, blank=True, null=True)
    facility = models.CharField(max_length=200, blank=True, null=True)
    service = models.CharField(max_length=200, blank=True, null=True)
    administrated_flag = models.IntegerField()
    open_flag = models.IntegerField()
    store_user = models.ForeignKey(
        'StoreUser', models.DO_NOTHING, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'store'


class StoreUpdate(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey('User', models.DO_NOTHING)
    store_user = models.ForeignKey('StoreUser', models.DO_NOTHING)

    def __str__(self):
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'store_update'


class StoreUser(models.Model):
    mail = models.CharField(max_length=320)
    # Field renamed because it was a Python reserved word.
    password = models.CharField(db_column='pass', max_length=20)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tel = models.IntegerField()
    payment = models.IntegerField()
    active_flag = models.IntegerField()

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'store_user'


class SubItem(models.Model):
    name = models.CharField(max_length=100)
    main_item = models.ForeignKey(MainItem, models.DO_NOTHING)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'sub_item'


class User(models.Model):
    email = models.CharField(unique=True, max_length=255)
    # Field renamed because it was a Python reserved word.
    password = models.CharField(db_column='pass', max_length=255)
    name = models.CharField(max_length=10)
    birthday = models.DateField()
    gender = models.IntegerField()
    area = models.ForeignKey(Area, models.DO_NOTHING)
    active_flag = models.IntegerField()

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'user'


class Inquiry(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING)
    email = models.CharField(max_length=30)
    type = models.IntegerField()
    text = models.CharField(max_length=10000)

    def __str__(self):
        # id＆名前表示
        # return str(self.id)+":"+self.name
        # 名前表示
        # return self.name
        # id表示
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'inquiry'
