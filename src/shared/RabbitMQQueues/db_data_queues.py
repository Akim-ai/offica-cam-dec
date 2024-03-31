from faststream.rabbit import RabbitQueue

queue_create_frame = RabbitQueue(
    'create_frame', auto_delete=True,
    routing_key='create_frame',
)

queue_create_camera = RabbitQueue(
    'create_camera', auto_delete=True,
    routing_key='create_camera',
)
queue_get_camera = RabbitQueue(
    'get_camera', auto_delete=True,
    routing_key='get_camera'
)
queue_get_cameras = RabbitQueue(
    'get_cameras', auto_delete=True,
    routing_key='get_cameras',
)

queue_put_camera = RabbitQueue(
    'put_camera', auto_delete=True,
    routing_key='put_camera'
)

queue_get_frame_processors = RabbitQueue(
    'get_frame_processors', auto_delete=True,
    routing_key='get_frame_processors',
)

queue_get_all_data_gets = RabbitQueue(
    'get_all_data_gets', auto_delete=True,
    routing_key='get_all_data_gets'
)

queue_get_all_detected_users = RabbitQueue(
    'get_all_detected_users', auto_delete=True,
    routing_key='get_all_detected_users'
)

queue_get_user = RabbitQueue(
    'get_user', auto_delete=True,
    routing_key='get_user'
)

queue_get_users = RabbitQueue(
    'get_users', auto_delete=True,
    routing_key='get_users'
)

queue_delete_user = RabbitQueue(
    'delete_user', auto_delete=True,
    routing_key='delete_user'
)

queue_get_auth_user = RabbitQueue(
    'get_auth_user', auto_delete=True,
    routing_key='get_auth_user'
)


queue_create_user: RabbitQueue = RabbitQueue(
    'create_detected_user', auto_delete=True,
    routing_key='create_detected_user',
)

queue_get_frames_by_user: RabbitQueue = RabbitQueue(
    "get_frames_by_user", auto_delete=True,
    routing_key="get_frames_by_user"
)

queue_create_frame_with_boxes = RabbitQueue(
    'create_frame_with_boxes', auto_delete=True,
    routing_key='create_frame_with_boxes',
)

queue_get_frames = RabbitQueue(
    'get_frames', auto_delete=True,
    routing_key='get_frames'
)

