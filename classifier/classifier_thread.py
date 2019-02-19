from multiprocessing import Queue, Process
import importlib


def classify_fn(queue, done_queue):
    classifier = importlib.import_module('classifier.classifier')
    while True:
        if not queue.empty():
            print("queue has something")
            frames = input_queue.get()
            classification = classifier.classify_stream(frames)
            #output_queue.put(classification)
            print("DONE", classification)
            done_queue.put(classification)
            #cb(classification)


input_queue = Queue(maxsize=1)
output_queue = Queue(maxsize=1)
#output_queue = Queue(maxsize=1)

# initialize the prediction process
p = Process(target=classify_fn, args=(input_queue, output_queue, ))
p.daemon = True
p.start()


def start_classify_stream(frames, callback_when_done):
    global cb
    input_queue.put(frames)
    cb = callback_when_done
