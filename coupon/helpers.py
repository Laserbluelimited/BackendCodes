from re import U
import string
import random

from django.conf import settings
from . import models


def get_coupon_code_length(length=12):
    return settings.DSC_COUPON_CODE_LENGTH if hasattr(settings, 'DSC_COUPON_CODE_LENGTH') else length


def get_user_model():
    return settings.AUTH_USER_MODEL


def get_random_code(length=12):
    length = get_coupon_code_length(length=length)
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def create_ruleset_obj(form):
    #allowed users rule
    all_users = form.cleaned_data['all_users']
    all_ind_users = form.cleaned_data['all_ind_users']
    all_cor_users = form.cleaned_data['all_cor_users']
    users = form.cleaned_data['users']
    
    allowed_user_rule = models.AllowedUsersRule.objects.create(all_users=all_users,all_individual_users=all_ind_users, all_corporate_users=all_cor_users)
    allowed_user_rule.users.set(users)

    #maxusesrule
    max_uses1 = form.cleaned_data['max_uses']
    is_infinite = form.cleaned_data['is_infinite']
    uses_per_user = form.cleaned_data['uses_per_user']

    if uses_per_user is None or uses_per_user<1:
        uses_per_user=1



    max_uses_rule = models.MaxUsesRule.objects.create(max_uses=max_uses1, is_infinite=is_infinite, uses_per_user=uses_per_user)

    #validityrule
    expiration_date = form.cleaned_data['expiration_date']
    is_active = form.cleaned_data['is_active']

    validity_rule = models.ValidityRule.objects.create(expiration_date=expiration_date, is_active=is_active)

    #ruleset
    ruleset = models.Ruleset.objects.create(allowed_users=allowed_user_rule,max_uses=max_uses_rule, validity=validity_rule)

    return ruleset
