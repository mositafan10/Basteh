from django.db import models
from account.models import User, BaseModel, Country, City
from django.db import IntegrityError
import random


STATUS_CHOICES = [
        ('0', 'در انتظار تایید'),
        ('1', 'منتشر شده'),
        ('2', 'دارای پیشنهاد'),
        ('3', 'پذیرش شده'),
        ('4', 'ارسال شده'),
        ('5', 'عدم تایید'),
] 

# should complete TODO
# for other choice we need a field to be filled by user about category TODO
PACKET_CATEGORY = [
        ('0', 'مدارک'),('1', 'کتاب'),('2','لباس'),('3','سایر موارد')
]

# should complete TODO
PLACE = [
        ('0','فرودگاه'),('1','درب منزل'),('2','شهر'),
]

# do we need other currency for specially eroupe countries ? TODO
CURRENCY = [
        ('0','دلار'),('1','یورو'),('2','ریال'),
]

# should complete and need other choice and be filled by user TODO
REPORT_CHOICES = [ 
        ('0','عدم رعایت صداقت'),('1',''),('2',''),
]

Weight_Unit = [
    ('0','گرم'),('1','کیلوگرم'),('2','پوند'),
]
#should be completed
Airlines = [
    ('0','Mahan'),
    ('1','Iran Air'),
    ('2','Emirate'),
    ('3','Atlas Jet'),
    ('4','other'),
]

def generate_slug():
    return ''.join(str(random.randint(0, 9)) for _ in range(8))
    
class Packet(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    # need to search between countries TODO
    origin_country = models.ForeignKey(Country, on_delete = models.PROTECT,related_name="origin_country")
    # should select just related city not all city TODO
    # need to search between cities TODO
    origin_city = models.ForeignKey(City, on_delete=models.PROTECT,related_name="origin_city")
    destination_country = models.ForeignKey(Country, on_delete=models.PROTECT,related_name="destination_country")
    # should select just related city not all city also not the same with origin city TODO
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT,related_name="destination_city")
    category = models.CharField(max_length=20, choices=PACKET_CATEGORY)
    weight = models.PositiveIntegerField() # should be validate ( normally up to 30 kg) TODO
    weight_unit = models.CharField(max_length=5, choices=Weight_Unit)
    suggested_price = models.PositiveIntegerField()
    currency_price = models.CharField("currency",max_length=3, choices=CURRENCY)  
    place_of_get = models.CharField(max_length=20 ,choices=PLACE) 
    place_of_give = models.CharField(max_length=20 ,choices=PLACE)  
    start_date = models.DateField()
    end_date = models.DateField()
    buy = models.BooleanField("buy availibity")
    qr_code = models.ImageField(blank = True) # is it correct ? TODO
    visit_count = models.PositiveIntegerField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    picture = models.ImageField(blank = True) # need at least 3 picture TODO
    slug = models.CharField(defualt=generate_slug, editable=False, unique=True, db_index=True)
 
    def __str__(self):
        return str(self.id)
    
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         super().save(*args, **kwargs)
    #         try:
    #            
    #             super().save(*args, **kwargs)
    #         except IntegrityError:
    #             self.save(*args, **kwargs)
    #     super().save(*args, **kwargs)


class Travel(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    departure = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="depar_country")
    departure_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="depar_city")
    destination = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="dest_country")
    destination_city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="dest_city")
    empty_weight = models.PositiveIntegerField() # should be validate ( normally up to 30 kg)
    weight_unit = models.CharField(max_length=3, choices=Weight_Unit)
    ticket = models.OneToOneField('Ticket', on_delete=models.PROTECT) 
    place_of_get = models.CharField(max_length=20, choices=PLACE)
    place_of_give = models.CharField(max_length=20, choices=PLACE)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    # travel_date = models.DateField()  # should be future TODO
    # ticket_picture = models.FileField(blank=True) # must validate format(pdf & jpg) and size TODO

    def __str__(self):
        return str(self.id)

    # we should check if the user has right to send travel info TODO
    def check_permisssion(self):
        pass

class Offer(BaseModel):
    packet = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="packet_ads")
    travel = models.ForeignKey(Travel, on_delete=models.PROTECT, related_name="travel_ads")
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY)

    def __str__(self):
        return str(self.id)
    
    # we should check if the user has right to send offer TODO
    def check_permisssion(self):
        pass
    # not same owner for travel and packet 
    # same origin and destinatin for travel and packet

    # calculate number of offer to change the status of packet
    def change_status(self):
        pass
    
class Bookmark(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owner_bookmark")
    advertise = models.ForeignKey(Packet, on_delete=models.PROTECT, related_name="advertise")

    def __str__(self):
        return "%s --> %s" %(self.owner,self.advertise)

class Report(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter")
    packet = models.ForeignKey(Packet, on_delete=models.CASCADE)
    title = models.CharField(max_length=3, choices=REPORT_CHOICES)
    text = models.TextField()

    def __str__(self):
        return "%s --> %s" %(self.owner,self.packet)

class Ticket(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    date = models.DateTimeField("date")
    airline = models.CharField(max_length=40, choices=Airlines, blank=True)
    pic = models.FileField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s --> %s" %(self.owner, self.airline)

