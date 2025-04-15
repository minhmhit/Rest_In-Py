class CustomerInfo:
    def __init__(self,id=None,name=None,sex=None,birthday=None,national=None,country=None,checkin_date=None,room_type=None,room_number=None):
        self.id = id
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.national = national
        self.country = country
        self.checkin_date = checkin_date
        self.room_type = room_type
        self.room_number = room_number

    # def getID(self): return self.id
    # def getName(self): return self.name
    # def getSex(self): return self.sex
    # def getBirthDay(self): return self.birthday
    # def getNational(self): return self.national
    # def getCountry(self): return self.country
    # def getCheckinDate(self): return self.checkin_date
    # def getRoomType(self): return self.room_type

    def haveNone(self): 
        if self.id is None: return True
        if self.name is None: return True
        if self.sex is None: return True
        if self.birthday is None: return True
        if self.national is None: return True
        if self.country is None: return True
        if self.checkin_date is None: return True
        if self.room_type is None: return True
        return False
