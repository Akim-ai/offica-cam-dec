from faststream.rabbit import RabbitQueue

queue_create_data_get = RabbitQueue(
    'create_data_get', auto_delete=True,
    routing_key='create_data_get'
)
