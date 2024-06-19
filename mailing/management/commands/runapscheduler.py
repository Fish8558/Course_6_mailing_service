import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from mailing.services import start_mailing

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            start_mailing,
            trigger=CronTrigger(second="*/10"),
            id="start_mailing",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Запуск apscheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка apscheduler...")
            scheduler.shutdown()
            logger.info("Планировщик успешно завершил работу!")
