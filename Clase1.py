from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine(f'sqlite:///notas_estudiantes.db')

#Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class Estudiante(Base):
    __tablename__ = 'estudiantes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String)
    
    def __repr__(self):
        return f'{self.nombre} {self.apellido}' 
    

class Notas(Base):
    __tablename__ = 'notas'
    id = Column(Integer, primary_key=True)
    nota = Column(Float, nullable=False)
    materia = Column(String, nullable=False)
    
    estudiante_id = Column(Integer, ForeignKey('estudiantes.id'))

    def __repr__(self):
        return f'nota: {self.nota}'
    
Base.metadata.create_all(engine)


def crearUsuario():
    estudiante1 = Estudiante(nombre = 'Paul', apellido = 'Ochoa')
    session.add(estudiante1)
    session.commit()

    nota1 = Notas(nota= 10, materia = 'Programacion',estudiante_id = estudiante1.id)
    session.add(nota1)
    session.commit()
    
crearUsuario()

def consultar():
    estudiante1 = session.query(Estudiante).filter_by(nombre='Paul').first()
    
    nota1 = session.query(Notas).filter_by(estudiante_id=estudiante1.id).first()
    
    print(f"La nota del {estudiante1.nombre} {estudiante1.apellido} es {nota1.nota} en la materia {nota1.materia}")
    
consultar()
    