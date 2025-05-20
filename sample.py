from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

security = HTTPBasic()

VALID_USERNAME = "vebbox"
VALID_PASSWORD = "12345"


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

class Item(BaseModel):
    username: str
    age: str
    phno:str
    email:str
    cource:str



@app.post("/get")
def read_root1(obj: Item):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="firstdb",
        port="3306"
    )
    mypost = mydb.cursor()
    sql = "INSERT INTO details ( username, age, phno, email, cource) VALUES ( %s, %s, %s, %s, %s)"
    val = ( obj.username, obj.age, obj.phno, obj.email, obj.cource)
    mypost.execute(sql, val)
    mydb.commit()
    return {"message": "Data inserted successfully"}

@app.post("/view")
def read_root1():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="firstdb",
            port="3306"
        )

        mypost = mydb.cursor()
        mypost.execute("SELECT * FROM details")
        r = mypost.fetchall()
        mydb.commit()
        return r

@app.put("/update/{Id}")
def update_data(Id, obj:Item):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="firstdb",
        port=3306
    )
    mycursor = mydb.cursor()
    sql = "UPDATE details SET username=%s, age=%s, phno=%s, email=%s, cource=%s WHERE Id=%s"
    val = (obj.username, obj.age, obj.phno, obj.email, obj.cource, Id)
    mycursor.execute(sql ,val)
    mydb.commit()
    return {"message": "Data updated successfully"}

#
class deleterequest(BaseModel):
     Id:int

@app.delete("/delete")
def delete_data(d:deleterequest):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your actual password
        database="firstdb",
        port=3306
    )

    mycursor = mydb.cursor()
    sql = "DELETE FROM details WHERE Id = %s"
    val = (d.Id,)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()
    mydb.close
    return {"message": "Data deleted successfully"}