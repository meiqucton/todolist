import urllib
from flask_sqlalchemy import SQLAlchemy

params = urllib.parse.quote_plus(
    "DRIVER=ODBC Driver 17 for SQL Server;"
    "SERVER=100.66.12.8,1433;" 
    "DATABASE=taskList;"
    "UID=sa;"
    "PWD=123456789@"
)

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        db.init_app(app)
