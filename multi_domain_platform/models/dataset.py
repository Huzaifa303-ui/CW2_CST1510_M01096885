class Dataset:
 """Represents a data science dataset in the platform."""
 def __init__(self, id: int, name: str, source: int, category: int, size: int):
   self.__id = id
   self.__name = name
   self.__source = source
   self.__category = category
   self.__size = size
 
 def get_id(self) -> int:
   return self.__id
 
 def get_name(self) -> str:
   return self.__name
 
 def get_category(self) -> str:
   return self.__category


 def calculate_size_mb(self) -> float:
   return self.__size / (1024 * 1024)
 
 def get_source(self) -> str:
   return self.__source
 
 def __str__(self) -> str:
   size_mb = self.calculate_size_mb()
   return f"Dataset {self.__id}: {self.__name} ({size_mb:.2f} MB, {self.__category} rows) from {self.__source}"