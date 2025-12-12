
from datetime import datetime
class ITTicket:
 """Represents an IT support ticket."""
 def __init__(self, id: int, title: str, priority: str, status: str, created_date: datetime):
   self.__id = id
   self.__title = title
   self.__priority = priority
   self.__status = status
   self.__created_date = created_date

 def get_id(self) -> int:
   return self.__id 
 
 def get_title(self) -> str:
   return self.__title
 
 def get_priority(self) -> str:
   return self.__priority
 
 def get_created_date(self) -> datetime:
   return self.__created_date



 def close_ticket(self) -> None:
   self.__status = "Closed"
 
 def get_status(self) -> str:
   return self.__status
 
 def __str__(self) -> str:
   return (
 f"Ticket {self.__id}: {self.__title} "
 f"[{self.__priority}] – {self.__status} (assigned to: {self.__created_date})"
 )
