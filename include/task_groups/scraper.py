from include.scraping_operations import DataScraper
from airflow.utils.task_group import TaskGroup
from airflow.decorators import task


class DataScraperTG(TaskGroup):

    def __init__(self, group_id, tooltip="Criacao da tabela arquivos na camada bronze do BigQuery e Cloud Storage", **kwargs):
        super().__init__(group_id=group_id, tooltip=tooltip, **kwargs)


        @task(task_group=self)
        def scrape_bloomberg():
            """Scrape Bloomberg data."""
            scraper = DataScraper()
            scraper.scrape_bloomberg()

        @task(task_group=self)
        def scrape_usd_cny():
            """Scrape USD/CNY data."""
            scraper = DataScraper()
            scraper.scrape_usd_cny()

        @task(task_group=self)
        def scrape_china_index():
            """Scrape China Index data."""
            scraper = DataScraper()
            scraper.scrape_china_index()

        scrape_bloomberg() >> scrape_usd_cny() >> scrape_china_index()

