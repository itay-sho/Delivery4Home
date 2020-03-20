from datetime import timedelta

BEAT_SCHEDULE = {
    'telegram-task': [
        {
            # will call test_print method of PrintConsumer
            'type': 'run_bot',
            # message to pass to the consumer
            'message': {},
            # Every 5 seconds
            'schedule': timedelta(seconds=5)
        },
    ]
}