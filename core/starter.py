import threading


def starter(*exchanges):
    for exchange in exchanges:
        job = threading.Thread(target=exchange.run)
        job.start()