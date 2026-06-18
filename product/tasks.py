from celery import shared_task
from time import sleep


@shared_task
def generate_product_report(product_id):
    sleep(5)
    print(f"Report generated for product {product_id}")
    return f"Report for product {product_id} is ready"
