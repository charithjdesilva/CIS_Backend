from sqlalchemy import Boolean,Column,Integer,String, Float,Date
from database import Base
from sqlalchemy import Column, String, Date, Time, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'Users'

    RegNo = Column(String(50), primary_key=True)
    NIC = Column(String(12), unique=True, nullable=False)
    FirstName = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    Tel_No = Column(String(10))
    Branch = Column(String(50))
    UserType = Column(String(15))
    JoinedDate = Column(Date)
    Position = Column(String(50))
    Photo = Column(String(100))
    Province = Column(String(25))
    District = Column(String(25))
    City = Column(String(50))
    Area = Column(String(200))
    HouseNoOrName = Column(String(100))



# # Define the Crime model
class Crime(Base):
    __tablename__ = 'Crime'

    CrimeID = Column(String(50), primary_key=True)
    CrimeType = Column(String(50))
    CrimeDate = Column(Date)
    CrimeTime = Column(Time)
    Province = Column(String(25))
    District = Column(String(25))
    City = Column(String(50))
    Area = Column(String(200))
    HouseNoOrName = Column(String(100))
    Landmarks = Column(String(200))
    Testimonials = Column(String(500))

# # Define the Evidence model
# class Evidence(Base):
#     __tablename__ = 'Evidence'

#     EvidenceID = Column(String(50), primary_key=True)
#     Testimonials = Column(String(500))

# # Define the Person model
# class Person(Base):
#     __tablename__ = 'Person'

#     PersonID = Column(String(100), primary_key=True)
#     NIC = Column(String(12), unique=True, nullable=False)
#     FirstName = Column(String(50), nullable=False)
#     LastName = Column(String(50), nullable=False)
#     PhoneNo = Column(String(10))
#     Branch = Column(String(50))
#     PersonType = Column(String(15))
#     LifeStatus = Column(String(5))
#     Photo = Column(String(100))
#     Province = Column(String(25))
#     District = Column(String(25))
#     City = Column(String(50))
#     Area = Column(String(200))
#     HouseNoOrName = Column(String(100))

# # Define the CriminalOrSuspect model
# class CriminalOrSuspect(Base):
#     __tablename__ = 'CriminalOrSuspect'

#     InCustody = Column(Boolean)
#     CrimeJustified = Column(Boolean)
#     NIC = Column(String(12), unique=True, nullable=False)
#     Person = relationship("Person", back_populates="CriminalOrSuspect")

# # Define the CrimeCriminal model
# class CrimeCriminal(Base):
#     __tablename__ = 'CrimeCriminal'

#     NIC = Column(String(12), ForeignKey('Person.NIC'), primary_key=True)
#     CrimeID = Column(String(50), ForeignKey('Crime.CrimeID'), primary_key=True)

# # Define the Photos model
class Photos(Base):
    __tablename__ = 'Photos'

    PhotoID = Column(String(110), primary_key=True)
    PhotoType = Column(String(13))
    PhotoPath = Column(String(180))

# # Define the CrimePhoto model
class CrimePhoto(Base):
    __tablename__ = 'CrimePhoto'

    PhotoID = Column(String(110), ForeignKey('Photos.PhotoID'), primary_key=True)
    CrimeID = Column(String(50), ForeignKey('Crime.CrimeID'), primary_key=True)

# # Define the PersonPhoto model
# class PersonPhoto(Base):
#     __tablename__ = 'PersonPhoto'

#     PhotoID = Column(String(110), ForeignKey('Photos.PhotoID'), primary_key=True)
#     PersonID = Column(String(100), ForeignKey('Person.PersonID'), primary_key=True)

# # Define the EvidencePhoto model
# class EvidencePhoto(Base):
#     __tablename__ = 'EvidencePhoto'

#     PhotoID = Column(String(110), ForeignKey('Photos.PhotoID'), primary_key=True)
#     EvidenceID = Column(String(50), ForeignKey('Evidence.EvidenceID'), primary_key=True)


