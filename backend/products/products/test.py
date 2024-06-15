from psycopg2 import connect


con = connect(dbname='productsdb', user='jackdropuser', password='27o40T01+10$04$sPg%Tristr_5o0e-Ps#rq')

print(con)

con.close()
