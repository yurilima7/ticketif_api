from fastapi import APIRouter, Body, HTTPException
from ldap3 import Server, Connection
import json
import re
from auth.auth import create_account, authenticate, create_access_token, create_refresh_token

auth_router = APIRouter()


# Rota responsável pelo registro do aula
@auth_router.post("/register")
async def register(name: str = Body(...), matricula: str = Body(...), password: str = Body(...),
                   type_student: str = Body(...)):
    await create_account(name, matricula, password, type_student)
    return {"message": "Estudante criado com sucesso"}


# Rota responsável por efetuar o login
@auth_router.post("/login")
async def login(matricula: str = Body(...), password: str = Body(...)):
    student = await authenticate(matricula, password)

    if not student:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = await create_access_token(student["matricula"])
    refresh_token = await create_refresh_token(student["matricula"])
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@auth_router.get("/users")
def get_user():
    ldaprdn = "20181TIMTCX0027"
    ldappass = "nescaucereal"

    if ldaprdn:
        if ldappass:
            server = Server("ldap://10.9.10.50:389")
            conn = Connection(server, user=f"CN={ldaprdn},OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu",
                              password=ldappass)

            if conn.bind():
                conn.search("OU=Alunos,OU=CAMP-CAX,OU=IFMA,DC=ifma,DC=edu", f"(samaccountname={ldaprdn})", attributes=["*"])
                data = conn.entries
                if data:
                    # name = data[0]['displayName'].value
                    # user_json = json.dumps(f"OK:{name}")
                    # print(user_json)
                    print(data[0])
                else:
                    error_json = json.dumps("Login ou senha inválido")
                    print(error_json)
            else:
                error_json = json.dumps("Falha na autenticação")
                print(error_json)
        else:
            error_json = json.dumps("Preencher senha")
            print(error_json)
    else:
        error_json = json.dumps("Preencher matrícula")
        print(error_json)


def is_student_high_school(student):
    adm = "20231AD.CAX|20221AD.CAX|20211AD.CAX|20201AD.CAX|20191AD.CAX|20181AD.CAX|20171CXAD"
    agroind = "20231A.CAX|20221A.CAX|20211A.CAX|20201A.CAX|20191A.CAX|20181A.CAX|20171CXA|20231AE.CAX"
    agropec = "20231AP.CAX|20221AP.CAX|20211AP.CAX|20201AP.CAX|20191AP.CAX|20181AP.CAX|20171CXAP|20221APE.CAX"
    info = "20231IC.CAX|20221IC.CAX|20211IC.CAX|20201IC.CAX|20191CXIC|20191IC.CAX|20181IC.CAX|20171CXIC|20161CXIC"
    com = "20221COM.CAX"
    classes = f"{adm}|{agroind}|{agropec}|{info}|{com}"

    return re.match(classes, student) is not None
