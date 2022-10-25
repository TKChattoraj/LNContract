from django.db import models

# Create your models here.

class LN_Node(models.Model):
    address=models.CharField(max_length=50, default=None)

    def ln_node_dir(instance, filename):
        # assumes MEDIA_ROOT=Base_Dir/contracts/
        return 'ln_nodes/node_{0}/{1}'.format(instance.pk, filename)
    
    tls_path=models.FileField(upload_to=ln_node_dir)    
    macaroon_path=models.FileField(upload_to=ln_node_dir)
    status=models.CharField(max_length=50, blank=True, null=True)

class Contract(models.Model):
    contract_no=models.CharField(max_length=20)
    description=models.CharField(max_length=100, blank=True, null=True)
    status=models.CharField(max_length=100, blank=True, null=True)

    def contracts_context():
        cs=Contract.objects.all()
        contracts=[]
      
        for c in cs:         
            es=c.entity_set.all()
            print(es)
            if es.filter(party=True):
                p=es.filter(party=True)[0] #grab the first party
            else:
                p=None
            print(p)
            if es.filter(party=False):
                cp=es.filter(party=False)[0] #grab the first counteparty
            else:
                cp=None 
            contracts.append((c, p, cp))
        print(contracts)
        
        context={'contracts': contracts}

        return context

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
        # assumes MEDIA_ROOT=Base_Dir/contracts/

        return 'contracts_docs/contract_{0}/{1}'.format(instance.contract.pk, filename)
        pass
    contract=models.ForeignKey(Contract, on_delete=models.CASCADE, blank=True, null=True)
    file=models.FileField(upload_to=contract_files_path)




