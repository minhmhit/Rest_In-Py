class StaffInfo:
    def __init__(self,id=None,name=None,sex=None,birthday=None,role=None,username=None,password=None,permissions=None):
        self.id = id
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.role = role
        self.username = username
        self.password = password
        self.permissions = permissions

    def haveNone(self):
        if self.id is None: return True
        if self.name is None: return True
        if self.sex is None: return True
        if self.birthday is None: return True
        if self.role is None: return True
        if self.username is None: return True
        if self.password is None: return True
        if self.permissions is None: return True
        return False

    def get_values_for_treeview(self):
        """Returns a tuple of values in the correct order for Treeview display (YYYY-MM-DD)."""
        return (
            self.id, self.name, self.sex, self.birthday,
            self.role, self.username, self.password,
            self.permissions,
        )
