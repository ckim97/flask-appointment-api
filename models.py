from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import string, datetime

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)
db = SQLAlchemy(metadata=metadata)


class Patient(db.Model, SerializerMixin):
    __tablename__ = "patient_table"
    serialize_rules = ['-appointments.patient']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient")

    #doctors = [a.doctor for a in appointments]
    doctors = association_proxy("appointments", "doctor")




class Appointment(db.Model, SerializerMixin):
    __tablename__ = "appointment_table"
    serialize_rules = ['-patient.appointments', '-doctor.appointments']
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctor_table.id"), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient_table.id"), nullable=False)

    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")
    


    @validates("day")
    def validate_day(self, key, day):
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        if day not in weekdays:
            raise ValueError("Day must be between Monday and Friday")
        return day

class Doctor(db.Model, SerializerMixin):
    __tablename__ = "doctor_table"
    serialize_rules = ['-appointments.doctor']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String, nullable=False)

    appointments = db.relationship("Appointment", back_populates="doctor")

    patients = association_proxy("appointments", "patient")

    @validates("name")
    def validate_name(self, key, name):
        if not name.startswith("Dr."):
            raise ValueError("Doctor name must start with Dr. ")
        return name
    
    