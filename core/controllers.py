class DefaultControllers(object):
    model = None

    @classmethod
    def get_all(cls):
        if cls.model is None:
            return []
        return cls.model.objects.filter(enable=True)

    @classmethod
    def get_by_uuid(cls, obj_uuid):
        if cls.model is None:
            return None
        object_list = cls.model.objects.filter(uuid=obj_uuid, enable=True)
        if object_list.exists():
            return object_list[0]
        return None

    @classmethod
    def get_by_id(cls, obj_id):
        if cls.model is None:
            return None
        obj_id = str(obj_id)
        if not obj_id.isdigit():
            return None
        object_list = cls.model.objects.filter(pk=int(obj_id))
        if object_list.exists():
            return object_list[0]
        return None

    @classmethod
    def get_by_id_club_premier(cls, obj_id):
        if cls.model is None:
            return None
        object_list = cls.model.objects.filter(club_premier_id=obj_id, enable=True)
        if object_list.exists():
            return object_list[0]
        return None
