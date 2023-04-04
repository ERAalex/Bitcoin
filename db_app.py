from sqlalchemy import create_engine
import environ
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import FLOAT
from datetime import datetime

env = environ.Env()
environ.Env.read_env()

engine = create_engine(env('database'))
session = sessionmaker()
session.configure(bind=engine)
s = session()


Base = declarative_base()


class Cryptocurrency(Base):
    __tablename__ = 'cryptocurrency'

    id = Column(Integer(), primary_key=True)
    coin_name = Column(String(100), nullable=False, unique=False)
    price_usd = Column(Integer(), nullable=False)
    time = Column(DateTime(), default=datetime.now)
    changes_percent_last_call = Column(FLOAT, nullable=True)
    changes_percent_hour = Column(FLOAT, nullable=True)
    request_number = Column(Integer(), nullable=True)


class TableWork:
    def __init__(self):
        self.engine = create_engine(env('database'))
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
        self.s = self.session()

    def create_tables(self):
        Base = declarative_base()

        class Cryptocurrency(Base):
            __tablename__ = 'cryptocurrency'

            id = Column(Integer(), primary_key=True)
            coin_name = Column(String(100), nullable=False, unique=False)
            price_usd = Column(Integer(), nullable=False)
            time = Column(DateTime(), default=datetime.now)
            changes_percent_last_call = Column(FLOAT, nullable=True)
            changes_percent_hour = Column(FLOAT, nullable=True)
            request_number = Column(Integer(), nullable=True)

        Base.metadata.create_all(self.engine)

    def delete_informacion_db(self):
        s = self.session()
        s.query(Cryptocurrency).delete()
        s.commit()

    @staticmethod
    def get_number_data(currency_name, new_price):
        result = s.query(Cryptocurrency).filter(Cryptocurrency.coin_name == currency_name). \
            order_by(Cryptocurrency.time.desc()).first()

        if result == None:
            result_changes = 0
            return result_changes
        else:
            old_price = result.price_usd
            result_changes = round((new_price - old_price)/(old_price/100), 2)

            return result_changes

    @staticmethod
    def check_time(currency_name):
        check_time = s.query(Cryptocurrency).filter(Cryptocurrency.coin_name == currency_name,
                                                    Cryptocurrency.changes_percent_hour != None). \
            order_by(Cryptocurrency.time.desc()).first()

        if check_time == None:
            result_changes = 0
            return result_changes

        delta = datetime.now() - check_time.time
        result_time_pass = round((delta.total_seconds() // 60))
        # print('прошло с последней статистики за час ' + ' ' + str(result_time_pass) + ' ' + 'минут.')
        return result_time_pass


    @staticmethod
    def count_hour_change(currency_name):
        last_count = s.query(Cryptocurrency).filter(Cryptocurrency.coin_name == currency_name,
                                                    Cryptocurrency.changes_percent_hour != None). \
            order_by(Cryptocurrency.time.desc()).first()

        all_data = s.query(Cryptocurrency).filter(Cryptocurrency.coin_name == currency_name,
                                                   Cryptocurrency.id > last_count.id).all()

        count_percent_hour = 0
        for item in all_data:
            count_percent_hour += item.changes_percent_last_call

        return count_percent_hour


    def save_statics(self, currence_name, currence_usd_price):
        s = self.session()

        result_change = self.get_number_data(currence_name, currence_usd_price)

        if result_change >= 1 or result_change <= -1:
            print('Внимание валюта изменилась более чем на 1%')
            # в будущем можно связать с телеграмом

        time_check = self.check_time(currence_name)
        if time_check >= 60:
            result_hour_count_changes = self.count_hour_change(currence_name)
            create = Cryptocurrency(coin_name=currence_name,
                                    price_usd=currence_usd_price,
                                    changes_percent_last_call=result_change,
                                    changes_percent_hour=result_hour_count_changes)
        elif time_check == 0:
            create = Cryptocurrency(coin_name=currence_name,
                                    price_usd=currence_usd_price,
                                    changes_percent_last_call=result_change,
                                    changes_percent_hour=0)

        else:
            create = Cryptocurrency(coin_name=currence_name,
                                    price_usd=currence_usd_price,
                                    changes_percent_last_call=result_change)
        s.add(create)
        s.commit()

        return result_change


# work.create_tables()
# work.delete_information_db()
