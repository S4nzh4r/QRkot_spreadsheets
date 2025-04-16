from datetime import timedelta
from typing import Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
    CharityProjectUpdate
]):

    async def get_charity_prj_id_by_name(
        self,
        charity_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        charity_id = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_name
            )
        )
        charity_id = charity_id.scalars().first()
        return charity_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ) -> list[dict[str, str]]:
        duration = (
            extract('epoch', CharityProject.close_date) -
            extract('epoch', CharityProject.create_date)
        )
        projects = await session.execute(
            select(
                CharityProject.name,
                duration,
                CharityProject.description
            ).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(duration)
        )
        projects = projects.all()

        res = [
            {
                'name': str(name),
                'duration': str(timedelta(seconds=duration)),
                'description': str(description)
            }
            for name, duration, description in projects
        ]
        return res


charity_project_crud = CRUDCharityProject(CharityProject)
