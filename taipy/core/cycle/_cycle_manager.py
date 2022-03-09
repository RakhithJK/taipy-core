import calendar
from datetime import datetime, time, timedelta
from typing import Optional

from taipy.core.common._manager import _Manager
from taipy.core.common.frequency import Frequency
from taipy.core.cycle._cycle_repository import _CycleRepository
from taipy.core.cycle.cycle import Cycle


class _CycleManager(_Manager[Cycle]):

    _repository = _CycleRepository()
    _ENTITY_NAME = Cycle.__name__

    @classmethod
    def _create(
        cls, frequency: Frequency, name: str = None, creation_date: datetime = None, display_name=None, **properties
    ):
        creation_date = creation_date if creation_date else datetime.now()
        start_date = _CycleManager._get_start_date_of_cycle(frequency, creation_date)
        end_date = _CycleManager._get_end_date_of_cycle(frequency, start_date)
        properties["display_name"] = display_name if display_name else start_date.isoformat()
        cycle = Cycle(
            frequency, properties, creation_date=creation_date, start_date=start_date, end_date=end_date, name=name
        )
        cls._set(cycle)
        return cycle

    @classmethod
    def _get_or_create(
        cls, frequency: Frequency, creation_date: Optional[datetime] = None, display_name: Optional[str] = None
    ) -> Cycle:
        creation_date = creation_date if creation_date else datetime.now()
        start_date = _CycleManager._get_start_date_of_cycle(frequency, creation_date)
        cycles = cls._repository.get_cycles_by_frequency_and_start_date(frequency=frequency, start_date=start_date)
        if len(cycles) > 0:
            return cycles[0]
        else:
            return cls._create(frequency=frequency, creation_date=creation_date, display_name=display_name)

    @staticmethod
    def _get_start_date_of_cycle(frequency: Frequency, creation_date: datetime):
        start_date = creation_date.date()
        start_time = time()
        if frequency == Frequency.DAILY:
            start_date = start_date
        if frequency == Frequency.WEEKLY:
            start_date = start_date - timedelta(days=start_date.weekday())
        if frequency == Frequency.MONTHLY:
            start_date = start_date.replace(day=1)
        if frequency == Frequency.YEARLY:
            start_date = start_date.replace(day=1, month=1)
        return datetime.combine(start_date, start_time)

    @staticmethod
    def _get_end_date_of_cycle(frequency: Frequency, start_date: datetime):
        end_date = start_date
        if frequency == Frequency.DAILY:
            end_date = end_date + timedelta(days=1)
        if frequency == Frequency.WEEKLY:
            end_date = end_date + timedelta(7 - end_date.weekday())
        if frequency == Frequency.MONTHLY:
            last_day_of_month = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = end_date.replace(day=last_day_of_month) + timedelta(days=1)
        if frequency == Frequency.YEARLY:
            end_date = end_date.replace(month=12, day=31) + timedelta(days=1)
        return end_date - timedelta(microseconds=1)