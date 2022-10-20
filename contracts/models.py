from django.db import models

# Create your models here.

class LN_Nodes(models.Model):
    pass

class Entities(models.Model):
    name=models.CharField(max_length=20)
    ln_node=models.ForeignKey(LN_Nodes, on_delete=models.CASCADE)
    party=models.BooleanField()


class Contracts(models.Model):
    contract_no=models.CharField(max_length=20)
    party=models.ForeignKey(Entities, on_delete=models.CASCADE)
    counterparty=models.ForeignKey(Entities, on_delete=models.CASCADE)
    description=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

