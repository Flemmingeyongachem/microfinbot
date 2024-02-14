from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    chat_id = fields.BigIntField(unique=True)
    telegram_number = fields.CharField(max_length=50)
    password = fields.CharField(max_length=100)
    is_student = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_business_user = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    

    class PydanticMeta:
        # computed = ["full_name"]
        exclude = ["password"]
        # include = []
        
UserSerializer = pydantic_model_creator(User, name="user")
UserCreateSerializer = pydantic_model_creator(User,name="new user",exclude_readonly=True)

    
#gift restuarant treats,allow for business acoount
# allow for collect contribution 



class Department(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=400,unique=True)
    account_number = fields.BigIntField(unique=True)
    
    class Meta:
        ordering = ['name']
    
    
class ExchangeAddress(models.Model):
    id = fields.BigIntField(pk=True)
    user = fields.OneToOneField("models.User",related_name="exchange_address")
    address = fields.CharField(max_length=255, unique=True)
    
    class Meta:
        ordering = ['address']
    
class TagBook(models.Model):
    id = fields.BigIntField(pk=True)
    tags = fields.ManyToManyField("models.ExchangeAddress",related_name="tags")
    owner = fields.ForeignKeyField("models.User", related_name="tagbook")
    
    class Meta:
        ordering = ['tags']
    
class Transaction(models.Model):
    id = fields.BigIntField(pk=True)
    from_address = fields.OneToOneField("models.ExchangeAddress",related_name="sender")
    to_address = fields.ForeignKeyField("models.ExchangeAddress", related_name="receiver")
    created = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    
class MicroFinanceAccount(models.Model):
    id = fields.BigIntField(pk=True)
    account_number = fields.CharField(max_length=255,unique=True)
    is_student_account = fields.BooleanField(default=False)
    is_business_account = fields.BooleanField(default=False)
    balanace = fields.DecimalField(decimal_places=2, max_digits=15)    
    owner = fields.OneToOneField("models.User", related_name="microfinance_account")
    
    
class Bussiness(models.Model):
    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=400, unique=True, db_index=True)
    description = fields.TextField(max_length=1000, null=True)
    business_address = fields.ForeignKeyField("models.ExchangeAddress",related_name="business_address",null=True)
    
    
    

    
     
    