"""Camera Access"""
from harvesters.core import Harvester
import numpy as np
from PIL import Image

class ImageAcquisition:
    def __init__(self, cti_file_path, serial_number):
        self.harvester = Harvester()
        self.cti_file_path = cti_file_path
        self.serial_number = serial_number

    def initialize(self):
        self.harvester.add_file(self.cti_file_path)
        self.harvester.update()

        if len(self.harvester.device_info_list) > 0:
            self.impact_acquire = self.harvester.create({'serial_number': self.serial_number})
        else:
            print('No devices found.')
            exit()

    def acquire_image(self, output_file_path='output.png'):
        self.impact_acquire.start()

        with self.impact_acquire.fetch() as buffer:
            component = buffer.payload.components[0]
            _2d = component.data.reshape(component.height, component.width)
            image = Image.fromarray(_2d)
            image.show()
            image.save(output_file_path)

        self.impact_acquire.stop()
        self.impact_acquire.destroy()

    def reset_harvester(self):
        self.harvester.reset()

if __name__ == "__main__":
    cti_path = 'C:/Program Files/Balluff/Impact Acquire/bin/x64/mvGenTLProducer.cti'
    serial_number = '22FG049'

    image_acquisition = ImageAcquisition(cti_path, serial_number)
    image_acquisition.initialize()
    image_acquisition.acquire_image()
    image_acquisition.reset_harvester()
