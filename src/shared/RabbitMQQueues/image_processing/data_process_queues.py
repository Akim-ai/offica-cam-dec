from faststream.rabbit import RabbitQueue

queue_create_image_processor = RabbitQueue(
    "create_image_processor", auto_delete=True,
    routing_key='create_image_processor'
)

queue_run_image_processing = RabbitQueue(
    "run_image_processing", auto_delete=True,
    routing_key='run_image_processing'
)

queue_image_process_result = RabbitQueue(
    'image_process_result', auto_delete=True,
    routing_key='image_process_result'
)