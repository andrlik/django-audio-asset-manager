import rules


@rules.predicate
def is_object_owner(user, obj):
    return user == obj.owner
