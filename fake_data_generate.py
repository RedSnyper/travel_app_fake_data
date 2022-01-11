import random
from faker import Faker
from database import engine, Session
from sqlalchemy import exc
import models


models.Base.metadata.create_all(bind=engine)
fake_gen = Faker()


def get_all_users_id() -> list:
    user_id_list: list[tuple] = Session().query(models.User.id).all()
    return [id for id_tuple in user_id_list for id in id_tuple]


def get_all_treks_id() -> list:
    trek_id_list: list[tuple] = Session().query(
        models.TrekDestination.id).all()
    return [id for id_tuple in trek_id_list for id in id_tuple]

#----------------------------------------------------------------------------------------------------------------------#


def generate_fake_user(n: int = 1) -> None:

    with Session() as session:
        try:
            for _ in range(n):
                fake_user = {
                    "full_name": fake_gen.name(),
                    "address": fake_gen.address(),
                    "email": fake_gen.email(),
                    "phone_no": fake_gen.phone_number(),
                    "password": fake_gen.password()
                }
                session.add(models.User(**fake_user))
                session.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_dest(n: int = 1) -> None:
    user_id_list = get_all_users_id()
    with Session() as session:
        try:
            for _ in range(n):
                user_id = random.choice(user_id_list)
                days = random.randint(2, 15)
                if days >= 2 and days <= 5:
                    difficulty = "Easy"
                    total_cost = random.randint(1000, 5000)
                elif days >= 6 and days <= 10:
                    difficulty = "Medium"
                    total_cost = random.randint(6000, 10000)
                else:
                    difficulty = "Hard"
                    total_cost = random.randint(10000, 20000)

                fake_destination = {
                    "title": f'{fake_gen.city()} To {fake_gen.city()}',
                    "days": days,
                    "difficulty": difficulty,
                    "total_cost": total_cost,
                    "user_id": user_id
                }
                session.add(models.TrekDestination(**fake_destination))
                session.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_iternaries(n: int = 1):
    ''' 
        Generates fake_itenaries
        
        - shuffle and not random.choices() cause trek_id is primary key and random.choice() might generate the same number. 
        - shuffling gives unique already existing trek_ids in random order.
 
    '''

    with Session() as session:
        try:
            trek_ids = get_all_treks_id()
            random.shuffle(trek_ids)
            for _ in range(n):
                while trek_ids:
                    trek_id = trek_ids.pop()
                    # if there are no existing itenaries of existing trek_destination, then only add.
                    if not session.query(models.Itenary).filter(models.Itenary.trek_destination_id == trek_id).first():
                        break
                else:
                    trek_id = None

                if trek_id:
                    trek_days = session.query(models.TrekDestination.days).filter(
                        models.TrekDestination.id == trek_id).all()[0][0]

                    start_destination = session.query(models.TrekDestination.title).filter(
                        models.TrekDestination.id == trek_id).all()[0][0].split('To')[0].strip()

                    final_destination = session.query(models.TrekDestination.title).filter(
                        models.TrekDestination.id == trek_id).all()[0][0].split('To')[-1].strip()

                    total_cost = session.query(models.TrekDestination.total_cost).filter(
                        models.TrekDestination.id == trek_id).all()[0][0]

                    for i in range(0, trek_days):
                        fake_iten = {
                            'trek_destination_id': trek_id,
                            "day": i+1,
                            "description": fake_gen.text(),
                            "day_cost": total_cost/trek_days,
                        }
                        if i == 0:
                            fake_iten.update(
                                {"title": f'{start_destination} To {fake_gen.city()}'})
                        elif i == trek_days - 1:
                            fake_iten.update(
                                {"title": f'{fake_gen.city()} To {final_destination}'})
                        else:
                            fake_iten.update(
                                {"title": f'{fake_gen.city()} To {fake_gen.city()}'})

                        session.add(models.Itenary(**fake_iten))
                        session.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_comments(n: int = 1):

    with Session() as session:
        try:
            for _ in range(n):
                fake_comment = {
                    "comment_on": random.choice(get_all_treks_id()),
                    "comment": fake_gen.text(),
                    "comment_by": random.choice(get_all_users_id()),
                }
                session.add(models.Comment(**fake_comment))
                session.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")


def generate_fake_votes(n: int = 1):

    with Session() as session:
        try:
            all_vote_combinations = [
                (user, trek) for user in get_all_users_id() for trek in get_all_treks_id()]

            random.shuffle(all_vote_combinations)
            for _ in range(n):
                while all_vote_combinations:
                    combination = all_vote_combinations.pop()
                    user_id, trek_id = combination[0], combination[1]
                    if not session.query(models.Vote).filter(models.Vote.user_id == user_id, models.Vote.trek_destination_id == trek_id).first():
                        break
                else:
                    user_id, trek_id = None, None
                if user_id and trek_id:
                    fake_vote = {
                        "user_id": user_id,
                        "trek_destination_id": trek_id
                    }
                    session.add(models.Vote(**fake_vote))
                    session.commit()
        except exc.SQLAlchemyError as err:
            print(
                f"error occured. \n Type : {type(err)} \n Description: {err}")


