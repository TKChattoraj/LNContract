from django.db import models

# Create your models here.

class LN_Node(models.Model):
    address=models.CharField(max_length=50, default=None)

    def ln_node_dir(instance, filename):
        # assumes MEDIA_ROOT=Base_Dir/contracts/
        # Note:  might need to create the /ln_nodes/node_{0} folder/subfolder contstruct when the contract is created
        # when the node object is created, then create the folder structure
        return 'ln_nodes/node_{0}/{1}'.format(instance.pk, filename)
    
    tls_path=models.FileField(upload_to=ln_node_dir)    
    macaroon_path=models.FileField(upload_to=ln_node_dir)
    status=models.CharField(max_length=50, blank=True, null=True)

class Contract(models.Model):
    contract_no=models.CharField(max_length=20)
    description=models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True)

class Entity(models.Model):
    name=models.CharField(max_length=20)
    ln_node=models.ForeignKey(LN_Node, on_delete=models.CASCADE, blank=True, null=True)
    contracts=models.ManyToManyField(Contract, blank=True)
    party=models.BooleanField()

class Good(models.Model):
    part_number=models.CharField(max_length=50) # can't be None
    description=models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True)

class Service(models.Model):
    service_number=models.CharField(max_length=50) # can't be None
    description=models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True)


class MonetaryObligation(models.Model):
    MONETARY_UNITS=[
    ('Sats', 'Satoshis'),
    ('BTC', 'Bitcoin'),
    ('$', 'Dollar')
    ]   
    contract=models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    amount=models.BigIntegerField(blank=True, null=True)
    unit=models.CharField(max_length=4, choices=MONETARY_UNITS)
    due_date=models.DateField()
    tender=models.BooleanField() #whether or not the obligation has been proffered
    status=models.CharField(max_length=100, blank=True, null=True)

class SaleOfGood(models.Model):
    contract=models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    entity=models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True)
    good=models.ForeignKey(Good, on_delete=models.CASCADE, blank=True, null=True)
    quantity=models.IntegerField(blank=True, null=True)
    description=models.CharField(max_length=100, blank=True, null=True)
    due_date=models.DateField(blank=True, null=True)
    tender=models.BooleanField() #whether or not the obligation has been proffered
    status=models.CharField(max_length=100, blank=True, null=True)

class SaleOfService(models.Model):
    contract=models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    entity=models.ForeignKey(Entity, on_delete=models.CASCADE, blank=True, null=True)
    service=models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    quantity=models.IntegerField(blank=True, null=True)
    description=models.CharField(max_length=100, blank=True, null=True)
    due_date=models.DateField(blank=True, null=True)
    tender=models.BooleanField() #whether or not the obligation has been proffered
    status=models.CharField(max_length=100, blank=True, null=True)

class ContractText(models.Model):
    def contract_files_path(instance, filename):
        # assumes MEDIA_ROOT=Base_Dir/contracts
        # Note:  might need to create the /contract_texts/contract_{0} folder/subfolder contstruct when the contract is created
        # when the contract object is created, then create the folder structure
        return '/contracts_docs/contract_{0}/{1}'.format(instance.contract, filename)
        pass
    contract=models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    file=models.FileField(upload_to=contract_files_path)




