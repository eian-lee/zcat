import threading

def threads(*exchanges):
    for exchange in exchanges:
        job = threading.Thread(target=exchange.run)
        job.start()