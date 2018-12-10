from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from Dining.models import UserDiningSettings, DiningList
from UserDetails.models import User

"""""""""""""""""""""""""""""""""""""""""""""""""""
Adjust the credits due to dining list or related objects deletion
"""""""""""""""""""""""""""""""""""""""""""""""""""


@receiver(pre_delete, sender=DiningList)
def clear_list_funding(sender, instance=None, **kwargs):
    """
    When a complete dining_list is deleted, errors could occur due to the chain of recomputations after each DiningEntry
    deletion. To prevent this the dining_list auto reverts the cost to 0 reducing the number of credit recomputations
    to a single run_down.
    Note: if the Dining_list is already locked, this doesn't need to happen.
    :param sender: The DiningList class
    :param instance: The DiningList instance
    :param kwargs: not used in current implementation
    :return:
    """
    if instance.isAdjustable():
        instance.auto_pay = False
        instance.kitchen_cost = 0
        instance.save()


"""""""""""""""""""""""""""""""""""""""""""""""""""
Create a dining_detail entry when a new user signs up
"""""""""""""""""""""""""""""""""""""""""""""""""""


@receiver(post_save, sender=User)
@receiver(post_save, sender=User)
def create_user_dining_details(sender, instance=False, created=False, **kwargs):
    """
    Create a new userDiningSettingsModel upon creation of a user model (note, not userinformation as it does not catch
    the manage.py createsuperuser)
    :param sender:
    :param instance: the created instance
    :param created: whether this instance was newly created
    :param kwargs: not used
    """
    if created:
        instance = User.objects.get(pk=instance.pk)
        UserDiningSettings(user=instance).save()
