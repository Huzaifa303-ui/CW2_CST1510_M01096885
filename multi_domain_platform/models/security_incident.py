import datetime

class SecurityIncident:
 """Represents a cybersecurity incident in the platform."""
 def __init__(self, id: int, title: str, severity: str , status: str, date: datetime):
   self.__id = id
   self.__title = title
   self.__severity = severity
   self.__status = status
   self.__date = date
 
 def get_id(self) -> int:
   return self.__id
 
 def get_severity(self) -> str:
   return self.__severity
 
 def get_status(self) -> str:
   return self.__status
 
 def get_date(self) -> str:
   return self.__date
 
 def get_title(self) -> str:
   return self.__title
 
 def update_status(self, new_status: str) -> None:
   self.__status = new_status
 
 def get_severity_level(self) -> int:
   mapping = {
     "low": 1,
     "medium": 2,
     "high": 3,
     "critical": 4,
 }
   return mapping.get(self.__severity.lower(), 0)

 def __str__(self) -> str:
   return f"Incident {self.__id} [{self.__severity.upper()}] {self.__title} - Status: {self.__status}"
 

 



 