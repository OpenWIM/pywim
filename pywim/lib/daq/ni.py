from datetime import datetime

import time
import sys
import numpy as np

try:
    import PyDAQmx as pydaq
except NotImplementedError:
    import pywim.lib.daq.generic as pydaq


def analog_task(settings):
    """

    """
    try:
        samples_per_channel = settings['samples_per_channel']
        number_of_channels = settings['number_of_channels_ai']

        # Analog dev
        print("\nCreating analog task %s." % settings['name'])
        sys.stdout.flush()

        # settings
        task = pydaq.Task()
        task.CreateAIVoltageChan(
            settings['analog_input'].encode('utf-8'),
            **settings['parameters_create_ai']
        )
        task.CfgSampClkTiming(
            **settings['parameters_sample_clock_time_ai'])

        if 'parameters_export_signal' in settings:
            for sig in settings['parameters_export_signal']:
                task.ExportSignal(**sig)

        if 'parameters_start_trigger' in settings:
            task.CfgDigEdgeStartTrig(**settings['parameters_start_trigger'])

        total_samples = pydaq.int32()
        data_size = samples_per_channel * number_of_channels

        print("\nStarting analog task %s." % settings['name'])

        task.StartTask()

        total_samples.value = 0

        run = True

        while run:
            run = yield

            data = np.zeros((data_size,), dtype=np.float64)

            task.ReadAnalogF64(
                samples_per_channel,
                10.0,
                pydaq.DAQmx_Val_GroupByChannel,
                data,
                data_size,
                pydaq.byref(total_samples),
                None
            )
            yield data

    except:
        pass

    task.StopTask()
    task.ClearTask()


def digital_task(semaphore, semaphore_dev, counter, samples_queue, settings):
    """
    Digital
    Need to start the dio task first!

    """
    try:
        print("\nCreating digital task %s." % settings['name'])
        sys.stdout.flush()

        # settings
        samples_per_channel = settings['samples_per_channel']
        number_of_channels = settings['number_of_channels_di']

        total_samps = pydaq.int32()
        total_bytes = pydaq.int32()

        data_size = samples_per_channel * number_of_channels

        task = pydaq.Task()
        task.CreateDIChan(
            settings['digital_input'].encode('utf-8'),
            b'', pydaq.DAQmx_Val_ChanPerLine
        )
        task.CfgSampClkTiming(
            **settings['parameters_sample_clock_time_di']
        )

        print("\nStarting digital task %s." % settings['name'])
        sys.stdout.flush()

        task.StartTask()

        total_samps.value = 0
        total_bytes.value = 0

        run = True

        while run:
            run = yield

            data = np.zeros((data_size,), dtype=np.uint8 )

            task.ReadDigitalLines(
                samples_per_channel,  # numSampsPerChan
                10.0,  # timeout
                pydaq.DAQmx_Val_GroupByChannel,  # fillMode
                data,  # readArray
                data_size,  # arraySizeInBytes
                pydaq.byref(total_samps),  # sampsPerChanRead
                pydaq.byref(total_bytes),  # numBytesPerChan
                None  # reserved
            )
            yield data
    except:
        pass

    task.StopTask()
    task.ClearTask()
