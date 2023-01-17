from ConnectionSQL import Session
from models.RoleApprove import RoleApproveModel


class ClsRoleApprove:

    @classmethod
    def get_all_not_approved(cls, id_user_bayer_connected: int) -> list:
        session = Session()
        try:
            dados = session\
                .query(RoleApproveModel) \
                .filter(RoleApproveModel.ID_USER_BAYER_CONNECTED == id_user_bayer_connected) \
                .filter(RoleApproveModel.FL_APPROVE.is_(None))\
                .all()
            return dados
        finally:
            session.close()
