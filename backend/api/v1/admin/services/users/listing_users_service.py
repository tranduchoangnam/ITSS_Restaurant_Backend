from datetime import datetime

from sqlalchemy import Date, case, literal, or_
from sqlmodel import Session, String, cast, func, select

from backend.constants.account_status import AccountStatus
from backend.models.user import RoleCode, User
from backend.schemas.user import FilteringUsersQueryParams


def listing_users(db: Session, query_params: FilteringUsersQueryParams):
    conditions = _build_conditions(query_params)
    users = _get_users(db, query_params, conditions)
    total = _count_users(db, conditions)

    return users, total


def _get_users(db: Session, query_params: FilteringUsersQueryParams, conditions: list):

    query = (
        select(
            User.id,
            User.created_at,
            case(
                (
                    User.display_name.isnot(None),
                    User.display_name,
                ),
                else_=User.email,
            ).label("name"),
        )
        .where(*conditions)
        .group_by(User.id)
        .limit(query_params.per_page)
        .offset((query_params.page - 1) * query_params.per_page)
    )

    users = db.exec(query).mappings().all()

    return users


def _count_users(db: Session, conditions: list):
    query = select(func.count(User.id)).where(*conditions)
    total = db.exec(query).first()
    return total


def _build_conditions(query_params: FilteringUsersQueryParams):
    conditions = [User.role_code == RoleCode.USER]

    if query_params.name_keyword:
        name_keyword = query_params.name_keyword.lower()
        conditions.append(
            or_(
                cast(User.id, String).contains(name_keyword),
                func.lower(User.display_name).contains(name_keyword),
                func.lower(User.email).contains(name_keyword),
            )
        )

    if query_params.status == AccountStatus.active:
        conditions.append(User.deleted_at.is_(None))

    if query_params.status == AccountStatus.deleted:
        conditions.append(User.deleted_at.isnot(None))

    return conditions
