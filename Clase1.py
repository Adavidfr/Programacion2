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
    
    nombre = input("Ingrese el nombre del estudiante: ")
    apellido = input("Ingrese el apellido del estudiante: ")
    
    estudiante1 = Estudiante(nombre=nombre, apellido=apellido)
    session.add(estudiante1)
    session.commit()
    
    print(f"Estudiante {estudiante1.nombre} {estudiante1.apellido} creado exitosamente.")
    
def crearNotas():
    
    nombre_estudiante = input("Ingrese el nombre del estudiante: ")
    apellido_estudiante = input("Ingrese el apellido del estudiante: ")
        
    estudiante1 = session.query(Estudiante).filter_by(nombre=nombre_estudiante, apellido=apellido_estudiante).first()
    
    if estudiante1:
        materia = input("Ingrese la materia: ")
        while True:
            try:
                nota = float(input("Ingrese la nota: "))
                break
            except ValueError:
                print("Por favor, ingrese un número válido para la nota.")
    
        nota1 = Notas(nota= nota, materia = materia, estudiante_id = estudiante1.id)
        session.add(nota1)
        session.commit()
        print(f"Nota de {estudiante1.nombre} {estudiante1.apellido} en {materia} creada exitosamente.")
    else:
        print("Estudiante no encontrado.")
        
def modificarNotas():
    nombre_estudiante = input("Ingrese el nombre del estudiante para modificar la nota: ")
    apellido_estudiante = input("Ingrese el apellido del estudiante para modificar la nota: ")
    estudiante1 = session.query(Estudiante).filter_by(nombre=nombre_estudiante, apellido=apellido_estudiante).first()
    
    if estudiante1:
        materia = input("Ingrese la materia cuya nota desea cambiar: ")
        nota_existente = session.query(Notas).filter_by(estudiante_id=estudiante1.id, materia=materia).first()
        
        if nota_existente:
            while True:
                try:
                    nueva_nota = float(input("Ingrese la nueva nota para {materia}: "))
                    break
                except ValueError:
                    print("Por favor, ingrese un número válido para la nota.")
            
            nota_existente.nota = nueva_nota
            session.commit()
            print(f"Nota de {estudiante1.nombre} {estudiante1.apellido} en {materia} modificada exitosamente.")
        else:
            print(f"No se encontró una nota para {estudiante1.nombre} {estudiante1.apellido} en {materia}.")
    else:
        print("Estudiante no encontrado.")     
       
   
def eliminarNotas():
    nombre_estudiante = input("Ingrese el nombre del estudiante para eliminar la nota: ")
    apellido_estudiante = input("Ingrese el apellido del estudiante para eliminar la nota: ")
    estudiante1 = session.query(Estudiante).filter_by(nombre=nombre_estudiante, apellido=apellido_estudiante).first()
    
    if estudiante1:
        materia = input("Ingrese la materia cuya nota desea eliminar: ")
        nota_existente = session.query(Notas).filter_by(estudiante_id=estudiante1.id, materia=materia).first()
        
        if nota_existente:
            session.delete(nota_existente)
            session.commit()
            print(f"Nota de {estudiante1.nombre} {estudiante1.apellido} en {materia} eliminada exitosamente.")
        else:
            print(f"No se encontró una nota para {estudiante1.nombre} {estudiante1.apellido} en {materia}.")
    else:
        print("Estudiante no encontrado.")

def consultar():
    nombre_estudiante = input("Ingrese el nombre del estudiante para consultar sus notas: ")
    estudiante1 = session.query(Estudiante).filter_by(nombre=nombre_estudiante).first()

    if estudiante1:
        notas = session.query(Notas).filter_by(estudiante_id=estudiante1.id).all()
        if notas:
            print(f"Notas de {estudiante1.nombre} {estudiante1.apellido}:")
            for nota in notas:
                print(f"{nota.materia}: {nota.nota}")
        else:
            print(f"{estudiante1.nombre} no tiene notas registradas.")
    else:
        print("Estudiante no encontrado.")

def menu():
    while True:
        print("\nMenú de opciones:")
        print("1. Crear estudiante")
        print("2. Crear notas")
        print("3. Consultar notas")
        print("4. Modificar nota")
        print("5. Eliminar nota")
        print("6. Salir")

        opcion = input("Seleccione una opción (1-6): ")

        if opcion == '1':
            crearUsuario()
        elif opcion == '2':
            crearNotas()
        elif opcion == '3':
            consultar()
        elif opcion == '4':
            modificarNota()
        elif opcion == '5':
            eliminarNota()
        elif opcion == '6':
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

# Ejecutar el menú
menu()