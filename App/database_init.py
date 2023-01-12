import pandas as pd
from sqlalchemy import create_engine

connect = create_engine(
    "mysql+pymysql://{utilisateur}:{mdp}@mysql_db/{nom_db}?charset=utf8".
    format(utilisateur="admin", mdp="root", nom_db="webservice"))
data = pd.read_csv("database/train.csv")
data.to_sql(con=connect, name="train", if_exists="replace", index=False)

data1 = pd.read_csv("database/reservation.csv")
data1.to_sql(con=connect, name="reservation", if_exists="replace", index=True)
