import uuid
import time
import datetime
import dateutil.parser
from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.FloatField(default=time.time)
    date_created = models.DateTimeField(default=datetime.datetime.utcnow)
    wallet_address = models.CharField(max_length=1024, null=False)

    def __str__(self):
        return str(f"{self.id} | {self.user_id} | {self.wallet_address}")

    def __repr__(self):
        return str(f"{self.id} | {self.user_id} | {self.wallet_address}")

    def __unicode__(self):
        return str(f"{self.id} | {self.user_id} | {self.wallet_address}")
    class Meta:
        db_table = 'user_123'

class BuyHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    buy_history_id = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.FloatField(default=time.time)
    date_created = models.DateTimeField(default=datetime.datetime.utcnow)
    amount_bnb = models.FloatField(null=False, blank=False)
    package_selected = models.FloatField(default=0)
    is_complete = models.BooleanField(default=False)
    note = models.CharField(max_length=1024, null=True, blank=True)

    def check_time_over(self):
        now = time.time()
        time_over = now - self.created_at
        return time_over

    def is_complete_task(self):
        time_over = self.check_time_over()
        day_over = time_over / (24 * 60 * 60)
        if self.is_complete:
            return True
        if day_over > 90:
            self.is_complete = True
            self.save()
            return True
        return False

    def get_total_bnbk(self):
        return self.amount_bnb * (1000000 / 2)

    def get_day_over(self):
        now = datetime.datetime.utcnow().astimezone(datetime.timezone.utc)
        start_date = dateutil.parser.parse(
            self.date_created.isoformat()).astimezone(datetime.timezone.utc)
        return abs((now - start_date).days)

    def get_current_bnb_profit(self):
        day_over = self.get_day_over()
        if self.get_program_type() == 1:
            return day_over * (self.amount_bnb * (0.8 / 100))
        elif self.get_program_type() == 2:
            return day_over * (self.amount_bnb * (0.9 / 100))
        elif self.get_program_type() == 3:
            return day_over * (self.amount_bnb * (1.1 / 100))
        else:
            return day_over * (self.amount_bnb * (1.5 / 100))

    def get_current_bnbk_profit(self):
        day_over = self.get_day_over()
        if self.get_program_type() == 1:
            return day_over * (self.get_total_bnbk() * (1.2 / 100))
        elif self.get_program_type() == 2:
            return day_over * (self.get_total_bnbk() * (2.1 / 100))
        elif self.get_program_type() == 3:
            return day_over * (self.get_total_bnbk() * (3.9 / 100))
        else:
            return day_over * (self.get_total_bnbk() * (4.5 / 100))
    
    def get_interest_per_day(self):
        if self.get_program_type() == 1:
            return "2%"
        elif self.get_program_type() == 2:
            return "3%"
        elif self.get_program_type() == 3:
            return "5%"
        else:
            return "6%"

    def get_date_started(self):
        return self.date_created

    def get_date_finished(self):
        return self.date_created + datetime.timedelta(days=90)

    def get_program_type(self):
        if 0.1 <= self.amount_bnb <= 1:
            return 1
        elif 1 < self.amount_bnb <= 3:
            return 2
        elif 3 < self.amount_bnb <= 10:
            return 3
        else:
            return 4

    def __str__(self):
        return str(f"{self.id} | {self.user.user_id} | {self.user.wallet_address} | {self.amount_bnb} | {self.is_complete} | {self.note}")

    def __repr__(self):
        return str(f"{self.id} | {self.user.user_id} | {self.user.wallet_address} | {self.amount_bnb} | {self.is_complete} | {self.note}")

    def __unicode__(self):
        return str(f"{self.id} | {self.user.user_id} | {self.user.wallet_address} | {self.amount_bnb} | {self.is_complete} | {self.note}")
    class Meta:
        db_table = 'buyhistory'
class Introduction(models.Model):
    id = models.AutoField(primary_key=True)
    wallet_address = models.CharField(max_length=1024, null=False)
    wallet_address_introduced = models.CharField(max_length=1024, null=False)
    F_ratings = models.CharField(default='F?',max_length=54, null=False)
    created_at = models.FloatField(default=time.time)
    date_created = models.DateTimeField(default=datetime.datetime.utcnow)
    class Meta:
        db_table = 'introduction'

class PayInterest(models.Model):
    id = models.AutoField(primary_key=True)
    wallet_address = models.CharField(max_length=1024, null=False)
    interest_introduced = models.FloatField(default=0)
    interest_package = models.FloatField(default=0)
    timeProccess = models.FloatField(default=0)
    created_at = models.FloatField(default=time.time)
    date_created = models.DateTimeField(default=datetime.datetime.utcnow)
    