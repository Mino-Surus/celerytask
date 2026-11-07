from celery import Celery

app = Celery('tasks', broker='amqp://guest:guest@localhost//')


@app.task(bind=True, max_retries=3, default_retry_delay=3)
def process_data(self, id):
    try:
        if id < 0:
            raise ValueError("Отрицательный id")
        if id == 0:
            raise RuntimeError("Нулевой id запрещён")
        return f"Данные для id={id} обработаны"
    except Exception as exc:
        self.retry(exc=exc)