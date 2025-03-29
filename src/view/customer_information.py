class CustomerInfo:
    def __init__(self,id,name,sex,birthday,national,country,checkin_date,room_type):
        self.id = id
        self.name = name
        self.sex = sex
        self.birthday = birthday
        self.national = national
        self.country = country
        self.checkin_date = checkin_date
        self.room_type = room_type

    def getID(self): return self.id
    def getName(self): return self.name
    def getSex(self): return self.sex
    def getBirthDay(self): return self.birthday
    def getNational(self): return self.national
    def getCountry(self): return self.country
    def getCheckinDate(self): return self.checkin_date
    def getRoomType(self): return self.room_type
