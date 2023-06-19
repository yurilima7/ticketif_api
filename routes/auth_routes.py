from fastapi import APIRouter, Body, HTTPException
from ldap3 import Server, Connection
import json
from auth.auth import create_account
from models.student import Student
from repositories.student_repository import get_auth_student as get_student, get_type_student, create_student

auth_router = APIRouter()


# Rota responsável pelo registro do aula
@auth_router.post("/register")
async def register(name: str = Body(...), matricula: str = Body(...), password: str = Body(...),
                   type_student: str = Body(...)):
    await create_account(name, matricula, password, type_student)
    return {"message": "Estudante criado com sucesso"}


# Rota responsável por efetuar o login
# @auth_router.post("/login")
# async def login(matricula: str = Body(...), password: str = Body(...)):
#     student = await authenticate(matricula, password)
#
#     if not student:
#         raise HTTPException(status_code=401, detail="Credenciais inválidas")
#
#     access_token = await create_access_token(student["matricula"])
#     refresh_token = await create_refresh_token(student["matricula"])
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@auth_router.post("/login")
async def login(matricula: str = Body(...), password: str = Body(...)):
    print('matricula ' + matricula)
    if matricula:
        if password:
            server = Server("ldap://10.9.10.50:389")
            conn = Connection(server, user=f"CN={matricula},OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu",
                              password=password)

            if conn.bind():
                conn.search("OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu", f"(samaccountname={matricula})",
                            attributes=["*"])
                data = conn.entries
                if data:
                    student = await get_student(matricula)
                    verification_type = await get_type_student(matricula)
                    print(student)

                    if not student:
                        name = data[0]['givenName'].value
                        user_json = json.dumps(f"OK:{name}")
                        await create_student(Student(name=name, matricula=matricula, password='', type=verification_type))
                        print(user_json)
                        print(data[0])
                        print(student)
                        print(verification_type)

                    return {"result": 'Login realizado com sucesso!', "matricula": matricula}

                else:
                    error_json = json.dumps("Falha na autenticação!")
                    print(error_json)
                    raise HTTPException(status_code=404, detail="Falha na autenticação!")
            else:
                error_json = json.dumps("Login ou senha inválido")
                print(error_json)
                raise HTTPException(status_code=401, detail="Login ou senha inválido!")
        else:
            error_json = json.dumps("Preencher senha")
            print(error_json)
            raise HTTPException(status_code=400, detail="Preencher senha!")
    else:
        error_json = json.dumps("Preencher matrícula")
        print(error_json)
        raise HTTPException(status_code=400, detail="Preencher matrícula!!")

