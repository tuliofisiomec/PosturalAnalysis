import cv2


class ImageResizer:

    def __init__(self, image_url: str, new_width: int = 500, new_height: int = 300):
        self.image_url = image_url
        self.new_width = new_width
        self.new_height = new_height

    def resize_image(self):
        img = cv2.imread(self.image_url, cv2.IMREAD_UNCHANGED)
        dim = (self.new_width, self.new_height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized

    def write_resized_image(self, resized_image):
        cv2.imwrite('resized.jpeg', resized_image)
        
    def run(self):
        resized = self.resize_image()
        self.write_resized_image(resized)


if __name__ == '__main__':
    resizer = ImageResizer('RoundedShoulderRaw/rounded_shoulder_1.jpeg')
    resizer.run()
    