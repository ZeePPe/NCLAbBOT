from NCLabBot1.config import DefaultConfig
from datetime import date
import textwrap
import pyodbc


class DBConnector:
    def __init__(self):
        self.connection_string = textwrap.dedent('''
            Driver={driver};
            Server={server};
            Database={database};
            Uid={username};
            Pwd={password};
            Encrypt=yes;
            TrustServerCertificate=no;
            Connection Timeout=30;
        '''.format(
            driver=DefaultConfig.SQL_DRIVER,
            server=DefaultConfig.SQL_SERVER,
            database=DefaultConfig.SQL_DATABASE_NAME,
            username=DefaultConfig.SQL_USERNAME,
            password=DefaultConfig.SQL_PASSWORD
        ))

    def _execute_query(self, query):
        # connection object
        cnxn: pyodbc.Connection = pyodbc.connect(self.connection_string)
        crsr: pyodbc.Cursor = cnxn.cursor()
        crsr.execute(query)
        result = crsr.fetchall()
        cnxn.close()
        return result

    def _execute_update(self, query):
        # connection object
        cnxn: pyodbc.Connection = pyodbc.connect(self.connection_string)
        crsr: pyodbc.Cursor = cnxn.cursor()
        crsr.execute(query)
        cnxn.commit()
        cnxn.close()

    def get_all_appelli(self, date_query='now'):
        if date_query == "now":
            query = "SELECT * FROM Appelli WHERE data >='{today}'".format(today=date.today())
        else:
            query = "SELECT * FROM Appelli WHERE data ='{data}'".format(data=date_query)

        lista_appelli = self._execute_query(query)

        if len(lista_appelli) > 0:
            return_value = "Ho trovato questi appelli:\n"
            for appello in lista_appelli:
                return_value += appello[1] + " il " + str(appello[2]) + "\n"
        else:
            return_value = "Nessun appello previsto."

        return return_value

    def get_appelli_esame(self, esame):
        query = "SELECT * FROM Appelli WHERE nome_corso='{esame}' and data >='{today}'".format(esame=esame,
                                                                                               today=date.today())

        lista_appelli = self._execute_query(query)

        if len(lista_appelli) > 0:
            return_value = "Ho trovato questi appelli:\n"
            for appello in lista_appelli:
                return_value += appello[1] + " il " + str(appello[2]) + "\n"
        else:
            return_value = "Nessun appello previsto."

        return return_value

    def update_interesati(self, esame):
        query = "UPDATE appelli SET interessati = interessati + 1 WHERE nome_corso='{esame}'".format(esame=esame)

        self._execute_update(query)

    def get_interessati(self, esame):
        query = "SELECT interessati FROM appelli WHERE nome_corso='{esame}' AND data >='{data}'".format(esame=esame,
                                                                                                        data=date.today())

        interessati = self._execute_query(query)

        if len(interessati) > 0:
            return_value = "Sono interessati {numero} studenti al prossimo appello di {esame}.\n".\
                format(numero=interessati[0][0],
                       esame=esame)

        else:
            return_value = "Nessun appello previsto di {esame}.".format(esame=esame)

        return return_value
