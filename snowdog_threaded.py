from pynmeagps import NMEAReader                                                          >
from datetime import date, datetime
import json
import queue
from threading import Thread, Event
from time import sleep


def produce_values(nmr: NMEAReader, que: queue.Queue, shutdown: Event):
    while not shutdown.is_set():
        for (raw_data, parsed_data) in nmr:
            try:
                if parsed_data.identity == 'GPGGA':
                    if parsed_data.quality == 1:
                        data = {}

                        ts_date = str(date.today())
                        ts_time = str(parsed_data.time)
                        ts_raw = f"{ts_date} {ts_time}"
                        data['ts'] = datetime.strptime(ts_raw, '%Y-%m-%d %H:%M:%S').isoformat()
                        data['lat'] = parsed_data.lat
                        data['lon'] = parsed_data.lon
                        data['alt'] = parsed_data.alt
                        #print(json.dumps(data))

                        que.put_nowait(data)
            except queue.Full:
                print("Previous value not sent yet")
                # Check if process still running:
                if shutdown.is_set():
                    break
            except:
                pass

def send_values(que: queue.Queue, shutdown: Event):
    print("Sending values...")

    while not shutdown.is_set():
        if que.empty is False:
            data = que.get()
            print(json.dumps(data))
            que.task_done()


if __name__ == "__main__":
    que = queue.Queue(maxsize=1)
    shutdown_signal = Event()

    stream = open('/dev/EG25.NMEA', 'rb')
    nmr = NMEAReader(stream, nmeaonly=True)

    produce_values_thread = Thread(target=produce_values,
                                   args=(nmr,
                                         que,
                                         shutdown_signal))

    send_values_thread = Thread(target=send_values,
                                   args=(que,
                                         shutdown_signal))
    
    produce_values_thread.start()
    send_values_thread.start()


    while not shutdown_signal.is_set():
        try:
            sleep(1)
        except KeyboardInterrupt:
            print("Terminated by keyboard... Shutting down")
            shutdown_signal.set()

    produce_values_thread.join()
    send_values_thread.join()