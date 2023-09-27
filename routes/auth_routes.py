from fastapi import APIRouter, Body, HTTPException
from ldap3 import Server, Connection
import json
from auth.auth import create_account, authenticate
from models.student import Student
from repositories.student_repository import get_auth_student as get_student, get_type_student, create_student

auth_router = APIRouter()


# Rota responsável pelo registro do usuário adm
@auth_router.post("/register-adm")
async def register(username: str = Body(...), password: str = Body(...), loginTypeId: int = Body(...)):
    await create_account(username, loginTypeId, password)
    return {"message": "Usuário criado com sucesso"}


# Rota responsável por efetuar o login adm
@auth_router.post("/login-adm")
async def login(username: str = Body(...), password: str = Body(...)):

    user = await authenticate(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    login_type = user["login_type_id"]

    return {"user": username, "login_type_id": login_type}


# Rota responsável por efetuar o login
@auth_router.post("/login")
async def login(matricula: str = Body(...), password: str = Body(...)):
    print('matricula ' + matricula)
    if matricula:
        if password:
            student = await get_student(matricula)
            verification_type = await get_type_student(matricula)
            print(student)

            return {"result": 'Login realizado com sucesso!', "matricula": matricula}

            # server = Server("ldap://10.9.10.50:389")
            # conn = Connection(server, user=f"CN={matricula},OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu",
            #                   password=password)
            #
            # if conn.bind():
            #     conn.search("OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu", f"(samaccountname={matricula})",
            #                 attributes=["*"])
            #     data = conn.entries
            #     if data:
            #         student = await get_student(matricula)
            #         verification_type = await get_type_student(matricula)
            #         print(student)
            #         print(data[0]['displayname'].value)
            #
            #         if not student:
            #             name = data[0]['displayname'].value
            #             await create_student(Student(name=name, matricula=matricula, password='', type=verification_type))
            #             print(data[0])
            #             print(student)
            #             print(verification_type)
            #
            #         return {"result": 'Login realizado com sucesso!', "matricula": matricula}
            #
            #     else:
            #         error_json = json.dumps("Falha na autenticação!")
            #         print(error_json)
            #         raise HTTPException(status_code=404, detail="Falha na autenticação!")
            # else:
            #     error_json = json.dumps("Login ou senha inválido")
            #     print(error_json)
            #     raise HTTPException(status_code=401, detail="Login ou senha inválido!")
        else:
            error_json = json.dumps("Preencher senha")
            print(error_json)
            raise HTTPException(status_code=400, detail="Preencher senha!")
    else:
        error_json = json.dumps("Preencher matrícula")
        print(error_json)
        raise HTTPException(status_code=400, detail="Preencher matrícula!!")

