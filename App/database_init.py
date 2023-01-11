import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

connect = create_engine(
    "mysql+pymysql://{utilisateur}:{mdp}@localhost/{nom_db}?charset=utf8".
    format(utilisateur="root", mdp="", nom_db="webservice"))
data = pd.read_csv("database/train.csv")
data.to_sql(con=connect, name="train", if_exists="replace", index=False)

data1 = pd.read_csv("database/reservation.csv")
data1.to_sql(con=connect, name="reservation", if_exists="replace", index=True)
