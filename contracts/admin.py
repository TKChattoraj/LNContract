from django.contrib import admin
from contracts.models import (
    LN_Node,
    Contract,
    Entity,
    Good,
    Service,
    MonetaryObligation,
    SaleOfGood,
    SaleOfService,
    ContractText
)


# Register your models here.
models=[LN_Node, Contract, Entity, Good, Service, MonetaryObligation, SaleOfGood, SaleOfService, ContractText]
admin.site.register(models)