import functools

from ConnectionSQL import Session, or_
from models.RoleUser import RoleUserModel
from models.Users import UsersModel
from sqlalchemy import func


class ClsRoleUser():

    @classmethod
    def get_by_identification(cls, user_identification):
        session = Session()
        try:
            dados = session.query(RoleUserModel).filter(
                RoleUserModel.USER_IDENTIFICATION == str(user_identification)).all()
            return dados
        finally:
            session.close()

    @classmethod
    def get_group_members(cls, role_name: str) -> list:
        session = Session()
        try:
            dados = session.query(RoleUserModel).filter(RoleUserModel.ROLE_NAME == role_name).all()
            dados = [item.USER_IDENTIFICATION for item in dados]
            return dados
        finally:
            session.close()

    @classmethod
    def get_members_by_roles(cls, list_of_system_role: list) -> list:
        session = Session()
        try:
            dados: list = []

            for system_role in list_of_system_role:

                if system_role.ROLE != None:
                    ret_query = session \
                        .query(RoleUserModel) \
                        .filter(RoleUserModel.ROLE_NAME == system_role.ROLE.NAME) \
                        .all()

                    dados.extend([item.USER_IDENTIFICATION for item in ret_query])

            return dados
        finally:
            session.close()
