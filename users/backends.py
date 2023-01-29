from django.contrib.auth.backends import ModelBackend
from . models import Accounts


class EmailAuthBackend(ModelBackend):

    #overriding  authenticate function 
    #by default it's a email password login, but we need to login through email or phone_number.
    def authenticate(self,phone_number=None,password=None,**kwargs) :

        if phone_number is None:
            phone_number = kwargs.get('email') #key-value from the login form will stored to the variable phone_number
                                                # (value of the key contains either email or phone_number)

        try:
            if (Accounts.objects.filter(email=phone_number).exists()): #if the key contains value of email
                user = Accounts.objects.get(email=phone_number)
            else:
                user = Accounts.objects.get(phone_number=phone_number) #if the key contains values of phone_number

            if user.check_password(password):
                user.backend = "%s.%s"%(self.__module__,self.__class__.__name__)
                return user
            else:
                return None
        except Accounts.DoesNotExist:
            return None                