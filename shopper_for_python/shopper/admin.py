from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

# モデルをインポート
from .models import *

# 管理ツールに登録


class RegionAdmin(BaseUserAdmin):
    list_display = (
        "name",
    )
    list_filter = (
        "name",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',)}
         ),
    )


admin.site.register(Region, RegionAdmin)


class PrefectureAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "region",
    )
    list_filter = (
        "name",
        "region",
    )
    ordering = ("id",)
    filter_horizontal = ()

    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'region',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'region',)}
         ),
    )


admin.site.register(Prefecture, PrefectureAdmin)


class AreaAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "prefecture",
    )
    list_filter = (
        "name",
        "prefecture",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'prefecture',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'prefecture',)}
         ),
    )


admin.site.register(Area, AreaAdmin)


class UserAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "email",
        "birthday",
        "gender",
        "area",
        "active_flag",
    )
    list_filter = (
        "name",
        "email",
        "birthday",
        "gender",
        "area",
        "active_flag",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'email', 'birthday',
         'gender', 'area', 'active_flag',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'birthday', 'gender', 'area', 'active_flag',)}
         ),
    )


admin.site.register(User, UserAdmin)


class StoreAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "area",
        "address",
        "start_hour",
        "end_hour",
        "url",
        "tel",
        "payment",
        "facility",
        "service",
        "administrated_flag",
        "open_flag",
        "store_user",
        "count",
    )
    list_filter = (
        "name",
        "area",
        "address",
        "start_hour",
        "end_hour",
        "url",
        "tel",
        "payment",
        "facility",
        "service",
        "administrated_flag",
        "open_flag",
        "store_user",
        "count",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'area', 'address', 'start_hour', 'end_hour', 'url', 'tel', 'payment',
         'facility', 'service', 'administrated_flag', 'open_flag', 'store_user', 'count', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'area', 'address', 'start_hour', 'end_hour', 'url', 'tel', 'payment', 'facility', 'service', 'administrated_flag', 'open_flag', 'store_user', 'count', )}
         ),
    )


admin.site.register(Store, StoreAdmin)


class StoreUpdateAdmin(BaseUserAdmin):
    list_display = (
        "date",
        "user",
        "store_user",
    )
    list_filter = (
        "date",
        "user",
        "store_user",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('date',)

    fieldsets = (
        (None, {'fields': ('date', 'user', 'store_user',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('date', 'user', 'store_user',)}
         ),
    )


admin.site.register(StoreUpdate, StoreUpdateAdmin)


class StoreUserAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "mail",
        "address",
        "tel",
        "payment",
        "active_flag",
    )
    list_filter = (
        "name",
        "mail",
        "address",
        "tel",
        "payment",
        "active_flag",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name', 'mail', 'address', 'tel',)

    fieldsets = (
        (None, {'fields': ('name', 'mail', 'password',
         'address', 'tel', 'payment', 'active_flag',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'mail', 'password', 'address', 'tel', 'payment', 'active_flag',)}
         ),
    )


admin.site.register(StoreUser, StoreUserAdmin)


class MainItemAdmin(BaseUserAdmin):
    list_display = (
        "name",
    )
    list_filter = (
        "name",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',)}
         ),
    )


admin.site.register(MainItem, MainItemAdmin)


class SubItemAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "main_item",
    )
    list_filter = (
        "name",
        "main_item",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'main_item',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'main_item',)}
         ),
    )


admin.site.register(SubItem, SubItemAdmin)


class ItemAdmin(BaseUserAdmin):
    list_display = (
        "name",
        "sub_item",
        "unit",
    )
    list_filter = (
        "name",
        "sub_item",
        "unit",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('name',)

    fieldsets = (
        (None, {'fields': ('name', 'sub_item', 'unit',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'sub_item', 'unit',)}
         ),
    )


admin.site.register(Item, ItemAdmin)


class ProductAdmin(BaseUserAdmin):
    list_display = (
        "user",
        "item",
        "detail",
        "store",
        "amount",
        "price",
        "date",
        "discount",
        "comment",
    )
    list_filter = (
        "user",
        "item",
        "detail",
        "store",
        "amount",
        "price",
        "date",
        "discount",
        "comment",
    )
    ordering = ("id",)
    filter_horizontal = ()
    search_fields = ('detail',)

    fieldsets = (
        (None, {'fields': ('user', 'item', 'detail', 'store',
         'amount', 'price', 'date', 'discount', 'comment',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'item', 'detail', 'store', 'amount', 'price', 'date', 'discount', 'comment',)}
         ),
    )


admin.site.register(Product, ProductAdmin)
